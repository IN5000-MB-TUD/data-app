import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from server.routers import data

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s : %(message)s"
)
log = logging.getLogger(__name__)

# Initialize the app.
app = FastAPI(
    title="IN5000 TUD Data App",
    description="Repository data API and dashboard.",
    version="1.0.0",
)

# Assign API routes to the FastAPI app.
app.include_router(data.router)

# Setup CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the client side front-end
app.mount("", StaticFiles(directory="client/", html=True), name="static")
