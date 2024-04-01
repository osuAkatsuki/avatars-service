import os

from dotenv import load_dotenv

load_dotenv()


def read_bool(value: str) -> bool:
    return value.lower() in ("1", "true")


APP_ENV = os.environ["APP_ENV"]
APP_HOST = os.environ["APP_HOST"]
APP_PORT = int(os.environ["APP_PORT"])

CODE_HOTRELOAD = read_bool(os.environ["CODE_HOTRELOAD"])

AWS_S3_REGION = os.environ["AWS_S3_REGION"]
AWS_S3_ACCESS_KEY_ID = os.environ["AWS_S3_ACCESS_KEY_ID"]
AWS_S3_SECRET_ACCESS_KEY = os.environ["AWS_S3_SECRET_ACCESS_KEY"]
AWS_S3_ENDPOINT_URL = os.environ["AWS_S3_ENDPOINT_URL"]
AWS_S3_BUCKET_NAME = os.environ["AWS_S3_BUCKET_NAME"]

AWS_REKOGNITION_REGION = os.environ["AWS_REKOGNITION_REGION"]
AWS_REKOGNITION_ACCESS_KEY_ID = os.environ["AWS_REKOGNITION_ACCESS_KEY_ID"]
AWS_REKOGNITION_SECRET_ACCESS_KEY = os.environ["AWS_REKOGNITION_SECRET_ACCESS_KEY"]
AWS_REKOGNITION_ENDPOINT_URL = os.environ["AWS_REKOGNITION_ENDPOINT_URL"]

DEFAULT_AVATAR_FILENAME = os.environ["DEFAULT_AVATAR_FILENAME"]
