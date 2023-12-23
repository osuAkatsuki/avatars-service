from fastapi import APIRouter
from fastapi import Response

from app.adapters import s3

router = APIRouter()


@router.get("/api/v1/profile-backgrounds/{file_path:path}")
async def get_profile_background(file_path: str):
    if ".." in file_path or "/" in file_path:
        return Response(status_code=404)

    download_response = await s3.download(
        file_name=file_path,
        directory="profile-backgrounds",
    )
    if download_response is None:
        return Response(status_code=404)

    return Response(
        content=download_response["body"],
        media_type=download_response["content_type"],
    )
