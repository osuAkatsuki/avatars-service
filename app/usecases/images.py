import io
import logging
from enum import Enum

from PIL import Image

from app.adapters import rekognition
from app.adapters import s3
from app.errors import Error
from app.errors import ErrorCode

DISALLOWED_MODERATION_LABELS = [
    "Explicit Nudity",
    "Suggestive",
    "Violence",
    "Visually Disturbing",
]


class ImageType(str, Enum):
    USER_PROFILE_PICTURE = "user_profile_picture"
    USER_PROFILE_BACKGROUND = "user_profile_background"
    CLAN_ICON = "clan_icon"
    SCREENSHOT = "screenshot"

    def get_s3_folder(self) -> str:
        return {
            ImageType.USER_PROFILE_PICTURE: "avatars",
            ImageType.USER_PROFILE_BACKGROUND: "profile-backgrounds",
            ImageType.CLAN_ICON: "clan-icons",
            ImageType.SCREENSHOT: "screenshots",
        }[self]

    def get_desirable_size(self) -> tuple[int, int]:
        return {
            ImageType.USER_PROFILE_PICTURE: (512, 512),
            ImageType.USER_PROFILE_BACKGROUND: (1920, 1080),
            ImageType.CLAN_ICON: (256, 256),
            ImageType.SCREENSHOT: (1920, 1080),
        }[self]


def should_disallow_upload(moderation_labels: list[str]) -> bool:
    return any(l in DISALLOWED_MODERATION_LABELS for l in moderation_labels)


async def upload_image(
    image_type: ImageType,
    body: bytes,
    file_name: str,
) -> None | Error:
    try:
        image = Image.open(body)

        # Resize Image
        image.resize(image_type.get_desirable_size())

        # TODO: Image Compression

        # Convert it to PNG format
        with io.BytesIO() as f:
            image.save(f, format="PNG")
            body = f.getvalue()
    except Exception:
        return Error("Invalid Image", ErrorCode.INVALID_CONTENT)

    moderation_labels = await rekognition.detect_moderation_labels(body)
    if moderation_labels is None:
        return Error("Service Unavailable", ErrorCode.SERVICE_UNAVAILABLE)

    if should_disallow_upload(moderation_labels):
        # TODO: store/audit log these occurrences persistently
        logging.warning(
            "Rejected image due to moderation labels",
            extra={
                "image_type": image_type,
                "file_name": file_name,
                "moderation_labels": moderation_labels,
            },
        )
        return Error("Inappropriate Content", ErrorCode.INAPPROPRIATE_CONTENT)

    await s3.upload(
        body=body,
        file_name=file_name,
        folder=image_type.get_s3_folder(),
        content_type="image/png",
    )
    return None
