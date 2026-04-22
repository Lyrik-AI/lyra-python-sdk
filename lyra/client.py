from __future__ import annotations

from typing import Any, TypeVar

import httpx
from pydantic import BaseModel, ValidationError

from lyra.config import LyraClientConfig
from lyra.errors import (
    LyraAPIError,
    LyraAuthenticationError,
    LyraResponseValidationError,
    LyraServerError,
)
from lyra.models import (
    DestinationDetail,
    DestinationListResponse,
    ExperienceDetail,
    ExperienceListResponse,
    GuideDetail,
    GuidesListResponse,
    RestaurantDetail,
    RouteDetail,
    RoutePageExperiences,
    RoutePageHotels,
    RoutePageItinerary,
    RoutePageJourney,
    RoutePageListResponse,
    RoutePageQueryResponse,
    RoutePageSummary,
    RoutesListResponse,
)

ModelT = TypeVar("ModelT", bound=BaseModel)


class AsyncLyraClient:
    """Async Python SDK for the Lyra/DataPipe internal API."""

    def __init__(
        self,
        *,
        base_url: str,
        api_key: str = "",
        timeout: float = 10.0,
        transport: httpx.AsyncBaseTransport | httpx.BaseTransport | None = None,
    ) -> None:
        self._config = LyraClientConfig(
            base_url=base_url,
            api_key=api_key,
            timeout=timeout,
        )
        self._transport = transport
        self.query = QueryNamespace(self)

    async def _get_model(
        self,
        path: str,
        *,
        response_model: type[ModelT],
        params: dict[str, Any] | None = None,
        allow_not_found: bool = False,
    ) -> ModelT | None:
        headers = self._config.headers()
        request_kwargs: dict[str, Any] = {"headers": headers}
        if params is not None:
            request_kwargs["params"] = params

        async with httpx.AsyncClient(
            base_url=self._config.base_url,
            timeout=self._config.timeout,
            transport=self._transport,
        ) as http_client:
            response = await http_client.get(path, **request_kwargs)

        if allow_not_found and response.status_code == 404:
            return None
        if response.status_code in {401, 403}:
            raise LyraAuthenticationError.from_response(response)
        if response.status_code >= 500:
            raise LyraServerError.from_response(response)
        if response.status_code >= 400:
            raise LyraAPIError.from_response(response)

        try:
            payload = response.json()
        except ValueError as exc:
            raise LyraResponseValidationError("Lyra response is not valid JSON.") from exc

        try:
            return response_model.model_validate(payload)
        except ValidationError as exc:
            raise LyraResponseValidationError("Lyra response does not match SDK model.") from exc


class QueryNamespace:
    def __init__(self, client: AsyncLyraClient) -> None:
        self.route_pages = RoutePagesNamespace(client)
        self.destinations = DestinationsNamespace(client)
        self.experiences = ExperiencesNamespace(client)
        self.guides = GuidesNamespace(client)
        self.restaurants = RestaurantsNamespace(client)
        self.routes = RoutesNamespace(client)


class RoutePagesNamespace:
    def __init__(self, client: AsyncLyraClient) -> None:
        self._client = client

    async def list(self) -> RoutePageListResponse:
        result = await self._client._get_model(
            "/api/v1/query/route-pages",
            response_model=RoutePageListResponse,
        )
        if result is None:
            raise LyraResponseValidationError("Lyra route page list response is empty.")
        return result

    async def summary(self, route_page_id: str) -> RoutePageSummary | None:
        result = await self._client._get_model(
            f"/api/v1/query/route-page/{route_page_id}",
            response_model=RoutePageQueryResponse,
            allow_not_found=True,
        )
        if result is None:
            return None
        return result.summary

    async def journey(self, route_page_id: str) -> RoutePageJourney | None:
        return await self._client._get_model(
            f"/api/v1/query/route-page/{route_page_id}/journey",
            response_model=RoutePageJourney,
            allow_not_found=True,
        )

    async def itinerary(self, route_page_id: str) -> RoutePageItinerary | None:
        return await self._client._get_model(
            f"/api/v1/query/route-page/{route_page_id}/itinerary",
            response_model=RoutePageItinerary,
            allow_not_found=True,
        )

    async def hotels(self, route_page_id: str) -> RoutePageHotels | None:
        return await self._client._get_model(
            f"/api/v1/query/route-page/{route_page_id}/hotels",
            response_model=RoutePageHotels,
            allow_not_found=True,
        )

    async def experiences(self, route_page_id: str) -> RoutePageExperiences | None:
        return await self._client._get_model(
            f"/api/v1/query/route-page/{route_page_id}/experiences",
            response_model=RoutePageExperiences,
            allow_not_found=True,
        )


class DestinationsNamespace:
    def __init__(self, client: AsyncLyraClient) -> None:
        self._client = client

    async def list(
        self,
        *,
        page: int = 1,
        page_size: int = 36,
        q: str = "",
        province: str = "",
    ) -> DestinationListResponse:
        result = await self._client._get_model(
            "/api/v1/query/destinations",
            response_model=DestinationListResponse,
            params={
                "page": page,
                "pageSize": page_size,
                "q": q,
                "province": province,
            },
        )
        if result is None:
            raise LyraResponseValidationError("Lyra destination list response is empty.")
        return result

    async def retrieve(
        self,
        destination_id: str,
        *,
        include: set[str] | None = None,
    ) -> DestinationDetail | None:
        include_value = ",".join(sorted(include or set()))
        return await self._client._get_model(
            f"/api/v1/query/destination/{destination_id}",
            response_model=DestinationDetail,
            params={"include": include_value} if include_value else None,
            allow_not_found=True,
        )


class GuidesNamespace:
    def __init__(self, client: AsyncLyraClient) -> None:
        self._client = client

    async def list(
        self,
        *,
        page: int = 1,
        page_size: int = 36,
        q: str = "",
        tag: str = "",
    ) -> GuidesListResponse:
        result = await self._client._get_model(
            "/api/v1/query/guides",
            response_model=GuidesListResponse,
            params={
                "page": page,
                "pageSize": page_size,
                "q": q,
                "tag": tag,
            },
        )
        if result is None:
            raise LyraResponseValidationError("Lyra guides list response is empty.")
        return result

    async def retrieve(self, slug: str) -> GuideDetail | None:
        return await self._client._get_model(
            f"/api/v1/query/guide/{slug}",
            response_model=GuideDetail,
            allow_not_found=True,
        )


class ExperiencesNamespace:
    def __init__(self, client: AsyncLyraClient) -> None:
        self._client = client

    async def list(
        self,
        *,
        page: int = 1,
        page_size: int = 36,
        q: str = "",
    ) -> ExperienceListResponse:
        result = await self._client._get_model(
            "/api/v1/query/experiences",
            response_model=ExperienceListResponse,
            params={
                "page": page,
                "pageSize": page_size,
                "q": q,
            },
        )
        if result is None:
            raise LyraResponseValidationError("Lyra experiences list response is empty.")
        return result

    async def retrieve(self, experience_id: str) -> ExperienceDetail | None:
        return await self._client._get_model(
            f"/api/v1/query/experience/{experience_id}",
            response_model=ExperienceDetail,
            allow_not_found=True,
        )


class RestaurantsNamespace:
    def __init__(self, client: AsyncLyraClient) -> None:
        self._client = client

    async def retrieve(self, restaurant_id: str) -> RestaurantDetail | None:
        return await self._client._get_model(
            f"/api/v1/query/restaurant/{restaurant_id}",
            response_model=RestaurantDetail,
            allow_not_found=True,
        )


class RoutesNamespace:
    def __init__(self, client: AsyncLyraClient) -> None:
        self._client = client

    async def list(
        self,
        *,
        page: int = 1,
        page_size: int = 36,
        q: str = "",
        sort: bool = True,
    ) -> RoutesListResponse:
        result = await self._client._get_model(
            "/api/v1/query/routes",
            response_model=RoutesListResponse,
            params={
                "page": page,
                "pageSize": page_size,
                "q": q,
                "sort": str(sort).lower(),
            },
        )
        if result is None:
            raise LyraResponseValidationError("Lyra routes list response is empty.")
        return result

    async def retrieve(self, route_id: str) -> RouteDetail | None:
        return await self._client._get_model(
            f"/api/v1/query/route-detail/{route_id}",
            response_model=RouteDetail,
            allow_not_found=True,
        )
