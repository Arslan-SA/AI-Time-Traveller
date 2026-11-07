"""API router composition."""

from fastapi import APIRouter

from app.api.routes import activities, metrics

api_router = APIRouter(prefix="/api")
api_router.include_router(activities.router, tags=["activities"])
api_router.include_router(metrics.router, tags=["metrics"])
