from fastapi import APIRouter
from fastapi import File
from fastapi import Response

import app.usecases.images
import settings
from app.adapters import s3
from app.errors import Error
from app.errors import ErrorCode
from app.usecases.images import ImageType

router = APIRouter()


def _get_status_code_for_error(error_code: ErrorCode) -> int:
    return {
        ErrorCode.INVALID_CONTENT: 400,
        ErrorCode.INAPPROPRIATE_CONTENT: 400,
        ErrorCode.SERVICE_UNAVAILABLE: 503,
    }[error_code]


@router.post("/api/v1/avatars/{user_id}")
async def upload_avatar(user_id: str, file_content: bytes = File(...)):
    data = await app.usecases.images.upload_image(
        image_type=ImageType.USER_PROFILE_PICTURE,
        body=file_content,
        file_name=f"{user_id}.png",
    )
    if isinstance(data, Error):
        return Response(
            status_code=_get_status_code_for_error(data.code),
            content=data.user_feedback,
        )
    return Response(status_code=201)


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
            return Response(status_code=404)

    return Response(
        content=download_response["body"],
        media_type=download_response["content_type"],
    )
