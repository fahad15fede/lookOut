import os
import psycopg2

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    return psycopg2.connect(DATABASE_URL)


def create_tables():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cameras(
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    source TEXT NOT NULL,
                    location VARCHAR(100),
                    is_enabled BOOLEAN NOT NULL DEFAULT TRUE,
                    status VARCHAR(20) NOT NULL DEFAULT 'offline',
                    vision_status VARCHAR(20) NOT NULL DEFAULT 'offline',
                    detection_model VARCHAR(50) NOT NULL DEFAULT 'YOLO11n',
                    tracking VARCHAR(50) NOT NULL DEFAULT 'ByteTrack',
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                    );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS intrusion_events (
                    id SERIAL PRIMARY KEY,
                    event_type VARCHAR(50) NOT NULL,
                    track_id INTEGER NOT NULL,
                    detected_at TIMESTAMPTZ NOT NULL,
                    image_path TEXT
                );
            """)
            cursor.execute("""
                ALTER TABLE intrusion_events
                ADD COLUMN IF NOT EXISTS camera_id INTEGER
                REFERENCES cameras(id);
            """)

            cursor.execute(
                """
                ALTER TABLE intrusion_events
                ADD COLUMN IF NOT EXISTS crop_path TEXT;
                """
            )

        connection.commit()

    finally:
        connection.close()