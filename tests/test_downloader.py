import pytest
import os
import tempfile
import hashlib
from unittest.mock import AsyncMock, MagicMock
from polydown.downloader import DownloadManager, DownloadTask

@pytest.mark.asyncio
async def test_download_file_success():
    mock_session = MagicMock()
    mock_response = AsyncMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.headers = {'content-length': '12'}

    content = b"test content"

    # Mock iter_chunked
    async def async_iter(chunk_size):
        yield content

    mock_response.content = MagicMock()
    mock_response.content.iter_chunked.side_effect = async_iter

    mock_session.get.return_value.__aenter__.return_value = mock_response

    with tempfile.TemporaryDirectory() as tmpdir:
        manager = DownloadManager(mock_session)
        task = DownloadTask(
            url="http://example.com/file.txt",
            destination_folder=tmpdir,
            filename="file.txt"
        )

        filename, status, verified = await manager.download(task)

        assert filename == "file.txt"
        assert status == "downloaded"
        assert verified is True

        file_path = os.path.join(tmpdir, "file.txt")
        assert os.path.exists(file_path)
        with open(file_path, "rb") as f:
            assert f.read() == content

@pytest.mark.asyncio
async def test_download_file_exists_skip():
    mock_session = MagicMock()

    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, "existing.txt")
        with open(file_path, "wb") as f:
            f.write(b"existing content")

        manager = DownloadManager(mock_session)
        task = DownloadTask(
            url="http://example.com/existing.txt",
            destination_folder=tmpdir,
            filename="existing.txt",
            overwrite=False
        )

        filename, status, verified = await manager.download(task)

        assert status == "exists"
        # Network call should not happen
        mock_session.get.assert_not_called()

@pytest.mark.asyncio
async def test_md5_verification():
    mock_session = MagicMock()
    mock_response = AsyncMock()
    mock_response.raise_for_status = MagicMock()
    content = b"test content"
    mock_response.headers = {'content-length': str(len(content))}

    async def async_iter(chunk_size):
        yield content

    mock_response.content = MagicMock()
    mock_response.content.iter_chunked.side_effect = async_iter

    mock_session.get.return_value.__aenter__.return_value = mock_response

    # Calculate correct MD5
    md5 = hashlib.md5(content).hexdigest()

    with tempfile.TemporaryDirectory() as tmpdir:
        manager = DownloadManager(mock_session)

        # Test Correct MD5
        task = DownloadTask(
            url="http://example.com/file.txt",
            destination_folder=tmpdir,
            filename="file.txt",
            md5=md5,
            overwrite=True
        )
        filename, status, verified = await manager.download(task)
        assert verified is True

        # Test Incorrect MD5
        task2 = DownloadTask(
            url="http://example.com/file2.txt",
            destination_folder=tmpdir,
            filename="file2.txt",
            md5="wrongmd5",
            overwrite=True
        )
        filename, status, verified = await manager.download(task2)
        assert verified is False
