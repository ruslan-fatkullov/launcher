import subprocess
from typing import TYPE_CHECKING

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
    Stack
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
        self.end_indicator = None
        self.edit_field = None
        self.board_list_id = next(BoardList.id_counter)
        self.store: DataStore = store
        self.board = board
        self.launch_id = launch_id
        self.title = title
        self.desc = description
        self.file_path = file_path
        self.image_path = image_path

    def build(self):
        self.end_indicator = Container(
            bgcolor=colors.BLACK26,
            border_radius=border_radius.all(0),
            height=3,
            width=200,
            opacity=0.0
        )
        self.my_header = Container(
            Stack(
                controls=[
                    Container(
                        content=Text(self.title, color=colors.with_opacity(1, "#ffffff")),
                        bgcolor=colors.with_opacity(1, "#075667"),
                        padding=padding.all(10),
                        border_radius=border_radius.all(5),
                        shadow=BoxShadow(
                            spread_radius=0,
                            blur_radius=5,
                            color=colors.BLACK26,
                            offset=Offset(5, 5),
                            blur_style=ShadowBlurStyle.NORMAL
                        )
                    ),
                    Container(
                        PopupMenuButton(
                            items=[
                                PopupMenuItem(
                                    content=Text(
                                        value="Редактировать",
                                        style=TextThemeStyle("labelMedium"),
                                        text_align=TextAlign("center"),
                                        color=colors.BLACK,
                                        bgcolor=colors.BLACK
                                    ),
                                    on_click=self.edit_launch,

                                ),
                                PopupMenuItem(),
                                PopupMenuItem(
                                    content=Text(
                                        value="Переместить в...",
                                        style=TextThemeStyle("labelMedium"),
                                        text_align=TextAlign("center"),
                                        color=colors.BLACK),),
                                PopupMenuItem(),
                                PopupMenuItem(
                                    content=Text(
                                        value="Копировать в...",
                                        style=TextThemeStyle("labelMedium"),
                                        text_align=TextAlign("center"),
                                        color=colors.BLACK),),
                                PopupMenuItem(),
                                PopupMenuItem(
                                    content=Text(
                                        value="Удалить",
                                        style=TextThemeStyle("labelMedium"),
                                        text_align=TextAlign("center"),
                                        color=colors.RED),
                                    on_click=self.delete_list),

                            ],

                        ),
                        right=0,
                        bgcolor=colors.WHITE,
                        border_radius=50,
                        shadow=BoxShadow(
                            spread_radius=0,
                            blur_radius=5,
                            color=colors.BLACK26,
                            offset=Offset(5, 5),
                            blur_style=ShadowBlurStyle.NORMAL
                        )
                    )

                ],
            ),
            top=15,
            left=10,
            right=10
        )
        self.inner_list = Container(
            content=Stack([
                Image(
                    src=self.image_path,
                    opacity=1,
                    fit=ImageFit.FILL,
                ),
                self.my_header,
                Container(
                    content=TextButton(
                        content=Row([Icon(icons.PLAY_ARROW), Text("Запуск")]),
                        on_click=self.play_launch,
                        style=ButtonStyle(
                            color={
                                MaterialState.HOVERED: colors.with_opacity(1, "#22afc0"),
                                MaterialState.DEFAULT: colors.with_opacity(1, "#075667")
                            },
                            bgcolor={
                                MaterialState.HOVERED: colors.with_opacity(1, "#075667"),
                                MaterialState.DEFAULT: colors.with_opacity(1, "#22afc0")
                            },
                        )),
                    bottom=10,
                    left=15,
                    shadow=BoxShadow(
                        spread_radius=0,
                        blur_radius=5,
                        color=colors.BLACK26,
                        offset=Offset(5, 5),
                        blur_style=ShadowBlurStyle.NORMAL
                    ),
                    border_radius=border_radius.all(0)
                )

            ]),
            shadow=BoxShadow(
                spread_radius=0,
                blur_radius=5,
                color=colors.BLACK26,
                offset=Offset(5, 5),
                blur_style=ShadowBlurStyle.NORMAL
            )
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
