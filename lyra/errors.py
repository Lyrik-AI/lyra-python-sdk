from __future__ import annotations

import httpx


class LyraError(Exception):
    """Base SDK exception."""


class LyraAPIError(LyraError):
    def __init__(self, message: str, *, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code

    @classmethod
    def from_response(cls, response: httpx.Response) -> "LyraAPIError":
        return cls(
            _response_message(response),
            status_code=response.status_code,
        )


class LyraAuthenticationError(LyraAPIError):
    pass


class LyraServerError(LyraAPIError):
    pass


class LyraResponseValidationError(LyraError):
    pass


def _response_message(response: httpx.Response) -> str:
    try:
        payload = response.json()
    except ValueError:
        return response.text or f"Lyra API request failed with {response.status_code}."
    if isinstance(payload, dict):
        detail = payload.get("detail")
        if isinstance(detail, str):
            return detail
        if detail is not None:
            return str(detail)
    return f"Lyra API request failed with {response.status_code}."
