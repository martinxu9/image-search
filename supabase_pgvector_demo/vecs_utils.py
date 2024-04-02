import io
import os
from PIL import Image

from sentence_transformers import SentenceTransformer

import vecs

model = SentenceTransformer("clip-ViT-B-32")

VECS_DB_URL = os.getenv("VECS_DB_URL", "")

vx = vecs.create_client(VECS_DB_URL)
collection = vx.get_or_create_collection(name="image_vectors", dimension=512)
collection.create_index()


def image_to_embedding(image_bytes: bytes):
    return model.encode(Image.open(io.BytesIO(image_bytes)))  # type: ignore


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


def search(query_text: str, max_results: int = 1) -> list[str]:
    # query_text = "a bike in front of a red brick wall"
    text_emb = model.encode(query_text)

    # query the collection filtering metadata for "type" = "jpg"
    results = collection.query(
        data=text_emb,  # required
        limit=max_results,  # number of records to return
        # filters={"type": {"$eq": "jpg"}},  # metadata filters
    )
    return [res[0] if not isinstance(res, str) else res for res in results]
