import os
from pathlib import Path

import boto3
from botocore.exceptions import BotoCoreError, ClientError

AWS_REGION = os.getenv("AWS_REGION", "eu-north-1")
S3_BUCKET_NAME = os.getenv(
    "S3_BUCKET_NAME",
    "lookout-ai-evidence-fahad-847122344148-eu-north-1-an"
)

s3 = boto3.client(
    "s3",
    region_name=AWS_REGION
)

def upload_file(file_path: str, object_key: str) -> str:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File does not exist: {file_path}")

    try:
        s3.upload_file(
            str(path),
            S3_BUCKET_NAME,
            object_key
        )

        return object_key

    except (BotoCoreError, ClientError) as error:
        raise RuntimeError(
            f"Failed to upload file to S3: {error}"
        ) from error