import flet
import self as self
from board import Board

from app_layout import AppLayout
from flet import (
    AlertDialog,
    AppBar,
    Column,
    Container,
    ElevatedButton,
    Page,
    Row,
    TemplateRoute,
    Text,
    TextField,
    UserControl,
    View,
    colors,
    icons,
    margin,
    padding,
    theme,
)
from data_store import DataStore
from memory_store import InMemoryStore


class LauncherApp(UserControl):
    def __init__(self, page: Page, store: DataStore):
        super().__init__()
        self.store: DataStore = store
        self.page = page
        self.page.on_route_change = self.route_change
        self.boards = self.store.get_boards()

        self.appbar_items = [
            flet.IconButton(icon=icons.CLOSE)
        ]
        self.appbar = AppBar(
            leading=flet.Image(src='./assets/esvologo.png'),
            leading_width=300,
            title=Text(f"Лаунчер", font_family="Roboto", size=32),
            center_title=True,
            toolbar_height=105,
            bgcolor=colors.with_opacity(1, "#222c36"),
            color=colors.WHITE,
            actions=[
                Container(
                    content=flet.Row([
                        flet.IconButton(icon=icons.CHECK_BOX_OUTLINE_BLANK, on_click=lambda e: page.window_maximized),
                        flet.IconButton(icon=icons.CLOSE, on_click=lambda e: page.window_close()),
                        # flet.IconButton(icon=icons.ADD, on_click=self.add_board),
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
        self.page.update()
        # if len(self.boards) == 0:
        #     self.create_new_board("My First Board")
        # self.page.go("/")

    def route_change(self, e):
        troute = TemplateRoute(e.page.route)
        if troute.match("/"):
            e.page.go("/boards")
        elif troute.match("/board/:id"):
            if int(troute.id) > len(self.store.get_boards()):
                self.page.go("/")
                return
            self.layout.set_board_view(int(troute.id))
        elif troute.match("/boards"):
            self.layout.set_all_boards_view()
        e.page.update()

    def add_board(self, e):
        def close_dlg(e):
            if (hasattr(e.control, "text") and not e.control.text == "Cancel") or (
                    type(e.control) is TextField and e.control.value != ""
            ):
                self.create_new_board(dialog_text.value, e.page)
            dialog.open = False
            e.page.update()

        def textfield_change(e):
            if dialog_text.value == "":
                create_button.disabled = True
            else:
                create_button.disabled = False
            e.page.update()

        dialog_text = TextField(
            label="Название группы", on_submit=close_dlg, on_change=textfield_change
        )
        create_button = ElevatedButton(
            text="Создать", bgcolor=colors.BLUE_200, on_click=close_dlg, disabled=True
        )
        dialog = AlertDialog(
            title=Text("Введите название для вашей группы"),
            content=Column(
                [
                    dialog_text,
                    Row(
                        [
                            ElevatedButton(text="Закрыть", on_click=close_dlg),
                            create_button,
                        ],
                        alignment="spaceBetween",
                    ),
                ],
                tight=True,
            ),
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        e.page.dialog = dialog
        dialog.open = True
        e.page.update()
        dialog_text.focus()

    def create_new_board(self, board_name, page):
        new_board = Board(self, self.store, board_name, page)
        self.store.add_board(new_board)
        self.layout.hydrate_all_boards_view()

    def delete_board(self, e):
        self.store.remove_board(e.control.data)
        self.layout.set_all_boards_view()


def main(page: flet.Page):
    page.title = "Flet Launcher App"
    # page.window_frameless = True
    # page.window_resizable = True
    # page.window_full_screen = True

    page.padding = 0
    page.theme = theme.Theme(font_family="Verdana")
    page.theme.page_transitions.windows = "cupertino"
    page.fonts = {"Pacifico": "Pacifico-Regular.ttf"}
    page.bgcolor = colors.BLUE_GREY_200
    app = LauncherApp(page, InMemoryStore())
    page.add(app)
    page.update()
    app.initialize()


flet.app(target=main, assets_dir="../assets")
