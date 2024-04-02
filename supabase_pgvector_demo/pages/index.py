import reflex as rx

import reflex.components.radix.themes as rdxt
import reflex.components.radix.primitives as rdxp

from ..styles import FONT_FAMILY

from ..navigation import dashboard_sidebar, navbar


def index() -> rx.Component:
    return rdxt.box(
        dashboard_sidebar,
        rx.box(
            navbar(heading="Dashboard"),
            rx.box(
                # content_grid(),
                margin_top="calc(50px + 2em)",
                padding="2em",
            ),
            padding_left="250px",
        ),
        # rdxt.theme_panel(
        #     default_open=True,
        # ),
        padding_bottom="4em",
        font_family=FONT_FAMILY,
    )
    # return rx.fragment(
    #     rx.color_mode_button(rx.color_mode_icon(), float="right"),
    #     rx.hstack(
    #         rdxt.avatar(
    #             src="/logo.jpg", fallback="RX", width=50, height=50, float="left"
    #         ),
    #     ),
    #     rx.hstack(
    #         rx.vstack(
    #             rdxt.tooltip(
    #                 rdxt.icon(
    #                     tag="gear",
    #                     width=25,
    #                     height=25,
    #                     color="green",
    #                     margin="0.5em",
    #                 ),
    #                 content="Settings",
    #                 side="right",
    #             ),
    #             rdxt.icon(
    #                 tag="calendar",
    #                 width=25,
    #                 height=25,
    #                 color="green",
    #                 margin="0.5em",
    #             ),
    #             margin_top="0.5em",
    #             justify_content="stretch",
    #             width=30,
    #         ),
    #         # rx.vstack(
    #         #     rx.heading("Welcome to Reflex!", font_size="2em"),
    #         #     rx.box("Get started by editing ", rx.code(filename, font_size="1em")),
    #         #     rx.link(
    #         #         "Check out our docs!",
    #         #         href=docs_url,
    #         #         border="0.1em solid",
    #         #         padding="0.5em",
    #         #         border_radius="0.5em",
    #         #         _hover={
    #         #             "color": rx.color_mode_cond(
    #         #                 light="rgb(107,99,246)",
    #         #                 dark="rgb(179, 175, 255)",
    #         #             )
    #         #         },
    #         #     ),
    #         #     spacing="1.5em",
    #         #     font_size="2em",
    #         #     padding_top="10%",
    #         # ),
    #     ),
    # )
