import reflex as rx

from .styles import FONT_FAMILY


def sidebar_link(text: str, href: str, icon: str) -> rx.Link:
    return rx.link(
        rx.flex(
            rx.tooltip(
                rx.icon(tag=icon, width=25, height=25, margin="12px"),
                content=text,
                side="right",
                side_offset=15,
                z_index="10",
            ),
            py="2",
            px="4",
            gap="4",
            align="baseline",
            direction="row",
            # font_family=FONT_FAMILY,
        ),
        href=href,
        width="100%",
        border_radius="12px",
        _hover={
            "background": "rgba(255, 255, 255, 0.1)",
            "backdrop_filter": "blur(10px)",
        },
    )


def sidebar(
    *sidebar_links,
    **props,
) -> rx.Component:
    logo_src = props.get("logo_src", "/logo.jpg")
    return rx.vstack(
        rx.hstack(
            rx.image(src=logo_src),
            width="70%",
        ),
        rx.separator(),
        rx.vstack(
            *sidebar_links,
            padding_y="1em",
        ),
        width="120px",
        position="fixed",
        height="100%",
        left="0px",
        top="0px",
        align_items="center",
        z_index="10",
        backdrop_filter="blur(10px)",
        padding="2em",
    )


SETTINGS_ROUTE = "/settings"
QUERY_ROUTE = "/query"

dashboard_sidebar = sidebar(
    sidebar_link(text="Home", href="/", icon="home"),
    sidebar_link(text="Query", href=QUERY_ROUTE, icon="command"),
    sidebar_link(text="Settings", href=SETTINGS_ROUTE, icon="settings"),
    logo_src="/supabase-logo-icon.svg",
)


def navbar(heading: str) -> rx.Component:
    return rx.hstack(
        rx.heading(heading, font_family=FONT_FAMILY, size="7"),
        rx.spacer(),
        rx.dropdownmenu_root(
            rx.dropdownmenu_trigger(
                rx.button(
                    "Menu",
                    rx.icon(tag="chevron_down", weight=16, height=16),
                    variant="soft",
                ),
            ),
            rx.dropdownmenu_content(
                rx.dropdownmenu_item(
                    "Logout",
                    color_scheme="green",
                ),
                variant="soft",
            ),
        ),
        position="fixed",
        width="calc(100% - 250px)",
        top="0px",
        z_index="1000",
        padding_x="2em",
        padding_top="2em",
        padding_bottom="1em",
        backdrop_filter="blur(10px)",
    )
