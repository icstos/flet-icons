import flet as ft
from dataclasses import dataclass


MAX_RESULTS = 100
ICON_SIZE = 40
TEXT_SIZE = 10
TEXT_WIDTH = 100
GRID_RUNS_COUNT = 5
GRID_MAX_EXTENT = 120
GRID_SPACING = 5
SEARCH_HINT = "Enter keyword and press search button. To view all icons enter *"


@dataclass
class IconResult:
    name: str
    key: str
    icon: ft.IconData


@ft.component
def IconBrowser(icon_set, expand: bool = False):
    results, set_results = ft.use_state([])
    search_term, set_search_term = ft.use_state("")

    search_icon = icon_set.SEARCH if hasattr(icon_set, "SEARCH") else ft.Icons.SEARCH

    def do_search(st: str | None = None):
        if st is None:
            st = search_term
        search_upper = st.upper()
        show_all = st == "*"

        new_results = [
            IconResult(
                name=icon.name,
                key=f"ft.{icon.__class__.__name__}.{icon.name}",
                icon=icon,
            )
            for icon in icon_set
            if show_all or search_upper in icon.name
        ]
        set_results(new_results)

    ft.on_mounted(lambda: do_search("*"))

    async def on_copy_icon(e):
        icon_key = e.control.data
        await ft.Clipboard().set(icon_key)
        e.page.show_dialog(ft.SnackBar(ft.Text(f"Copied: {icon_key}")))

    grid_controls = [
        ft.Column(
            [
                ft.IconButton(
                    icon=item.icon,
                    icon_size=ICON_SIZE,
                    tooltip=item.key,
                    data=item.key,
                    on_click=on_copy_icon,
                ),
                ft.Text(
                    item.name,
                    size=TEXT_SIZE,
                    text_align=ft.TextAlign.CENTER,
                    no_wrap=True,
                    overflow=ft.TextOverflow.FADE,
                    width=TEXT_WIDTH,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=GRID_SPACING,
        )
        for item in results[:MAX_RESULTS]
    ]

    return ft.Container(
        expand=expand,
        content=ft.Column(
            controls=[
                ft.Row(
                    [
                        ft.TextField(
                            expand=1,
                            hint_text=SEARCH_HINT,
                            autofocus=True,
                            value=search_term,
                            on_change=lambda e: set_search_term(e.control.value),
                            on_submit=lambda e: do_search(),
                        ),
                        ft.IconButton(
                            icon=search_icon,
                            tooltip="Search",
                            on_click=lambda e: do_search(),
                        ),
                    ],
                    spacing=10,
                ),
                ft.GridView(
                    expand=1,
                    runs_count=GRID_RUNS_COUNT,
                    max_extent=GRID_MAX_EXTENT,
                    child_aspect_ratio=1,
                    spacing=GRID_SPACING,
                    run_spacing=GRID_SPACING,
                    controls=grid_controls,
                ),
                ft.Text(f"Icons found: {len(results)}"),
            ],
            expand=True,
            spacing=10,
        ),
    )


@ft.component
def App():
    ft.context.page.title = "Flet icons browser"
    ft.context.page.theme_mode = ft.ThemeMode.LIGHT
    ft.context.page.padding = 20

    return ft.SafeArea(
        expand=True,
        content=ft.Tabs(
            selected_index=0,
            length=2,
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.TabBar(
                        tabs=[
                            ft.Tab(label="Material"),
                            ft.Tab(label="Cupertino"),
                        ]
                    ),
                    ft.TabBarView(
                        expand=True,
                        controls=[
                            IconBrowser(ft.Icons, expand=True),
                            IconBrowser(ft.CupertinoIcons, expand=True),
                        ],
                    ),
                ],
            ),
        ),
    )


if __name__ == "__main__":
    ft.run(lambda page: page.render(App))
