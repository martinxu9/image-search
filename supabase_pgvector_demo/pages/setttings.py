import asyncio
import hashlib
import io
import reflex as rx

import reflex.components.radix.themes as rdxt
import reflex.components.radix.primitives as rdxp

from ..supabase_utils import upload_file
from ..vecs_utils import (
    add_embedding_to_index,
    image_to_embedding,
    refresh_index,
)

from ..navigation import dashboard_sidebar, navbar
from ..styles import FONT_FAMILY


class SettingState(rx.State):
    upload_files: list[str]
    indexed_files: list[str]

    # Whether we are currently uploading files.
    is_uploading: bool
    render_answers: bool

    query_results: str

    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle the file upload."""

        self.is_uploading = True

        # Iterate through the uploaded files.
        for file in files:
            upload_data = await file.read()
            emb = image_to_embedding(upload_data)
            image_id = hashlib.md5(upload_data).hexdigest()
            url = upload_file(filename=image_id, image_file=upload_data)
            add_embedding_to_index(id=image_id, embedding=emb, metadata={"url": url})

        refresh_index()

        return SettingState.stop_upload

    async def stop_upload(self):
        """Stop the file upload."""
        await asyncio.sleep(1)
        self.is_uploading = False

        return rx.clear_selected_files


def settings():
    return rdxt.box(
        dashboard_sidebar,
        rx.box(
            navbar(heading="Configuration"),
            rdxt.flex(
                # TODO: it was not easy to get the upload text+icon aligned correctly
                rx.upload(
                    rdxt.flex(
                        rdxt.text("Upload files", font_size="1.25em"),
                        rdxt.icon(tag="upload", height=25, width=25),
                        rdxt.flex(
                            rx.foreach(rx.selected_files, rdxt.text),
                            font_size="0.75em",
                            direction="column",
                            # TODO: when I used vstack here instead, it didn't align
                        ),
                        align="center",
                        direction="column",
                        gap="2",
                    ),
                    multiple=True,
                    # TODO: did not get the documentation, but example has it
                    # TODO: this rejects the invalid files silently
                    # TODO: what other types should be here?
                    accept={
                        "image/jpeg": [".jpg", ".jpeg"],
                        "image/png": [".png"],
                    },
                    max_files=5,
                    border="1px solid",
                    border_radius="1em",
                    # border_left="4px solid green",
                    padding="1em",
                ),
                rdxt.flex(
                    rdxt.button(
                        "Submit",
                        size="4",
                        width="8em",
                        on_click=SettingState.handle_upload(rx.upload_files()),  # type: ignore
                    ),
                    rdxt.button(
                        "Clear",
                        size="4",
                        width="8em",
                        on_click=rx.clear_selected_files,
                        variant="outline",
                    ),
                    rx.cond(
                        SettingState.is_uploading,
                        rx.progress(is_indeterminate=True, color="blue", width="100%"),
                    ),
                    gap="4",
                    direction="row",
                ),
                direction="column",
                gap="4",
                margin_top="calc(50px + 2em)",
                padding="2em",
            ),
            padding_left="250px",
        ),
        padding_bottom="4em",
        font_family=FONT_FAMILY,
    )
