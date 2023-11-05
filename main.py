#!/usr/bin/env python3
import atexit

import uvicorn
from fastapi import FastAPI

import app.clients
import app.exception_handling
import app.logging
import settings

asgi_app = FastAPI()


@asgi_app.on_event("startup")
async def startup() -> None:
    app.clients.s3_client = None
    if (
        config.AWS_ENDPOINT_URL
        and config.AWS_REGION
        and config.AWS_ACCESS_KEY_ID
        and config.AWS_SECRET_ACCESS_KEY
    ):
        app.clients.s3_client = await ctx_stack.enter_async_context(
            aiobotocore.session.get_session().create_client(  # type: ignore
                "s3",
                region_name=config.AWS_REGION,
                aws_access_key_id=config.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
                endpoint_url=config.AWS_ENDPOINT_URL,
            ),
        )

    app.logging.setup_logging()


@asgi_app.route("/avatars/{file_path:path}")
async def get_avatar(file_path: str) -> str:
    return file_path


def main() -> int:
    app.logging.configure_logging()

    app.exception_handling.hook_exception_handlers()
    atexit.register(app.exception_handling.unhook_exception_handlers)

    uvicorn.run(
        "main:asgi_app",
        reload=settings.CODE_HOTRELOAD,
        log_level=settings.LOG_LEVEL,
        server_header=False,
        date_header=False,
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        access_log=False,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
