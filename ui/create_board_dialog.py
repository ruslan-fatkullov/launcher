import flet as ft
import uuid
from dataXML import DataXML


class CreateBoardDialog:
    def __init__(self, app, dataXML: DataXML):
        self.dataXML = dataXML
        self.app = app
        self.dialog_text = ft.TextField(
            label="Название группы",
            on_submit=self.close_dlg,
            on_change=self.textfield_change,
            border=ft.InputBorder.NONE,
            filled=True
        )
        self.create_button = ft.ElevatedButton(
            text="Создать", bgcolor=ft.colors.BLUE_200, on_click=self.close_dlg, disabled=True
        )
        self.dialog = ft.AlertDialog(
            content_padding=ft.Padding(
                top=-10,
                bottom=-30,
                left=0,
                right=0
            ),
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text("Введите название", size=24, font_family="MyFont"),
                                ft.IconButton(
                                    ft.icons.CLOSE,
                                    on_click=self.close_dlg,
                                    style=ft.ButtonStyle(
                                        color={
                                            ft.MaterialState.HOVERED: ft.colors.with_opacity(1, "#22afc0"),
                                            ft.MaterialState.DEFAULT: ft.colors.with_opacity(1, "#075667")
                                        },
                                        bgcolor={
                                            ft.MaterialState.HOVERED: ft.colors.with_opacity(1, "#075667"),
                                            ft.MaterialState.DEFAULT: ft.colors.with_opacity(1, "#ffffff")
                                        },
                                    ),
                                )
                            ],
                            alignment=ft.alignment.center_right
                        ),
                        self.dialog_text,
                        ft.Row(
                            [
                                ft.ElevatedButton(text="Закрыть", on_click=self.close_dlg),
                                self.create_button,
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                    ],
                    spacing=30,
                    tight=True,
                ),
                bgcolor=ft.colors.with_opacity(1, "#ffffff"),
                padding=ft.padding.all(24),
                width=400
            ),
            on_dismiss=lambda dismiss: print("Modal dialog dismissed!"),
            shape=ft.RoundedRectangleBorder(radius=0.0),
        )

    def init_dialog(self, page):
        page.dialog = self.dialog
        self.dialog.open = True
        page.update()
        self.dialog_text.focus()

    def close_dlg(self, event):
        if (hasattr(event.control, "text") and not event.control.text == "Закрыть") or (
                type(event.control) is ft.TextField and event.control.value != ""
        ):
            unique_id = uuid.uuid4()
            self.dataXML.add_group(unique_id, self.dialog_text.value)
            self.app.create_new_board(unique_id, self.dialog_text.value)
        self.dialog.open = False
        event.page.update()

    def textfield_change(self, event):
        if self.dialog_text.value == "":
            self.create_button.disabled = True
        else:
            self.create_button.disabled = False
        event.page.update()
