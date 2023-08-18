import random

import flet
import flet as ft
import SingleCart


class SingleCartList(ft.UserControl):

    def __init__(self, app_layout, page, list_width):
        super().__init__()
        self.view = None
        self.list_width = list_width
        self.cart_width = 200,
        self.app_layout = app_layout
        self.page = page
        self.page.on_resize = self.resize_page

        self.create_new_singlecart = ft.TextButton(content=ft.Row([ft.Icon(ft.icons.PLUS_ONE), ft.Text("Create")]), on_click=self.open_dlg)
        self.images = ft.GridView(
            expand=1,
            runs_count=5,
            max_extent=250,
            child_aspect_ratio=1.0,
            spacing=15,
            run_spacing=15,
            width=self.list_width,
            padding=15
        )
        for i in range(0, 30):
            self.images.controls.append(
                SingleCart.SingleCart(f"АОС 76МД{i}", "Это описание",
                                      "C:\\Users\\fatkullov_ra\\Desktop\\test.txt",
                                      f"./assets/frodo{i % 5}.png")
            )


        self.dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Создайте лаунч"),
            content=ft.Text("Do you really want to delete all those files?"),
            actions=[
                ft.TextButton("Yes", on_click=self.close_dlg),
                ft.TextButton("No", on_click=self.close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

    #self.create_new_singlecart = ft.TextButton(content=ft.Row([ft.Icon(icons.CREATE), ft.Text("Create")]), on_click=self.open_dlg, )
    def build(self):
        self.view = flet.Container(
            ft.Column([
                self.create_new_singlecart,
                self.images
            ])
        )
        return self.view

    def resize_page(self, e):
        self.images.width = e.control.width - 270
        self.view.update()


    def close_dlg(self, e):
        self.dlg.open = False
        self.page.update()

    def open_dlg(self, e):
        self.page.dialog = self.dlg
        self.dlg.open = True
        self.page.update()
