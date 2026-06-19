import flet as ft
from db import main_db


def main_page(page: ft.Page):
    page.title = "Список покупок"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    filter_type = "all"

    product_list = ft.Column(spacing=6, scroll=ft.ScrollMode.AUTO, expand=True)
    counter_text = ft.Text(size=14, weight=ft.FontWeight.BOLD)

    def load_products():
        product_list.controls.clear()
        for product_id, name, quantity, bought in main_db.get_products(filter_type):
            product_list.controls.append(
                view_product(product_id=product_id, name=name,
                             quantity=quantity, bought=bought)
            )
        bought_count, total = main_db.count_products()
        counter_text.value = f"Куплено: {bought_count} из {total}"
        # подсветка активного фильтра — активная кнопка заблокирована
        btn_all.disabled = filter_type == "all"
        btn_bought.disabled = filter_type == "bought"
        btn_unbought.disabled = filter_type == "unbought"
        page.update()

    def view_product(product_id, name, quantity, bought):
        checkbox = ft.Checkbox(
            label=f"{name}  x{quantity}",
            value=bool(bought),
            on_change=lambda e: toggle_product(product_id, e.control.value),
        )

        def delete_product_flet(_):
            main_db.delete_product(product_id)
            load_products()

        delete_button = ft.TextButton("✕", on_click=delete_product_flet)

        return ft.Row([checkbox, delete_button],
                      alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    def toggle_product(product_id, is_bought):
        main_db.set_bought(product_id, is_bought)
        load_products()

    def add_product_flet(_):
        name = name_input.value.strip() if name_input.value else ""
        if not name:
            return
        qty = qty_input.value.strip() if qty_input.value else ""
        qty = int(qty) if qty.isdigit() and int(qty) > 0 else 1
        main_db.add_product(name, qty)
        name_input.value = None
        qty_input.value = "1"
        load_products()

    name_input = ft.TextField(label="Товар", expand=True, on_submit=add_product_flet)
    qty_input = ft.TextField(label="Кол-во", value="1", width=90,
                             keyboard_type=ft.KeyboardType.NUMBER)
    add_button = ft.ElevatedButton("ADD", on_click=add_product_flet)

    def set_filter(filter_value):
        nonlocal filter_type
        filter_type = filter_value
        load_products()

    btn_all = ft.ElevatedButton("Все", on_click=lambda e: set_filter("all"))
    btn_bought = ft.ElevatedButton("Купленные", on_click=lambda e: set_filter("bought"))
    btn_unbought = ft.ElevatedButton("Некупленные", on_click=lambda e: set_filter("unbought"))

    filter_buttons = ft.Row(
        [btn_all, btn_bought, btn_unbought],
        alignment=ft.MainAxisAlignment.SPACE_AROUND,
    )

    page.add(
        ft.Row([name_input, qty_input, add_button]),
        ft.Row([filter_buttons, counter_text],
               alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ft.Divider(),
        product_list,
    )

    load_products()


if __name__ == '__main__':
    main_db.init_db()
    ft.app(main_page)