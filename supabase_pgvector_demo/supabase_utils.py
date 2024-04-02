import os

from supabase.client import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
SUPABASE_BUCKET_ID = os.getenv("SUPABASE_BUCKET_ID", "")

SUPABASE_FOLDER_NAME = "src_images"

supabase_client = create_client(supabase_url=SUPABASE_URL, supabase_key=SUPABASE_KEY)


def upload_file(filename: str, image_file: bytes) -> str:
    remote_path = f"{SUPABASE_FOLDER_NAME}/{filename}"
    supabase_client.storage.from_(SUPABASE_BUCKET_ID).upload(remote_path, image_file)
    return remote_path


def get_signed_url(relative_path: str) -> dict[str, str]:
    return supabase_client.storage.from_(SUPABASE_BUCKET_ID).create_signed_url(
        relative_path,
        expires_in=600,
    )


# tests:
# with open("assets/logo.jpg", "rb") as image_file:
#     upload_file("logo.jpg", image_file.read())
