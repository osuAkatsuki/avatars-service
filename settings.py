import os

from dotenv import load_dotenv

load_dotenv()


def read_bool(value: str) -> bool:
    return value.lower() in ("1", "true")


APP_ENV = os.environ["APP_ENV"]
APP_HOST = os.environ["APP_HOST"]
APP_PORT = int(os.environ["APP_PORT"])

CODE_HOTRELOAD = read_bool(os.environ["CODE_HOTRELOAD"])

S3_AWS_REGION = os.environ["S3_AWS_REGION"]
S3_AWS_ACCESS_KEY_ID = os.environ["S3_AWS_ACCESS_KEY_ID"]
S3_AWS_SECRET_ACCESS_KEY = os.environ["S3_AWS_SECRET_ACCESS_KEY"]
S3_AWS_ENDPOINT_URL = os.environ["S3_AWS_ENDPOINT_URL"]
S3_AWS_BUCKET_NAME = os.environ["S3_AWS_BUCKET_NAME"]

REKOGNITION_AWS_REGION = os.environ["REKOGNITION_AWS_REGION"]
REKOGNITION_AWS_ACCESS_KEY_ID = os.environ["REKOGNITION_AWS_ACCESS_KEY_ID"]
REKOGNITION_AWS_SECRET_ACCESS_KEY = os.environ["REKOGNITION_AWS_SECRET_ACCESS_KEY"]
REKOGNITION_AWS_ENDPOINT_URL = os.environ["REKOGNITION_AWS_ENDPOINT_URL"]

DEFAULT_AVATAR_FILENAME = os.environ["DEFAULT_AVATAR_FILENAME"]
