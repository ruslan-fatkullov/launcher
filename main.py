from board import Board
from app_layout import AppLayout
import uuid
import win32api
from win32api import GetSystemMetrics
from flet import (
    app,
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
    IconButton,
    Image,
    MainAxisAlignment,
    AppView
)
from data_store import DataStore
from memory_store import InMemoryStore
from dataXML import DataXML


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
            title=Text(f"Лаунчер", font_family="Roboto", size=32),
            center_title=True,
            toolbar_height=105,
            bgcolor=colors.with_opacity(1, "#222c36"),
            color=colors.WHITE,
            actions=[
                Container(
                    content=Row([
                        IconButton(icon=icons.CHECK_BOX_OUTLINE_BLANK, on_click=lambda e: page.window_maximized),
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
        def close_dlg(event):
            if (hasattr(event.control, "text") and not event.control.text == "Закрыть") or (
                    type(event.control) is TextField and event.control.value != ""
            ):
                unique_id = uuid.uuid4()
                self.dataXML.add_group(unique_id, dialog_text.value)
                self.create_new_board(unique_id, dialog_text.value)
            dialog.open = False
            event.page.update()

        def textfield_change(event):
            if dialog_text.value == "":
                create_button.disabled = True
            else:
                create_button.disabled = False
            event.page.update()

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
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ],
                tight=True,
            ),
            on_dismiss=lambda dismiss: print("Modal dialog dismissed!"),
        )
        e.page.dialog = dialog
        dialog.open = True
        e.page.update()
        dialog_text.focus()

    def create_new_board(self, unique_id, board_name):
        new_board = Board(self, self.store, unique_id, board_name, self.page, self.dataXML)
        self.store.add_board(new_board)
        self.layout.hydrate_all_boards_view()

    def delete_board(self, e):
        self.dataXML.remove_group(e.control.data.unique_id)
        self.store.remove_board(e.control.data)
        self.layout.set_all_boards_view(e.page)

    # def setNewWidth(self, board):
    #     board.resize(self.page.window_width, self.page.window_height)


def main(page: Page):
    page.title = "Flet Launcher App"
    # page.window_frameless = True
    # page.window_resizable = True
    # page.window_full_screen = True
    page.padding = 0
    page.theme = theme.Theme(font_family="Verdana")
    page.theme.page_transitions.windows = "cupertino"
    page.fonts = {"Pacifico": "Pacifico-Regular.ttf"}
    page.window_width = 1233#GetSystemMetrics(0)
    page.window_height = 433#GetSystemMetrics(1)
    # page.window_maximized = True
    print(page.window_width)
    print(page.window_height)
    application = LauncherApp(page, InMemoryStore(), DataXML())
    page.add(application)
    page.update()
    application.initialize()


app(target=main, assets_dir="../assets")
