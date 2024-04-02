import os

from supabase.client import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
SUPABASE_BUCKET_ID = os.getenv("SUPABASE_BUCKET_ID", "image_search")

SUPABASE_FOLDER_NAME = "src_images"

supabase_client = create_client(supabase_url=SUPABASE_URL, supabase_key=SUPABASE_KEY)


def upload_file(filename: str, image_file: bytes) -> str:
    remote_path = f"{SUPABASE_FOLDER_NAME}/{filename}"
    supabase_client.storage.from_(SUPABASE_BUCKET_ID).upload(remote_path, image_file)
    return remote_path


def get_url(filename: str) -> str | None:
    return supabase_client.storage.from_(SUPABASE_BUCKET_ID).get_public_url(
        f"{SUPABASE_FOLDER_NAME}/{filename}",
    )


def fixed_public_url(filename: str) -> str:
    return f"https://oiulqpgzvnxyulmnqefg.supabase.co/storage/v1/object/public/image_search/src_images/{filename}"


def list_files() -> list[dict[str, str]]:
    return supabase_client.storage.from_(SUPABASE_BUCKET_ID).list(SUPABASE_FOLDER_NAME)
