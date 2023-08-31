from board import Board
from flet import (
    Control,
    Column,
    Page,
    Row,
    Container,
    padding,
    TextButton,
    Icon,
    icons,
    ButtonStyle,
    IconButton,
    colors,
    RoundedRectangleBorder,
    Text,
    MainAxisAlignment,
    TextThemeStyle,
    TextAlign,
    PopupMenuButton,
    PopupMenuItem,
    alignment,
    border_radius,
    border,
    MaterialState
)
from data_store import DataStore
from Sidebar import Sidebar


class AppLayout(Row):

    def __init__(self, app, page: Page, store: DataStore, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.page = page
        self.page.on_resize = self.page_resize
        self.store: DataStore = store
        self.sidebar = Sidebar(self, store, page)
        self.all_boards_view = Column(
            [
                Row(
                    [
                        Container(
                            Text(
                                value="Все группы",
                                style=TextThemeStyle("headlineMedium"),
                                font_family="MyFont",
                                size=32
                            ),
                            expand=True,
                            padding=padding.only(top=15),
                        ),
                        Container(
                            IconButton(
                                content=Row([
                                    Icon(icons.ADD),
                                    Text(
                                        "Добавить",
                                        font_family="MyFont"
                                    )

                                ]),
                                on_click=self.app.add_board,
                                style=ButtonStyle(
                                    color={
                                        MaterialState.HOVERED: colors.with_opacity(1, "#22afc0"),
                                        MaterialState.DEFAULT: colors.with_opacity(1, "#075667")
                                    },
                                    bgcolor={
                                        MaterialState.HOVERED: colors.with_opacity(1, "#075667"),
                                        MaterialState.DEFAULT: colors.with_opacity(1, "#22afc0")
                                    },
                                    shape={"": RoundedRectangleBorder(radius=30)},
                                ),
                            ),
                            padding=padding.only(right=50, top=15),
                        ),
                    ]
                ),
                Row([Text("Нет групп")]),
            ],
            expand=True

        )

        self._active_view: Control = self.all_boards_view
        self.controls = [self.sidebar, self.active_view]

    @property
    def active_view(self):
        return self._active_view

    @active_view.setter
    def active_view(self, view):
        self._active_view = view
        self.controls[-1] = self._active_view
        self.sidebar.sync_board_destinations()
        # self.app.page.update()

    def hydrate_all_boards_view(self):
        self.all_boards_view.controls[-1] = Row(
            [
                Container(
                    content=Row(
                        [
                            Container(
                                content=Text(
                                    value=b.board_name,
                                    font_family="MyFont",
                                    size=20
                                ),
                                data=b,
                                expand=True,
                                padding=padding.only(left=10),
                                on_click=self.board_click,
                                height=150,
                                alignment=alignment.center
                            ),
                            Container(
                                content=PopupMenuButton(
                                    items=[
                                        PopupMenuItem(
                                            content=Text(
                                                value="Удалить",
                                                style=TextThemeStyle("labelMedium"),
                                                text_align=TextAlign("center"),
                                            ),
                                            on_click=self.app.delete_board,
                                            data=b,
                                        ),
                                    ]
                                ),
                                padding=padding.only(left=10),
                                border_radius=border_radius.all(3),
                            ),
                        ],
                        alignment=MainAxisAlignment("spaceBetween"),
                    ),
                    border=border.all(1, colors.BLACK38),
                    border_radius=border_radius.all(5),
                    bgcolor=colors.WHITE60,
                    padding=padding.all(10),
                    width=250,
                    height=150,
                    data=b,
                )
                for b in self.store.get_boards()
            ],
            wrap=True,
        )
        self.sidebar.sync_board_destinations()

    def board_click(self, e):
        self.sidebar.bottom_nav_change(e)
        self.page_resize(e)

    def set_all_boards_view(self, e):
        self.active_view = self.all_boards_view
        self.hydrate_all_boards_view()
        self.sidebar.top_nav_rail.selected_index = 0
        self.sidebar.bottom_nav_rail.selected_index = None
        e.update()

    def set_board_view(self, e, i):
        self.store.get_boards()[i].initialize_board(e.page.window_width)
        self.active_view = self.store.get_boards()[i]
        self.sidebar.bottom_nav_rail.selected_index = i
        self.sidebar.top_nav_rail.selected_index = None
        e.page.update()

    def page_resize(self, e=None):
        """тут проблема _active_view Column а не Board"""
        if type(self.active_view) is Board:
            self.active_view.resize(
                e.page.width, e.page.height
            )
        e.page.update()
