"""API router composition."""

from fastapi import APIRouter

from app.api.routes import activities

api_router = APIRouter(prefix="/api")
api_router.include_router(activities.router, tags=["activities"])
