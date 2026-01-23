import pytest
from unittest.mock import AsyncMock, MagicMock
from polydown.api import PolyHavenClient

@pytest.mark.asyncio
async def test_get_asset_types():
    mock_session = MagicMock()
    mock_response = AsyncMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json.return_value = ["hdris", "textures"]
    mock_session.get.return_value.__aenter__.return_value = mock_response

    client = PolyHavenClient(mock_session)
    types = await client.get_asset_types()

    assert types == ["hdris", "textures"]
    mock_session.get.assert_called_with("https://api.polyhaven.com/types")

@pytest.mark.asyncio
async def test_get_assets():
    mock_session = MagicMock()
    mock_response = AsyncMock()
    mock_response.raise_for_status = MagicMock()
    # Mocking dict return
    mock_response.json.return_value = {"asset1": {}, "asset2": {}}
    mock_session.get.return_value.__aenter__.return_value = mock_response

    client = PolyHavenClient(mock_session)
    assets = await client.get_assets("hdris")

    assert set(assets) == {"asset1", "asset2"}
    mock_session.get.assert_called_with("https://api.polyhaven.com/assets?t=hdris")
