from http.client import HTTPException
from pathlib import Path

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.staticfiles import StaticFiles

from unknown_backend import apis
from unknown_backend.assemble import event
from unknown_backend.assemble import exception
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

# add static files
current_path = Path(__file__).resolve().parent
static_path = current_path.parent.parent.joinpath("static")
static_files = StaticFiles(directory=static_path)
app.mount("/static", static_files, name="static")

# add events
app.add_event_handler("startup", event.startup_event_1)
app.add_event_handler("startup", event.startup_event_2)
app.add_event_handler("shutdown", event.shutdown_event)

# add exception handlers
app.add_exception_handler(Exception, exception.exception_handler)
app.add_exception_handler(HTTPException, exception.http_exception_handler)
app.add_exception_handler(
    RequestValidationError, exception.validation_exception_handler
)

# add routers
app.include_router(apis.v1.index.router)

# Expose prometheus instrumentation
Instrumentator().instrument(app).expose(app)
