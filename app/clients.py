from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from types_aiobotocore_rekognition.client import RekognitionClient
    from types_aiobotocore_s3.client import S3Client

rekognition_client: "RekognitionClient"
s3_client: "S3Client"
