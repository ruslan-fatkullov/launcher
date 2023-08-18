import flet as ft
import os

from flet_core import colors
from PIL import Image


class SingleCart(ft.UserControl):

    def __init__(self, entity_name, entity_description="", entity_path="", image_path=""):
        super().__init__()
        self.entity_name = entity_name
        self.entity_description = entity_description
        self.entity_path = entity_path
        self.image_path = image_path
        self.image_opacity = 1

    def launch_entity(self, e):
        os.system(self.entity_path)

    def move_image_on_hover(self, e):
        e.control.opacity = 0.1 if e.data == "true" else 1
        e.control.update()

    def on_hover(self, e):
        e.control.opacity = 0.3 if e.data == "true" else self.image_opacity
        e.control.update()

    def build(self):
        try:
            image = Image.open(self.image_path)
            new_image = image.resize((300, 250))
            new_image = new_image.convert('RGB')
            new_image.save(f'./assets/resized_images/{self.entity_name}rs.jpg')
            show_path = f'./assets/resized_images/{self.entity_name}rs.jpg'
        except:
            image = Image.open('./assets/default.jpg')
            new_image = image.resize((300, 250))
            new_image = new_image.convert('RGB')
            new_image.save('./assets/resized_images/default.jpg')
            show_path = './assets/resized_images/default.jpg'
        return \
            ft.Container(
                ft.Stack([
                    ft.Container(
                        ft.Image(
                            src=show_path,
                            opacity=self.image_opacity,
                            fit=ft.ImageFit.CONTAIN,
                        ),
                        on_hover=self.move_image_on_hover,
                        top=0,
                        left=0,
                        right=0,
                    ),
                    ft.Row(
                        [
                            ft.Container(
                                ft.Text(
                                    self.entity_name,
                                    color="black",
                                    size=24,
                                    font_family="RobotoSlab",
                                    overflow=ft.TextOverflow.CLIP,
                                ),
                                bgcolor=colors.WHITE,
                                padding=ft.padding.only(left=15, top=5, right=15, bottom=5),
                                border_radius=5,
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        bottom=0,
                        left=0,
                        right=0,
                    ),
                ], ),
                bgcolor=ft.colors.with_opacity(1, '#222c36'),
                border_radius=3,
                on_hover=self.on_hover,
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=10,
                    color=ft.colors.BLACK,
                    offset=ft.Offset(0, 0),
                    blur_style=ft.ShadowBlurStyle.OUTER
                )
            )
