from dataXML import DataXML
import flet as ft
from data_store import DataStore
import uuid
from board_list import BoardList


class CopyLaunchDialog:
    def __init__(self,board, launch, dataXML: DataXML, store: DataStore):
        self.view = None
        self.board = board
        self.launch = launch
        self.dataXML = dataXML
        self.store = store
        self.boards = store.get_boards()
        self.listing = ft.ListView(expand=1, auto_scroll=False)
        self.dialog_window = ft.AlertDialog(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Выберете директорию для копирования", font_family="MyFont", size=23),
                    self.listing
                ]),
                height=250,
                width=400,
            ),
            modal=False,
            on_dismiss=lambda dismiss: print("Modal dialog dismissed!"),
            shape=ft.RoundedRectangleBorder(radius=0.0),
        )

    def initialize_dialog(self, page):
        for i in self.boards:
            print(i.board_name)
            self.listing.controls.append(
                ft.TextButton(
                    content=ft.Row([
                        ft.Icon(ft.icons.FOLDER),
                        ft.Text(i.board_name, font_family="MyFont", size=18, width=380)
                    ]),
                    data=i,
                    on_click=self.copy_to_folder,
                ),
            )
        page.dialog = self.dialog_window
        self.dialog_window.open = True
        page.update()
        print("______________")

    def copy_to_folder(self, e):
        print(e.control.data.board_name)
        launch_id = str(uuid.uuid4())
        new_image_path = e.control.data.generate_resized_image(self.launch.image_path, launch_id)
        self.dataXML.add_launch(
            e.control.data.unique_id,
            launch_id,
            self.launch.title,
            self.launch.desc,
            self.launch.file_path,
            new_image_path
        )
        new_list = BoardList(
            e.control.data,
            self.store,
            launch_id,
            self.launch.title,
            self.launch.desc,
            self.launch.file_path,
            new_image_path
        )
        e.control.data.add_list(new_list)
        self.dialog_window.open = False
        self.board.update()
        e.page.snack_bar = ft.SnackBar(
            content=ft.Text("Плитка скопирована"),
            action="Ок",
            bgcolor=ft.colors.GREEN,
        )
        e.page.snack_bar.open = True
        e.page.update()
