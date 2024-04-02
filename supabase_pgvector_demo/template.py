from typing import Callable

import reflex as rx

from .styles import FONT_FAMILY
from .navigation import dashboard_sidebar, navbar


def template(page: Callable[[], rx.Component]) -> rx.Component:
    return rx.box(
        dashboard_sidebar,
        rx.box(
            navbar(heading="Query"),
            page(),
            padding_left="250px",
        ),
        padding_bottom="4em",
        font_family=FONT_FAMILY,
    )
