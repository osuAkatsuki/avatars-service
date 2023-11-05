#!/usr/bin/env python3
import atexit
import contextlib

import uvicorn
from fastapi import FastAPI

import app.clients
import app.exception_handling
import app.logging
import settings

asgi_app = FastAPI()


ctx_stack = contextlib.AsyncExitStack()


@asgi_app.on_event("startup")
async def startup() -> None:
    app.clients.s3_client = await ctx_stack.enter_async_context(
        aiobotocore.session.get_session().create_client(  # type: ignore
            "s3",
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_ENDPOINT_URL,
        ),
    )


@asgi_app.on_event("shutdown")
async def shutdown() -> None:
    await ctx_stack.aclose()


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
