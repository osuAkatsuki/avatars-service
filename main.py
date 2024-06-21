#!/usr/bin/env python3
import atexit
from contextlib import asynccontextmanager

import aiobotocore.session
import uvicorn
from fastapi import FastAPI

import app.clients
import app.exception_handling
import app.logging
import settings
from app.api.v1 import avatars as avatars_v1
from app.api.v1 import profile_backgrounds as profile_backgrounds_v1


@asynccontextmanager
async def lifespan(asgi_app: FastAPI):
    session = aiobotocore.session.get_session()

    async with (
        session.create_client(
            service_name="s3",
            region_name=settings.AWS_S3_REGION,
            aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        ) as app.clients.s3_client,
        session.create_client(
            service_name="rekognition",
            region_name=settings.AWS_REKOGNITION_REGION,
            aws_access_key_id=settings.AWS_REKOGNITION_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_REKOGNITION_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_REKOGNITION_ENDPOINT_URL,
        ) as app.clients.rekognition_client,
    ):
        yield


asgi_app = FastAPI(lifespan=lifespan)


@asgi_app.get("/_health")
async def health():
    return {"status": "ok"}


asgi_app.include_router(avatars_v1.router)
asgi_app.include_router(profile_backgrounds_v1.router)


def main() -> int:
    app.logging.configure_logging()

    app.exception_handling.hook_exception_handlers()
    atexit.register(app.exception_handling.unhook_exception_handlers)

    uvicorn.run(
        "main:asgi_app",
        reload=settings.CODE_HOTRELOAD,
        server_header=False,
        date_header=False,
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        access_log=False,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
