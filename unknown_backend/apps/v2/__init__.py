"""NOT IMPLEMENTED."""

from fastapi import FastAPI

from unknown_backend.assemble.middleware import context_middleware
from unknown_backend.assemble.middleware import cors_middleware
from unknown_backend.assemble.middleware import session_context_id_middlewares

app = FastAPI(
    docs_url="/docs",
    middleware=[
        context_middleware,
        cors_middleware,
        session_context_id_middlewares,
    ],
)
