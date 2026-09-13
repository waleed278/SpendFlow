from fastapi import FastAPI

from app.core.config import settings

from app.routers.auth import router as auth_router
from app.routers.expenses import router as expenses_router
from app.routers.manager import router as manager_router
app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
)

# Include the aliased routers
app.include_router(auth_router)
app.include_router(expenses_router)
app.include_router(manager_router)