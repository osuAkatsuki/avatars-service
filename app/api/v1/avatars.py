from fastapi import APIRouter
from fastapi import Response

from app.adapters import s3

router = APIRouter()


@router.get("/avatars/{file_path:path}")
async def get_avatar(file_path: str):
    if ".." in file_path or "/" in file_path:
        return Response(status_code=404)

    content = await s3.download(file_path, "avatars")
    if content is None:
        return Response(status_code=404)

    return Response(content=content, media_type="image/png")
