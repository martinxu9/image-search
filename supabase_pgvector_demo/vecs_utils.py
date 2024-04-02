import os
from pathlib import Path
from PIL import Image

from sentence_transformers import SentenceTransformer

import vecs
from vecs.collection import Record

model = SentenceTransformer("clip-ViT-B-32")

VECS_DB_URL = os.getenv("VECS_DB_URL", "")

vx = vecs.create_client(VECS_DB_URL)
collection = vx.get_or_create_collection(name="image_vectors", dimension=512)
# How often should we re-index?
# collection.create_index()


def image_to_embedding(image_bytes: bytes):
    return model.encode(Image.open(io.BytesIO(image_bytes)))


def add_embedding_to_index(id: str, embedding, metadata: dict):
    collection.upsert(
        records=[
            (
                id,
                embedding,
                metadata,
            ),
        ]
    )
    # TODO: do we need to refresh the index here?


def refresh_index():
    collection.create_index()


def search(query_text: str, max_results: int = 1) -> list[Record]:
    # query_text = "a bike in front of a red brick wall"
    text_emb = model.encode(query_text)

    # query the collection filtering metadata for "type" = "jpg"
    results = collection.query(
        data=text_emb,  # required
        limit=max_results,  # number of records to return
        filters={"type": {"$eq": "jpg"}},  # metadata filters
    )
    return results
