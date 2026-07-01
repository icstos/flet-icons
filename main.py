import flet as ft


@ft.component
def IconBrowser(icon_set, expand: bool = False, key_prefix: str | None = None):
    results, set_results = ft.use_state([])
    search_term, set_search_term = ft.use_state("")

    search_icon = icon_set.SEARCH if hasattr(icon_set, "SEARCH") else ft.Icons.SEARCH

    def do_search(st: str | None = None):
        if st is None:
            st = search_term
        icons_list = list(icon_set)
        search_upper = st.upper()
        show_all = st == "*"
        new_results = []

        for icon in icons_list:
            icon_name = icon.name
            icon_key = f"ft.{icon.__class__.__name__}.{icon_name}"
            if show_all or search_upper in icon_name:
                new_results.append({"name": icon_name, "key": icon_key, "icon": icon})

        set_results(new_results)

    ft.on_mounted(lambda: do_search("*"))

    async def on_copy_icon(e):
        icon_key = e.control.data
        await ft.Clipboard().set(icon_key)
        e.page.show_dialog(ft.SnackBar(ft.Text(f"Copied: {icon_key}")))

    grid_controls = []
    for item in results[:100]:
        grid_controls.append(
            ft.Column(
                [
                    ft.IconButton(
                        icon=item["icon"],
                        icon_size=40,
                        tooltip=item["key"],
                        data=item["key"],
                        on_click=on_copy_icon,
                    ),
                    ft.Text(
                        item["name"],
                        size=10,
                        text_align=ft.TextAlign.CENTER,
                        no_wrap=True,
                        overflow=ft.TextOverflow.FADE,
                        width=100,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5,
            )
        )

    return ft.Container(
        expand=expand,
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.TextField(
                            expand=1,
                            hint_text="Enter keyword and press search button. To view all icons enter *",
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
                    runs_count=5,
                    max_extent=120,
                    child_aspect_ratio=1,
                    spacing=5,
                    run_spacing=5,
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
                            IconBrowser(
                                ft.Icons,
                                expand=True,
                                key_prefix="material",
                            ),
                            IconBrowser(
                                ft.CupertinoIcons,
                                expand=True,
                                key_prefix="cupertino",
                            ),
                        ],
                    ),
                ],
            ),
        ),
    )


if __name__ == "__main__":
    ft.run(lambda page: page.render(App))
