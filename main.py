#!/usr/bin/env python3

import fastapi

import settings

import uvicorn
import logger

import exception_handling

import atexit


def main() -> int:
    logger.configure_logging()

    exception_handling.hook_exception_handlers()
    atexit.register(exception_handling.unhook_exception_handlers)

    uvicorn.run(
        "main:app",
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
