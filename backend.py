from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List

app = FastAPI(
    title="OTT Audience Segmentation API",
    description="Backend API for OTT viewer segmentation and recommendations",
    version="1.0.0"
)


# -----------------------------
# User Input Model
# -----------------------------
class UserProfile(BaseModel):
    user_id: str
    watch_time_hours: float = Field(ge=0)
    top_genres: List[str] = []
    avg_session_mins: float = Field(ge=0)


# -----------------------------
# Home API
# -----------------------------
@app.get("/")
def home():
    return {
        "message": "OTT Audience Segmentation Backend is Running"
    }


# -----------------------------
# Health Check
# -----------------------------
@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": True
    }


# -----------------------------
# Recommendation API
# -----------------------------
@app.post("/recommend")
def recommend(user: UserProfile):

    # Simple segmentation logic
    if user.watch_time_hours >= 50 and user.avg_session_mins >= 90:
        segment_id = 2
        segment_name = "Power Viewer"

    elif user.watch_time_hours >= 25 and user.avg_session_mins >= 60:
        segment_id = 1
        segment_name = "Engaged Viewer"

    else:
        segment_id = 0
        segment_name = "Casual Viewer"


    # Recommendation logic
    recommendations = []

    for genre in user.top_genres:
        recommendations.append(
            f"Recommended {genre} Content"
        )

    if len(recommendations) == 0:
        recommendations = [
            "Trending Now",
            "Popular Movies",
            "Recommended For You"
        ]


    return {
        "user_id": user.user_id,
        "segment_id": segment_id,
        "segment_name": segment_name,
        "recommendations": recommendations[:3],
        "distance_to_centroid": 0.0
    }