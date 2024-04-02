import asyncio
import hashlib
import io
import reflex as rx

from ..template import template

from ..supabase_utils import upload_file
from ..vecs_utils import (
    add_embedding_to_index,
    image_to_embedding,
    refresh_index,
)

from ..navigation import QUERY_ROUTE, dashboard_sidebar, navbar
from ..styles import FONT_FAMILY


def search() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.icon_button(
                rx.icon(tag="paperclip", width=20, height=20),
                variant="ghost",
            ),
            rx.input.root(
                rx.input.input(
                    placeholder="Search",
                ),
                variant="soft",
            ),
            direction="row",
            gap="4",
            align="center",
        ),
        margin_top="calc(50px + 2em)",
        padding="2em",
    )


@rx.page(route=QUERY_ROUTE)
@template
def query():
    return search()
