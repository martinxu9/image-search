"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import asyncio
import hashlib
import os
from datetime import datetime, timedelta
from rxconfig import config
from rx_carousel.carousel import carousel

import reflex as rx


from .supabase_utils import fixed_public_url, get_url, list_files, upload_file
from .vecs_utils import (
    search as vecs_search,
    add_embedding_to_index,
    image_to_embedding,
)

MAX_FILES_TO_UPLOAD = int(os.getenv("MAX_FILES_TO_UPLOAD", 10))
MAX_FILES_TO_BROWSE = int(os.getenv("MAX_FILES_TO_BROWSE", 20))
MAX_FILES_TO_QUERY = int(os.getenv("MAX_FILES_TO_QUERY", 3))


class State(rx.State):
    """The app state."""

    upload_files: list[str]
    indexed_files: list[str]

    # Whether we are currently uploading files.
    is_uploading: bool
    render_answers: bool

    query_results: list[str]

    @rx.var
    def browse_results(self) -> list[str]:
        files_in_bucket = list_files()
        files_in_bucket.sort(
            key=lambda f: (
                datetime.fromisoformat(f["updated_at"])
                if f.get("updated_at")
                else datetime(2023, 8, 16)
            ),
            reverse=True,
        )
        # print(files_in_bucket)
        files_to_display = [
            fixed_public_url(f["name"])
            for f in files_in_bucket[-MAX_FILES_TO_BROWSE:-1]
            if f.get("name")
        ]
        print(files_to_display)
        return files_to_display

    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle the file upload."""

        self.is_uploading = True

        # Iterate through the uploaded files.
        for file in files:
            upload_data = await file.read()
            emb = image_to_embedding(upload_data)
            image_id = hashlib.md5(upload_data).hexdigest()
            extension = (file.filename or "").split(".")[-1]
            new_filename = f"{image_id}.{extension}"
            url = upload_file(filename=new_filename, image_file=upload_data)
            add_embedding_to_index(
                id=new_filename, embedding=emb, metadata={"url": url}
            )

        return State.stop_upload

    async def stop_upload(self):
        """Stop the file upload."""
        await asyncio.sleep(1)
        self.is_uploading = False

        return rx.clear_selected_files

    def handle_search_submit(self, data: dict):
        """Handle the search form submission."""
        # print(f"Search term: {data['search_term']}")
        results = vecs_search(data["search_term"], max_results=MAX_FILES_TO_QUERY)
        self.query_results = []
        yield
        for filename in results:
            if signed_url := get_url(filename):
                print(signed_url)
                self.query_results.append(signed_url)


def browse() -> rx.Component:
    return rx.vstack(
        rx.el.em(f"Last uploaded {MAX_FILES_TO_BROWSE} images"),
        carousel(
            rx.foreach(
                State.browse_results,
                lambda src: rx.image(
                    src=src,
                    max_height="360px",
                    class_name="object-contain",
                ),
            ),
        ),
        align="center",
        height="400px",
        width="800px",
        padding="2em",
    )


def search_box() -> rx.Component:
    return rx.box(
        rx.form(
            rx.hstack(
                rx.input.root(
                    rx.input.input(
                        placeholder="Search",
                        name="search_term",
                        size="3",
                        width="30em",
                    ),
                ),
                rx.button("Go", type="submit", variant="soft", size="3"),
                spacing="4",
                align="center",
            ),
            on_submit=State.handle_search_submit,
        ),
    )


def search() -> rx.Component:
    return rx.vstack(
        search_box(),
        rx.cond(
            rx.text(f"Top {MAX_FILES_TO_QUERY} results:"),
            carousel(
                rx.foreach(
                    State.query_results,  # type: ignore
                    lambda url: rx.image(
                        src=url, max_height="360px", class_name="object-contain"
                    ),
                ),
            ),
        ),
        spacing="2",
        align="center",
        height="400px",
        width="800px",
        padding="1em",
    )


def upload() -> rx.Component:
    return rx.vstack(
        rx.text(
            "Accepted image types: jpg/jpeg, png, webp, avif.",
        ),
        rx.text(f"Max {MAX_FILES_TO_UPLOAD} files."),
        rx.upload(
            rx.vstack(
                rx.text("Upload files", font_size="1.25em"),
                rx.icon(tag="upload", height=25, width=25),
                rx.vstack(
                    rx.foreach(rx.selected_files, rx.text),
                    font_size="0.75em",
                ),
                align="center",
                spacing="2",
            ),
            multiple=True,
            accept={
                "image/jpeg": [".jpg", ".jpeg"],
                "image/png": [".png"],
                "image/avif": [".avif"],
                "image/webp": [".webp"],
            },
            max_files=MAX_FILES_TO_UPLOAD,
            border="1px solid",
            border_radius="1em",
            width="400px",
            padding="1em",
        ),
        rx.cond(
            State.is_uploading,
            rx.chakra.progress(
                is_indeterminate=True,
                width="400px",
            ),
        ),
        rx.hstack(
            rx.button(
                "Submit",
                size="3",
                width="8em",
                variant="soft",
                on_click=State.handle_upload(rx.upload_files()),  # type: ignore
            ),
            rx.button(
                "Clear",
                size="3",
                width="8em",
                on_click=rx.clear_selected_files,
                variant="outline",
            ),
            spacing="4",
        ),
        spacing="4",
        padding="2em",
        align="center",
        height="400px",
        width="800px",
    )


def tab_heading(heading: str) -> rx.Component:
    return rx.tabs.trigger(
        rx.text(
            heading.capitalize(),
            color="green",
            size="6",
            padding_x="2em",
            # padding_y="0.5em",
        ),
        value=heading,
    )


def index() -> rx.Component:
    return rx.center(
        # rx.theme_panel(),
        rx.vstack(
            rx.heading("Image Search", size="9"),
            rx.text("Powered by Supabase+pgvector, Reflex, CLIP by OpenAI"),
            rx.tabs.root(
                rx.hstack(
                    rx.tabs.list(
                        tab_heading("search"),
                        tab_heading("upload"),
                        tab_heading("browse"),
                    ),
                    align="stretch",
                    justify="center",
                    padding="1em",
                    width="800px",
                ),
                rx.tabs.content(
                    search(),
                    value="search",
                ),
                rx.tabs.content(
                    upload(),
                    value="upload",
                ),
                rx.tabs.content(
                    browse(),
                    value="browse",
                ),
                default_value="search",
                orientation="vertical",
            ),
            rx.text(
                "Images from ",
                rx.link(
                    "https://unsplash.com/license", href="https://unsplash.com/license"
                ),
                " via ",
                rx.link("https://picsum.photos/", href="https://picsum.photos/"),
                size="1",
                margin_top="5em",
            ),
            align="center",
            spacing="3",
        ),
        height="100vh",
    )


app = rx.App(
    theme=rx.theme(
        appearance="dark", has_background=True, radius="large", accent_color="green"
    ),
)
app.add_page(index, title="CLIP x Supabase pgvector | Reflex")
