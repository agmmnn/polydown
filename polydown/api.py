import aiohttp
from typing import List, Optional, Dict, Any

class PolyHavenClient:
    BASE_URL = "https://api.polyhaven.com"

    def __init__(self, session: Optional[aiohttp.ClientSession] = None):
        self.session = session
        self._own_session = False

    async def _get(self, endpoint: str) -> Any:
        if not self.session:
             self.session = aiohttp.ClientSession()
             self._own_session = True

        url = f"{self.BASE_URL}{endpoint}"
        async with self.session.get(url) as response:
            response.raise_for_status()
            return await response.json()

    async def close(self):
        if self._own_session and self.session:
            await self.session.close()

    async def get_asset_types(self) -> List[str]:
        """Fetch available asset types (e.g., hdris, textures, models)."""
        return await self._get("/types")

    async def get_categories(self, asset_type: str) -> List[str]:
        """Fetch categories for a given asset type."""
        return await self._get(f"/categories/{asset_type}")

    async def get_assets(self, asset_type: str, category: Optional[str] = None) -> List[str]:
        """Fetch list of asset IDs for a type and optional category."""
        params = f"?t={asset_type}"
        if category:
            params += f"&c={category}"
        data = await self._get(f"/assets{params}")
        # The API returns a dictionary where keys are asset IDs
        return list(data.keys())

    async def get_files(self, asset_id: str) -> Dict[str, Any]:
        """Fetch file metadata for a specific asset."""
        return await self._get(f"/files/{asset_id}")
