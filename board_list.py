import subprocess
from typing import TYPE_CHECKING
from math import pi

# from dataXML import DataXML
if TYPE_CHECKING:
    from board import Board
import itertools
from flet import (
    UserControl,
    Draggable,
    DragTarget,
    Row,
    ImageFit,
    Text,
    Icon,
    PopupMenuButton,
    PopupMenuItem,
    Container,
    TextButton,
    icons,
    border_radius,
    border,
    colors,
    padding,
    Image,
    TextThemeStyle,
    TextAlign,
    ButtonStyle,
    MaterialState,
    BoxShadow,
    Offset,
    ShadowBlurStyle,
    Stack,
    Column,
    Alignment,
    animation,
    transform,
    IconButton
)
from data_store import DataStore


class BoardList(UserControl):
    id_counter = itertools.count()

    def __init__(self, board: "Board", store: DataStore, launch_id: str, title: str, description: str = "",
                 file_path: str = "",
                 image_path: str = ""):
        super().__init__()
        self.my_header = None
        self.image = None
        self.view = None
        self.inner_list = None
        self.edit_field = None
        self.board_list_id = next(BoardList.id_counter)
        self.store: DataStore = store
        self.board = board
        self.launch_id = launch_id
        self.title = title
        self.desc = description
        self.file_path = file_path
        self.image_path = image_path
        self.title_view = Text(
            self.title,
            font_family="MyFont",
            size=19,
            color=colors.WHITE,
            top=15,
            left=15
        )
        self.title_container = Container(
            content=Stack([
                self.title_view,
                # self.popupmenu
            ]),
            padding=padding.all(5),
            bgcolor=colors.with_opacity(1, "#222c36"),
            animate_opacity=animation.Animation(duration=200),
            opacity=0,
            left=0,
            top=0,
            right=0,
            height=60
        )
        self.image = Image(
            src=self.image_path
        )
        self.launch_button = Container(
            content=TextButton(
                content=Row([Icon(icons.PLAY_ARROW), Text("Запуск", size=18, font_family="MyFont")]),
                on_click=self.play_launch,
                style=ButtonStyle(
                    color=colors.with_opacity(1, "#075667")
                )),
            bottom=0,
            left=0,
            right=0,
            height=60,
            bgcolor=colors.with_opacity(1, "#22afc0"),
            border_radius=border_radius.all(0),
            opacity=0,
            animate_opacity=animation.Animation(duration=150),

        )
        self.action_buttons = Container(
            content=Row([
                IconButton(icons.EDIT, bgcolor=colors.GREY_200, scale=0.9, on_click=self.edit_launch),
                IconButton(icons.COPY, bgcolor=colors.GREY_200, scale=0.9),
                IconButton(
                    icons.DELETE_OUTLINE,
                    bgcolor=colors.GREY_200,
                    scale=0.9,
                    on_click=self.delete_list,
                    style=ButtonStyle(
                        color=colors.RED,
                    )),
            ]),
            opacity=0,
            top=80,
            left=25,
            right=0,
            animate_opacity=animation.Animation(duration=150)
        )

    def tale_hover(self, e):

        if self.title_container.opacity == 1:
            self.title_container.opacity = 0
            self.inner_list.scale = 1
            self.launch_button.opacity = 0
            self.action_buttons.opacity = 0
        else:
            self.title_container.opacity = 1
            self.inner_list.scale = 1.05
            self.launch_button.opacity = 1
            self.action_buttons.opacity = 1
        self.launch_button.update()
        self.title_container.update()
        self.inner_list.update()

    def build(self):
        self.inner_list = Container(
            content=Stack([
                self.image,
                self.title_container,
                self.launch_button,
                self.action_buttons
            ]),
            on_hover=self.tale_hover,
            scale=1,
            animate_scale=animation.Animation(duration=150),
        )
        self.view = DragTarget(
            group="items",
            content=Draggable(
                group="lists",
                content=DragTarget(
                    group="lists",
                    content=self.inner_list,
                    data=self,
                    on_accept=self.list_drag_accept,
                    on_will_accept=self.list_will_drag_accept,
                    on_leave=self.list_drag_leave
                )
            ),
            data=self,
        )

        return self.view

    def list_drag_accept(self, e):
        src = self.page.get_control(e.src_id)
        i = self.board.board_lists
        to_index = i.index(e.control.data)
        from_index = i.index(src.content.data)
        i[to_index], i[from_index] = i[from_index], i[to_index]
        self.inner_list.border = border.all(2, colors.with_opacity(1, "#22afc0"))
        self.board.update()
        self.update()

    def list_will_drag_accept(self, e):
        if e.data == "true":
            self.inner_list.border = border.all(3, colors.with_opacity(1, "#22afc0"))
        self.update()

    def list_drag_leave(self, e):
        self.inner_list.border = border.all(0)
        self.update()

    def delete_list(self, e):
        self.board.remove_list(self)

    def edit_launch(self, e):
        self.board.edit_launch(self)

    def play_launch(self, e):
        subprocess.Popen(('start', "", self.file_path), shell=True)
