import itertools
from dataXML import DataXML
from PIL import Image as Im
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
    colors,
    padding,
    margin,
    Page,
    FilePicker,
    FilePickerResultEvent,
    Icon,
    ScrollMode,
    MainAxisAlignment
)
from board_list import BoardList
from data_store import DataStore


# Изменяем картинку при создании, сохраняем в директории проекта и возвращаем на него ссылку
def generate_resized_image(image_path, launcher_name):
    if image_path is None:
        image_path = "../launcher/assets/default.jpg"
    image = Im.open(image_path)
    width, height = image.size
    if width > height:
        difference = width - height
        top = 0
        bottom = height
        left = difference / 2
        right = left + height
        image = image.crop((int(left), int(top), int(right), int(bottom)))
    elif height > width:
        difference = height - width
        top = difference / 2
        bottom = top + width
        left = 0
        right = width
        image = image.crop((int(left), int(top), int(right), int(bottom)))
    image = image.resize((300, 300))
    image = image.convert('RGB')
    image.save(f'./assets/resized_image/{launcher_name}rs.png')
    show_path = f'../launcher/assets/resized_image/{launcher_name}rs.png'
    return show_path


class Board(UserControl):
    id_counter = itertools.count()

    def __init__(self, app, store: DataStore, name: str, page: Page, dataXML: DataXML):
        super().__init__()
        self.view = None
        self.page = page
        self.board_id = next(Board.id_counter)
        self.store: DataStore = store
        self.dataXML = dataXML
        self.app = app
        self.board_name = name
        self.add_list_button = FloatingActionButton(
            icon=icons.ADD, text="добавить новый", height=30, on_click=self.create_list)

        self.board_lists = [
            self.add_list_button
        ]

        self.list_grid = GridView(
            expand=1,
            runs_count=5,
            max_extent=250,
            child_aspect_ratio=1.0,
            spacing=15,
            run_spacing=15,
            padding=15,
            # тут поменять значения
            width=1900,
            height=800
        )

        launch_list = self.dataXML.get_launch_by_board_name(self.board_name)
        for item in launch_list:
            name = str(item.find('name').text)
            description = str(item.find('description').text)
            path = item.find('path').text
            image = str(item.find('image').text)
            new_list = BoardList(self, self.store, name, description, path, image)
            self.add_list(new_list)

        self.list_grid.controls = self.board_lists

    def build(self):
        self.view = Container(
            content=Column(
                controls=[
                    self.list_grid
                ],
                scroll=ScrollMode('auto'),
                expand=True
            ),
            data=self,
            margin=margin.all(0),
            padding=padding.only(top=10, right=0),
            # поменять тут
            height=730
        )
        return self.view

    def create_list(self, e):
        def close_dlg(event):
            if (hasattr(event.control, "text") and not event.control.text == "Закрыть") or (
                    type(event.control) is TextField and event.control.value != ""):
                new_image_path = generate_resized_image(image_path.value, dialog_text.value)
                self.dataXML.add_launch(self.board_name, dialog_text.value, dialog_description.value, file_path.value,
                                        new_image_path)
                new_list = BoardList(self, self.store, dialog_text.value, dialog_description.value,
                                     file_path.value, new_image_path)
                self.add_list(new_list)
            dialog.open = False
            self.page.update()
            self.update()

        def textfield_change(e=None):
            if dialog_text.value == "" or selected_files.value is None or selected_image.value is None:
                create_button.disabled = True
            else:
                create_button.disabled = False
            self.page.update()

        def on_pick_file_result(fp: FilePickerResultEvent):
            file_path.value = fp.files[0].path
            selected_files.value = (
                ", ".join(map(lambda f: f.name, fp.files)) if fp.files else "Cancelled!"
            )
            selected_files.update()
            textfield_change(None)

        def on_image_pick(fp: FilePickerResultEvent):
            image_path.value = (
                fp.files[0].path
            )
            selected_image.value = (
                ", ".join(map(lambda f: f.name, fp.files)) if fp.files else "Cancelled!"
            )
            selected_image.update()
            textfield_change(None)

        file_picker = FilePicker(on_result=on_pick_file_result)
        image_picker = FilePicker(on_result=on_image_pick)

        selected_files = Text()
        selected_image = Text()
        file_path = Text()
        image_path = Text()

        dialog_text = TextField(label="Название лаунча",
                                on_submit=close_dlg, on_change=textfield_change)
        dialog_description = TextField(label="Описание лаунча (необязательно)",
                                       on_submit=close_dlg, on_change=textfield_change, multiline=True, min_lines=6)

        create_button = ElevatedButton(
            text="Создать", bgcolor=colors.BLUE_200, on_click=close_dlg, disabled=True)
        dialog = AlertDialog(
            title=Text("Новый лаунч"),
            content=Column([
                Container(content=dialog_text,
                          padding=padding.symmetric(horizontal=5)),
                Container(content=dialog_description,
                          padding=padding.symmetric(horizontal=5)),
                Row([
                    Icon(icons.FILE_OPEN),
                    ElevatedButton("Выберете запускаемый файл",
                                   on_click=lambda _: file_picker.pick_files(allow_multiple=False)),
                    selected_files
                ]),
                file_picker,
                Row([
                    Icon(icons.IMAGE),
                    ElevatedButton("Выберете изображение",
                                   on_click=lambda _: image_picker.pick_files(allow_multiple=False)),
                    selected_image
                ]),
                image_picker,
                Row([
                    ElevatedButton(
                        text="Закрыть", on_click=close_dlg),
                    create_button
                ], alignment=MainAxisAlignment("spaceBetween")),
            ], tight=True, alignment=MainAxisAlignment("center")),
            on_dismiss=lambda dismiss: print("Modal dialog dismissed!"),
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
        dialog_text.focus()

    def remove_list(self, launch):
        self.dataXML.remove_launch_item(self.board_name, launch.title)
        self.board_lists.remove(launch)
        self.store.remove_list(self.board_id, launch.board_list_id)
        self.update()

    def add_list(self, launch):
        self.board_lists.insert(-1, launch)
        self.store.add_list(self.board_id, launch)

    def resize(self, page_width, page_height):
        self.list_grid.width = page_width - 260
        self.list_grid.height = page_height - 95
        self.list_grid.update()
        self.view.update()
