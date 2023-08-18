import itertools
from flet import (
    UserControl,
    Column,
    Row,
    FloatingActionButton,
    ElevatedButton,
    Text,
    GridView,
    TextField,
    AlertDialog,
    Container,
    icons,
    border_radius,
    border,
    colors,
    padding,
    alignment,
    margin,
    Page,
    FilePicker,
    FilePickerResultEvent
)
from board_list import BoardList
from data_store import DataStore


class Board(UserControl):
    id_counter = itertools.count()

    def __init__(self, app, store: DataStore, name: str, page: Page):
        super().__init__()
        self.page = page
        self.board_id = next(Board.id_counter)
        self.store: DataStore = store
        self.app = app
        self.board_name = name
        self.add_list_button = FloatingActionButton(
            icon=icons.ADD, text="add a list", height=30, on_click=self.create_list)

        self.board_lists = [
            self.add_list_button
        ]
        for l in self.store.get_lists_by_board(self.board_id):
            self.add_list(l)

        self.list_wrap = Row(
            self.board_lists,
            vertical_alignment="start",
            visible=True,
            scroll="auto",
            width=(page.width - 260),
            height=(page.height - 95)
        )

    def build(self):
        self.view = Container(
            content=Column(
                controls=[
                    self.list_wrap
                ],

                scroll="auto",
                expand=True
            ),
            data=self,
            margin=margin.all(0),
            padding=padding.only(top=10, right=0),
            height=self.page.height - 95
        )
        return self.view

    def resize(self, nav_rail_extended, width, height):
        self.list_wrap.width = (
                width - 310) if nav_rail_extended else (width - 50)
        self.view.height = height
        self.list_wrap.update()
        self.view.update()

    def create_list(self, e):

        def close_dlg(e):
            if (hasattr(e.control, "text") and not e.control.text == "Cancel") or (
                    type(e.control) is TextField and e.control.value != ""):
                new_list = BoardList(self, self.store, dialog_text.value)
                self.add_list(new_list)
            dialog.open = False
            self.page.update()
            self.update()

        def textfield_change(e):
            if dialog_text.value == "" or dialog_description.value == "":
                create_button.disabled = True
            else:
                create_button.disabled = False
            self.page.update()

        def on_dialog_result(e: FilePickerResultEvent):
            print("Selected files:", e.files)
            print("Selected file or directory:", e.path)

        dialog_text = TextField(label="Название лаунча",
                                on_submit=close_dlg, on_change=textfield_change)
        dialog_description = TextField(label="Описание лаунча",
                                       on_submit=close_dlg, on_change=textfield_change, multiline=True)
        file_picker = FilePicker(on_result=on_dialog_result)
        create_button = ElevatedButton(
            text="Создать", bgcolor=colors.BLUE_200, on_click=close_dlg, disabled=True)
        dialog = AlertDialog(
            title=Text("Новый лаунч"),
            content=Column([
                Container(content=dialog_text,
                          padding=padding.symmetric(horizontal=5)),
                Container(content=dialog_description,
                          padding=padding.symmetric(horizontal=5)),
                ElevatedButton("Выберете ссылку на запускаемый файл",
                               on_click=lambda _: file_picker.pick_files(allow_multiple=False)),
                Row([
                    ElevatedButton(
                        text="Закрыть", on_click=close_dlg),
                    create_button
                ], alignment="spaceBetween")
            ], tight=True, alignment="center"),

            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
        dialog_text.focus()

    def remove_list(self, list: BoardList, e):
        self.board_lists.remove(list)
        self.store.remove_list(self.board_id, list.board_list_id)
        self.update()

    def add_list(self, list: BoardList):
        self.board_lists.insert(-1, list)
        self.store.add_list(self.board_id, list)
