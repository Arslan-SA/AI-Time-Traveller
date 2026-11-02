"""FastAPI entrypoint for the AI Time Traveler API."""

from fastapi import FastAPI

app = FastAPI(
    title="AI Time Traveler API",
    description="Forecast personal productivity trends and simulate what-if scenarios.",
    version="0.1.0",
)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    """Report that the API process is running."""
    return {"status": "ok"}
