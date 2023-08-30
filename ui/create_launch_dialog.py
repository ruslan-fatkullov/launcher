""" класс диалогового окна для создания отдельных лаунчей """
import flet as ft
import uuid
from board_list import BoardList
from dataXML import DataXML
from data_store import DataStore


class CreateLaunchDialog:

    def __init__(self, board, dataXML: DataXML, store: DataStore):
        self.board = board
        self.dataXML = dataXML
        self.store = store

        self.file_picker = ft.FilePicker(on_result=self.on_pick_file_result)
        self.image_picker = ft.FilePicker(on_result=self.on_image_pick)

        self.selected_files = ft.Text()
        self.selected_image = ft.Text()

        self.file_path = ft.Text()
        self.image_path = ft.Text()

        self.launch_name = ft.TextField(label="Название лаунча",
                                        on_submit=self.close_dlg, on_change=self.textfield_change)
        self.launch_description = ft.TextField(label="Описание лаунча (необязательно)",
                                               on_submit=self.close_dlg, on_change=self.textfield_change,
                                               multiline=True, min_lines=6)

        self.create_button = ft.ElevatedButton(
            text="Создать", bgcolor=ft.colors.BLUE_200, on_click=self.close_dlg, disabled=True)

        self.dialog = ft.AlertDialog(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Row([
                            ft.Text("Новый лаунч", size=32),
                            ft.IconButton(ft.icons.CLOSE, on_click=self.close_dlg)
                        ]),
                        ft.Container(content=self.launch_name,
                                     padding=ft.padding.symmetric(horizontal=5)),
                        ft.Container(content=self.launch_description,
                                     padding=ft.padding.symmetric(horizontal=5)),
                        ft.Row([
                            ft.Icon(ft.icons.FILE_OPEN, color=ft.colors.BLUE_200),
                            ft.ElevatedButton("Выберете запускаемый файл",
                                              on_click=lambda _: self.file_picker.pick_files(allow_multiple=False)),
                            self.selected_files
                        ]),
                        self.file_picker,
                        ft.Row([
                            ft.Icon(ft.icons.IMAGE, color=ft.colors.BLUE_200),
                            ft.ElevatedButton("Выберете изображение",
                                              on_click=lambda _: self.image_picker.pick_files(allow_multiple=False)),
                            self.selected_image
                        ]),
                        self.image_picker,
                        ft.Row([
                            ft.ElevatedButton(
                                text="Закрыть", on_click=self.close_dlg),
                            self.create_button
                        ], alignment=ft.MainAxisAlignment("spaceBetween")),
                    ],
                    tight=True,
                    alignment=ft.MainAxisAlignment("center"),
                    spacing=10
                ),
                bgcolor=ft.colors.WHITE,
                padding=ft.padding.all(34)
            ),
            on_dismiss=lambda dismiss: print("Modal dialog dismissed!"),
            shape=ft.RoundedRectangleBorder(radius=0.0),
            content_padding=ft.padding.only(0, 0, 0, -30)
        )

    def init_create_launch_dialog(self, page):
        page.dialog = self.dialog
        self.dialog.open = True
        page.update()
        self.launch_name.focus()

    def close_dlg(self, event):
        if (hasattr(event.control, "text") and not event.control.text == "Закрыть") or (
                type(event.control) is ft.TextField and event.control.value != ""):
            launch_id = str(uuid.uuid4())
            new_image_path = self.board.generate_resized_image(self.image_path.value, launch_id)
            self.dataXML.add_launch(
                self.board.unique_id,
                launch_id,
                self.launch_name.value,
                self.launch_description.value,
                self.file_path.value,
                new_image_path
            )
            new_list = BoardList(
                self.board,
                self.store,
                launch_id,
                self.launch_name.value,
                self.launch_description.value,
                self.file_path.value, new_image_path
            )
            self.board.add_list(new_list)

        self.dialog.open = False
        self.board.update()
        event.page.update()

    def textfield_change(self, e=None):
        if self.launch_name.value == "" or self.selected_files.value is None or self.selected_image.value is None:
            self.create_button.disabled = True
        else:
            self.create_button.disabled = False
        self.dialog.update()

    def on_pick_file_result(self, fp: ft.FilePickerResultEvent):
        self.file_path.value = fp.files[0].path
        self.selected_files.value = (
            ", ".join(map(lambda f: f.name, fp.files)) if fp.files else "Cancelled!"
        )
        self.selected_files.update()
        self.textfield_change(None)

    def on_image_pick(self, fp: ft.FilePickerResultEvent):
        self.image_path.value = (
            fp.files[0].path
        )
        self.selected_image.value = (
            ", ".join(map(lambda f: f.name, fp.files)) if fp.files else "Cancelled!"
        )
        self.selected_image.update()
        self.textfield_change(None)
