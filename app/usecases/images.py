import io
import logging
from enum import Enum

from PIL import Image

from app.adapters import rekognition
from app.adapters import s3
from app.errors import Error
from app.errors import ErrorCode

DISALLOWED_MODERATION_LABELS = [
    # https://docs.aws.amazon.com/rekognition/latest/dg/moderation.html#moderation-api
    "Explicit Nudity",
    "Explicit Sexual Activity",
    "Sex Toys",
    "Obstructed Intimate Parts",
    "Self-Harm",
    "Blood & Gore",
    "Death and Emaciation",
    "Hate Symbols",
]


class ImageType(str, Enum):
    USER_AVATAR = "user_avatar"
    USER_PROFILE_BACKGROUND = "user_profile_background"
    CLAN_ICON = "clan_icon"
    SCREENSHOT = "screenshot"

    def get_s3_folder(self) -> str:
        return {
            ImageType.USER_AVATAR: "avatars",
            ImageType.USER_PROFILE_BACKGROUND: "profile-backgrounds",
            ImageType.CLAN_ICON: "clan-icons",
            ImageType.SCREENSHOT: "screenshots",
        }[self]

    def get_max_single_dimension_size(self) -> int:
        return {
            ImageType.USER_AVATAR: 512,
            ImageType.USER_PROFILE_BACKGROUND: 1920,
            ImageType.CLAN_ICON: 256,
            ImageType.SCREENSHOT: 1920,
        }[self]


def should_disallow_upload(moderation_labels: list[str]) -> bool:
    return any(l in DISALLOWED_MODERATION_LABELS for l in moderation_labels)


async def upload_image(
    image_type: ImageType,
    image_content: bytes,
    file_name: str,
) -> None | Error:
    try:
        with io.BytesIO(image_content) as read_file:
            image = Image.open(read_file)

            # Resize image if it is too large
            max_single_dimension_size =  image_type.get_max_single_dimension_size()
            if image.width > max_single_dimension_size or image.height > max_single_dimension_size:
                biggest_dim = max(image.width, image.height)
                ratio = max_single_dimension_size / biggest_dim
                new_width = int(image.width * ratio)
                new_height = int(image.height * ratio)
                image = image.resize((new_width, new_height))

            # TODO: Image Compression

            # Convert it to PNG format
            with io.BytesIO() as write_file:
                image.save(write_file, format="PNG")
                image_content = write_file.getvalue()
    except Exception:
        logging.exception(
            "Failed to process image",
            extra={
                "file_name": file_name,
                "image_type": image_type,
                "image_size": len(image_content),
            },
        )
        return Error("Invalid Image", ErrorCode.INVALID_CONTENT)

    if image_type is not ImageType.SCREENSHOT:
        # XXX: we currently do not moderate screenshots,
        # as it would be significantly higher qps/cost.
        moderation_labels = await rekognition.detect_moderation_labels(image_content)
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
        body=image_content,
        file_name=file_name,
        folder=image_type.get_s3_folder(),
        content_type="image/png",
    )
    return None
