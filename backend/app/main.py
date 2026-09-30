from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.database import create_tables, get_connection
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(
    title="lookOut API",
    description="Backend API for the lookOut home security system.",
    version="0.1.0",
    lifespan=lifespan
)

app.add_middleware(    #Middleware allowing permissions of hostings
    CORSMiddleware,
    allow_origins=[
        'http://localhost:5173',
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/evidence",
    StaticFiles(directory="recordings/intrusions"),
    name="evidence"
)

class IntrusionEventCreate(BaseModel):
    event_type: str
    track_id: int
    detected_at: datetime
    image_path: str | None = None
    crop_path: str | None = None
    camera_id: int


class CameraCreate(BaseModel):
    name: str
    source: str
    location: str |None = None

class CameraStatusUpdate(BaseModel):
    status: str
    vision_status: str


@app.get("/")
def root():
    return {
        "service": "lookOut API",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post('/api/cameras')
def create_camera(camera: CameraCreate):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
            INSERT INTO cameras(
            name,
            source,
            location)
            VALUES(%s, %s, %s)
            RETURNING
                    id,
                    name,
                    source,
                    location,
                    is_enabled,
                    status,
                    vision_status,
                    detection_model,
                    tracking,
                    created_at;
            """,(
                    camera.name,
                    camera.source,
                    camera.location
            ))

            row = cursor.fetchone()

        connection.commit()
        return {
            "id": row[0],
            "name": row[1],
            "source": row[2],
            "location": row[3],
            "is_enabled": row[4],
            "status": row[5],
            "vision_status": row[6],
            "detection_model": row[7],
            "tracking": row[8],
            "created_at": row[9]
        }

    finally:
        connection.close()

@app.get("/api/cameras")
def get_cameras():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    name,
                    source,
                    location,
                    is_enabled,
                    status,
                    vision_status,
                    detection_model,
                    tracking,
                    created_at
                FROM cameras
                ORDER BY id ASC;
                """
            )

            rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "name": row[1],
                "source": row[2],
                "location": row[3],
                "is_enabled": row[4],
                "status": row[5],
                "vision_status": row[6],
                "detection_model": row[7],
                "tracking": row[8],
                "created_at": row[9]
            }
            for row in rows
        ]

    finally:
        connection.close()

@app.patch("/api/cameras/{camera_id}/status")
def update_camera_status(
    camera_id: int,
    status_update: CameraStatusUpdate
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
            UPDATE cameras
            SET
                status = %s,
                vision_status = %s
            WHERE id = %s
            RETURNING
                id,
                name,
                source,
                location,
                is_enabled,
                status,
                vision_status,
                detection_model,
                tracking,
                created_at;
            """,
            (
                status_update.status,
                status_update.vision_status,
                camera_id
            ))

            row = cursor.fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail = f"Camera {camera_id} not found"
            )

        connection.commit()

        return {
            "id": row[0],
            "name": row[1],
            "source": row[2],
            "location": row[3],
            "is_enabled": row[4],
            "status": row[5],
            "vision_status": row[6],
            "detection_model": row[7],
            "tracking": row[8],
            "created_at": row[9]
        }

    finally:
        connection.close()

@app.post("/api/events", status_code=201)
def create_event(event: IntrusionEventCreate):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO intrusion_events
                    (event_type, track_id, detected_at, image_path, crop_path, camera_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id;
                """,
                (
                    event.event_type,
                    event.track_id,
                    event.detected_at,
                    event.image_path,
                    event.crop_path,
                    event.camera_id
                )
            )

            event_id = cursor.fetchone()[0]

        connection.commit()

        return {
            "id": event_id,
            **event.model_dump()
        }

    finally:
        connection.close()


@app.get("/api/events")
def get_events():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    e.id,
                    e.event_type,
                    e.track_id,
                    e.detected_at,
                    e.image_path,
                    e.crop_path,
                    e.camera_id,
                    c.name as camera_name,
                    c.location AS camera_location
                FROM intrusion_events e
                LEFT JOIN cameras c
                    ON e.camera_id = c.id
                ORDER BY e.detected_at DESC
            """)

            rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "event_type": row[1],
                "track_id": row[2],
                "detected_at": row[3],
                "image_path": row[4],
                "crop_path": row[5],
                "camera_id": row[6],
                "camera_name": row[7],
                "camera_location": row[8]
            }
            for row in rows
        ]

    finally:
        connection.close()