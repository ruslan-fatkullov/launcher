import itertools
from dataXML import DataXML
import uuid
import os
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
    Page,
    FilePicker,
    FilePickerResultEvent,
    Icon,
    ScrollMode,
    MainAxisAlignment,
)
from board_list import BoardList
from data_store import DataStore


# Изменяем картинку при создании, сохраняем в директории проекта и возвращаем на него ссылку
def generate_resized_image(image_path, launcher_id):
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
    image.save(f'./assets/resized_image/{launcher_id}.png')
    show_path = f'../launcher/assets/resized_image/{launcher_id}.png'
    return show_path


class Board(UserControl):
    id_counter = itertools.count()

    def __init__(self, app, store: DataStore, unique_id: str, name: str, page: Page, dataXML: DataXML):
        super().__init__()
        self.view = None
        self.page = page
        self.board_id = next(Board.id_counter)
        self.store: DataStore = store
        self.dataXML = dataXML
        self.app = app
        self.unique_id = unique_id
        self.board_name = name

        self.add_list_button = FloatingActionButton(
            icon=icons.ADD, text="добавить новый", height=30, on_click=self.create_list)

        self.board_lists = [
            self.add_list_button
        ]

        self.list_grid = GridView(
            expand=1,
            runs_count=5,
            max_extent=200,
            child_aspect_ratio=1.0,
            spacing=15,
            run_spacing=15,
            padding=padding.only(0, 10, 0, 0),
            width=1600#self.page.window_width - 290,
        )

        launch_list = self.dataXML.get_launch_by_board_name(self.unique_id)
        for item in launch_list:
            name = str(item.find('name').text)
            description = str(item.find('description').text)
            path = item.find('path').text
            image = str(item.find('image').text)
            new_list = BoardList(self, self.store, item.attrib.get('id'), name, description, path, image)
            self.add_list(new_list)

        self.list_grid.controls = self.board_lists
        # self.page.on_resize = self.resize
        # подумать
        # self.page.on_resize = self.app.setNewWidth(self)

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
            # border=border.all(1),
            # поменять тут
        )
        return self.view

    def create_list(self, e):
        def close_dlg(event):
            if (hasattr(event.control, "text") and not event.control.text == "Закрыть") or (
                    type(event.control) is TextField and event.control.value != ""):
                launch_id = str(uuid.uuid4())
                new_image_path = generate_resized_image(image_path.value, launch_id)
                self.dataXML.add_launch(self.unique_id, launch_id, launch_name.value, launch_description.value, file_path.value,
                                        new_image_path)
                new_list = BoardList(self, self.store, launch_id, launch_name.value, launch_description.value,
                                     file_path.value, new_image_path)
                self.add_list(new_list)
            dialog.open = False
            self.page.update()
            self.update()

        def textfield_change(e=None):
            if launch_name.value == "" or selected_files.value is None or selected_image.value is None:
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

        launch_name = TextField(label="Название лаунча",
                                on_submit=close_dlg, on_change=textfield_change)
        launch_description = TextField(label="Описание лаунча (необязательно)",
                                       on_submit=close_dlg, on_change=textfield_change, multiline=True, min_lines=6)

        create_button = ElevatedButton(
            text="Создать", bgcolor=colors.BLUE_200, on_click=close_dlg, disabled=True)
        dialog = AlertDialog(
            title=Text("Новый лаунч"),
            content=Column([
                Container(content=launch_name,
                          padding=padding.symmetric(horizontal=5)),
                Container(content=launch_description,
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
        launch_name.focus()

    def remove_list(self, launch):
        self.dataXML.remove_launch_item(self.unique_id, launch.launch_id)
        self.board_lists.remove(launch)
        self.store.remove_list(self.board_id, launch.board_list_id)
        self.update()

    def add_list(self, launch):
        self.board_lists.insert(-1, launch)
        self.store.add_list(self.board_id, launch)

    def edit_launch(self, launch: BoardList):
        def close_dlg(event):
            if (hasattr(event.control, "text") and not event.control.text == "Закрыть") or (
                    type(event.control) is TextField and event.control.value != ""):
                # os.remove(f"./assets/resized_image/{launch.launch_id}.png")
                new_image_path = generate_resized_image(image_path.value, launch.launch_id)
                self.dataXML.edit_launch_item(self.unique_id, launch.launch_id, launch_name.value, launch_description.value, file_path.value, new_image_path)
                launch.title = launch_name
                new_list = BoardList(self, self.store, launch.launch_id, launch_name.value, launch_description.value,
                                     file_path.value, new_image_path)
                self.board_lists.remove(launch)
                self.add_list(new_list)
            dialog.open = False
            self.page.update()
            self.update()
            launch.update()

        def textfield_change(e=None):
            if launch_name.value == "" or selected_files.value is None or selected_image.value is None:
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

        selected_files = Text(launch.file_path)
        selected_image = Text(launch.image_path)
        file_path = Text(launch.file_path)
        image_path = Text(launch.image_path)

        launch_name = TextField(label="Название лаунча",
                                on_submit=close_dlg, on_change=textfield_change, value=launch.title)
        descrip = launch.desc
        if launch.desc is None:
            descrip = ""
        launch_description = TextField(label="Описание лаунча (необязательно)",
                                       on_submit=close_dlg, on_change=textfield_change, multiline=True, min_lines=6, value=descrip)

        create_button = ElevatedButton(
            text="Сохранить", bgcolor=colors.BLUE_200, on_click=close_dlg, disabled=False)
        dialog = AlertDialog(
            title=Text("Редактирование"),
            content=Column([
                Container(content=launch_name,
                          padding=padding.symmetric(horizontal=5)),
                Container(content=launch_description,
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
        launch_name.focus()

    def resize(self, width, height):
        self.list_grid.width = width - 290
        self.list_grid.height = height - 95
        self.list_grid.update()
        self.view.update()
