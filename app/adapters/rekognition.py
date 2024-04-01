import logging

import botocore.exceptions

import app.clients


async def detect_moderation_labels(image: bytes) -> list[str] | None:
    try:
        response = await app.clients.rekognition_client.detect_moderation_labels(
            Image={"Bytes": image},
            MinConfidence=70,
        )
    except app.clients.rekognition_client.exceptions.ImageTooLargeException:
        return None
    except (
        botocore.exceptions.BotoCoreError,
        botocore.exceptions.ClientError,
    ) as exc:
        logging.error("Failed to detect moderation labels", exc_info=exc)
        return None

    moderation_labels: list[str] = []
    for label in response.get("ModerationLabels", []):
        if label_name := label.get("Name"):
            moderation_labels.append(label_name)

    return moderation_labels
