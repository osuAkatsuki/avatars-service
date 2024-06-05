import logging

from fastapi import APIRouter
from fastapi import Response

import settings
from app.adapters import s3

router = APIRouter()


@router.get("/api/v1/avatars/{file_path:path}")
async def get_avatar(file_path: str):
    if ".." in file_path or "/" in file_path:
        return Response(status_code=404)

    if not file_path.endswith(".png"):
        file_path += ".png"

    download_response = await s3.download(file_path, "avatars")
    if download_response is None:
        # fallback to a default avatar so we don't need to
        # duplicate the default avatar for all of our userbase
        download_response = await s3.download(
            file_name=settings.DEFAULT_AVATAR_FILENAME,
            directory="avatars",
        )
        if download_response is None:
            logging.warning(
                "Failed to serve non-existent user avatar and default avatar is missing",
                extra={"file_path": file_path},
            )
            return Response(status_code=404)

        file_path = settings.DEFAULT_AVATAR_FILENAME

    logging.info("Served user avatar", extra={"file_path": file_path})

    return Response(
        content=download_response["body"],
        media_type=download_response["content_type"],
    )
