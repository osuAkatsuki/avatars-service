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

    content = await s3.download(file_path, "avatars")
    if content is None:
        # fallback to a default avatar so we don't need to
        # duplicate the default avatar for all of our userbase
        content = await s3.download(settings.DEFAULT_AVATAR_FILENAME, "avatars")
        if content is None:
            return Response(status_code=404)

    return Response(content=content, media_type="image/png")
