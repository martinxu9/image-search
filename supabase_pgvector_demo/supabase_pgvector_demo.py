"""Welcome to Reflex! This file outlines the steps to create a basic app."""

from rxconfig import config

import reflex as rx
import reflex.components.radix.themes as rdxt
import reflex.components.radix.primitives as rdxp

from .styles import STYLESHEETS

from .navigation import QUERY_ROUTE, SETTINGS_ROUTE
from .pages import index, settings, query


class State(rx.State):
    """The app state."""

    pass


# Create app instance and add index page.
app = rx.App(
    theme=rx.theme(
        appearance="dark",
        has_background=True,
        radius="large",
        accent_color="green",
        panel_background="translucent",
    ),
    stylesheets=STYLESHEETS,
)
app.add_page(index)
app.add_page(settings, route=SETTINGS_ROUTE)

