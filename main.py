import os.path
import uuid
import time

import flet
from flet import (
    app,
    AppBar,
    Container,
    Page,
    Row,
    TemplateRoute,
    Text,
    UserControl,
    View,
    colors,
    icons,
    margin,
    padding,
    theme,
    IconButton,
    Image,
)
from win32api import GetSystemMetrics

from app_layout import AppLayout
from board import Board
from dataXML import DataXML
from data_store import DataStore
from memory_store import InMemoryStore
from ui.create_board_dialog import CreateBoardDialog


class LauncherApp(UserControl):

    def __init__(self, page: Page, store: DataStore, dataXML: DataXML):
        self.boards = None
        super().__init__()
        self.layout = None
        self.store: DataStore = store
        self.page = page
        self.dataXML = dataXML
        self.page.on_route_change = self.route_change
        self.dataXML.get_groups()
        self.appbar_items = [
            IconButton(icon=icons.CLOSE)
        ]
        self.appbar = AppBar(
            leading=Image(src='assets/application_logo.png'),
            leading_width=300,
            title=Text(f"Лаунчер", font_family="MyFont", size=32),
            center_title=True,
            toolbar_height=105,
            bgcolor=colors.with_opacity(1, "#222c36"),
            color=colors.WHITE,
            actions=[
                Container(
                    content=Row([
                        IconButton(icon=icons.CHECK_BOX_OUTLINE_BLANK_SHARP, on_click=lambda e: page.window_minimized),
                        IconButton(icon=icons.CHECK_BOX_OUTLINE_BLANK_SHARP, on_click=lambda e: page.window_maximized),
                        IconButton(icon=icons.CLOSE, on_click=lambda e: page.window_close()),
                    ]),
                    margin=margin.only(left=50, right=25),
                )
            ],
        )
        self.page.appbar = self.appbar
        self.page.update()

    def build(self):
        self.layout = AppLayout(
            self,
            self.page,
            self.store,
            tight=True,
            expand=True,
            vertical_alignment="start",
        )
        return self.layout

    def initialize(self):

        for data_element in self.dataXML.root.findall("board"):
            self.create_new_board(data_element.get("id"), data_element.get("name"))

        self.boards = self.store.get_boards()
        self.page.views.clear()
        self.page.views.append(
            View(
                "/",
                [
                    self.appbar,
                    self.layout
                ],
                padding=padding.all(0),
                bgcolor=colors.BLUE_GREY_200,
            )
        )
        if len(self.boards) == 0:
            unique_id = uuid.uuid4()
            self.dataXML.add_group(unique_id, "Основная")
            self.create_new_board(unique_id, "Основная")
        self.page.go("/")

    def route_change(self, e):
        routing = TemplateRoute(e.page.route)
        if routing.match("/"):
            e.page.go("/boards")
        elif routing.match("/board/:id"):
            if int(routing.id) > len(self.store.get_boards()):
                self.page.go("/")
                return
            self.layout.set_board_view(e, int(routing.id))
        elif routing.match("/boards"):
            self.layout.set_all_boards_view(e.page)
        e.page.update()

    def add_board(self, e):
        dialog = CreateBoardDialog(self, self.dataXML)
        dialog.init_dialog(e.page)

    def create_new_board(self, unique_id, board_name):
        new_board = Board(self, self.store, unique_id, board_name, self.page, self.dataXML)
        self.store.add_board(new_board)
        self.layout.hydrate_all_boards_view()

    def delete_board(self, e):
        self.dataXML.remove_group(e.control.data.unique_id)
        self.store.remove_board(e.control.data)
        self.layout.set_all_boards_view(e.page)


def main(page: Page):
    page.title = "Лаунчер"
    page.theme_mode = flet.ThemeMode("light")
    # page.window_full_screen = True
    page.padding = 0

    page.theme = theme.Theme(font_family="Verdana")
    page.theme.page_transitions.windows = "cupertino"
    page.fonts = {"MyFont": "./fonts/20011.ttf"}
    page.window_width = GetSystemMetrics(0)
    page.window_height = GetSystemMetrics(1)
    page.window_maximized = True

    if not os.path.exists('assets'):
        os.mkdir('assets')
        os.mkdir('assets/resized_image')

    start = time.time()
    application = LauncherApp(page, InMemoryStore(), DataXML())
    page.add(application)
    page.update()
    application.initialize()
    end = time.time()
    print(end - start)


app(target=main, assets_dir="../assets")
