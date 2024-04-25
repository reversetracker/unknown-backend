from __future__ import annotations

import uuid

from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.types import ASGIApp, Scope, Receive, Send
from starlette_context import plugins
from starlette_context.middleware import RawContextMiddleware

from unknown_backend.database import session
from unknown_backend.database import contexts


class SqlAlchemyContextsMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        session_context = None
        nested_context = None
        try:
            session_id = str(uuid.uuid4())
            session_context = contexts.set_current_context_session_id(
                session_id=session_id
            )
            nested_context = contexts.set_current_context_nested_id(nested_context_id=0)
            await self.app(scope, receive, send)
        except Exception as e:
            raise e
        finally:
            # reset the session and all the contexts..
            await session.remove()
            if session_context:
                contexts.SESSION_CONTEXT.reset(session_context)
            if nested_context:
                contexts.NESTED_CONTEXT.reset(nested_context)


allow_origins = ["*"]
allow_methods = ["*"]
allow_headers = ["*"]

cors_middleware = Middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_methods=allow_methods,
    allow_headers=allow_headers,
    allow_credentials=True,
)

context_middleware = Middleware(
    RawContextMiddleware,
    plugins=[
        plugins.RequestIdPlugin(),
        plugins.CorrelationIdPlugin(),
    ],
)

session_context_id_middlewares = Middleware(
    SqlAlchemyContextsMiddleware,
)
