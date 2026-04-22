from pydantic import BaseModel, Field


class LyraClientConfig(BaseModel):
    base_url: str = Field(description="Lyra/DataPipe API base URL.")
    api_key: str = Field(default="", description="Internal bearer token.")
    timeout: float = Field(default=10.0, description="HTTP timeout in seconds.")

    def headers(self) -> dict[str, str]:
        token = self.api_key.strip()
        if not token:
            return {}
        return {"Authorization": f"Bearer {token}"}
