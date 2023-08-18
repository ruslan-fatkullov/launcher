from flet import (
    UserControl,
    Column,
    Container,
    Row,
    Text,
    NavigationRail,
    NavigationRailDestination,
    alignment,
    border_radius,
    colors,
    icons,
    padding,
    margin,
)
import flet as ft
from flet_core import TextField

from data_store import DataStore


class Sidebar(UserControl):

    def __init__(self, app_layout, store: DataStore, page):
        super().__init__()

        self.view = None
        self.store: DataStore = store
        self.app_layout = app_layout
        self.page = page
        self.top_nav_items = [
            NavigationRailDestination(
                label_content=Text("Все группы"),
                label="Boards",
                icon=icons.FOLDER,
                selected_icon=icons.FOLDER_OPEN
            ),
        ]
        self.top_nav_rail = NavigationRail(
            selected_index=None,
            label_type="all",
            on_change=self.top_nav_change,
            destinations=self.top_nav_items,
            bgcolor=colors.GREY_200,
            extended=True,
            height=55
        )
        self.bottom_nav_rail = NavigationRail(
            selected_index=None,
            label_type="all",
            on_change=self.bottom_nav_change,
            extended=True,
            expand=True,
            bgcolor=colors.GREY_200,
        )

    def build(self):
        self.view = Container(
            content=Column([
                Row([
                    Text("Workspace"),
                ]),
                # divider
                Container(
                    bgcolor=colors.BLACK26,
                    border_radius=border_radius.all(30),
                    height=1,
                    alignment=alignment.center_right,
                    width=220
                ),
                self.top_nav_rail,
                # divider
                Container(
                    bgcolor=colors.BLACK26,
                    border_radius=border_radius.all(30),
                    height=1,
                    alignment=alignment.center_right,
                    width=220
                ),
                self.bottom_nav_rail
            ], tight=True),
            padding=padding.all(15),
            margin=margin.all(0),
            width=250,
            bgcolor=colors.GREY_200,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=15,
                color=ft.colors.BLACK,
                offset=ft.Offset(0, 0),
                blur_style=ft.ShadowBlurStyle.OUTER
            )
        )
        return self.view

    def sync_board_destinations(self):
        boards = self.store.get_boards()
        self.bottom_nav_rail.destinations = []
        for i in range(len(boards)):
            b = boards[i]
            self.bottom_nav_rail.destinations.append(
                NavigationRailDestination(
                    label_content=TextField(
                        value=b.board_name,
                        hint_text=b.board_name,
                        text_size=12,
                        read_only=True,
                        # on_focus=self.board_name_focus,
                        # on_blur=self.board_name_blur,
                        border="none",
                        height=50,
                        width=150,
                        text_align="start",
                        data=i
                    ),
                    label=b.board_name,
                    selected_icon=icons.CHEVRON_RIGHT_ROUNDED,
                    icon=icons.ARROW_RIGHT
                )
            )
        self.view.update()

    def top_nav_change(self, e):
        index = e if (type(e) == int) else e.control.selected_index
        self.bottom_nav_rail.selected_index = None
        self.top_nav_rail.selected_index = index
        self.view.update()
        if index == 0:
            e.page.route = "/boards"
        e.page.update()

    def bottom_nav_change(self, e):
        index = e if (type(e) == int) else e.control.selected_index
        self.top_nav_rail.selected_index = None
        self.bottom_nav_rail.selected_index = index
        e.page.route = f"/board/{index}"
        self.view.update()
        e.page.update()

    # def board_link(self, e, page):
    #     index = e if (type(e) == int) else e.control.selected_index
    #     self.top_nav_rail.selected_index = None
    #     self.bottom_nav_rail.selected_index = index
    #     page.route = f"/board/{index}"
    #     self.view.update()
    #     page.update()