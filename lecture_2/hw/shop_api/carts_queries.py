from typing import Iterable

from items_queries import get_item_by_id, items
from models import Item, ItemInCart, Cart


def int_id_generator() -> Iterable[int]:
    i = 0
    while True:
        yield i
        i += 1


_cart_id_generator = int_id_generator()
carts = dict[int, Cart]()


def create_empty_cart() -> Cart:
    _id = next(_cart_id_generator)
    carts[_id] = Cart(_id, items=dict[int, ItemInCart](), price=0)

    return Cart(_id, carts[_id].items, carts[_id].price)


def get_cart_by_id(cart_id: int) -> Cart | str:
    if cart_id not in carts:
        return "cart not found"
    true_cart_price = 0
    true_cart_items = dict[int, ItemInCart]()

    cart: Cart = carts[cart_id]
    for item_id in cart.items:
        true_cart_item: Item = get_item_by_id(item_id)
        true_cart_item_quantity = cart.items[item_id].quantity
        true_cart_item_price = true_cart_item.info.price * true_cart_item_quantity
        true_cart_item_name = true_cart_item.info.name
        true_cart_price += true_cart_item_price
        true_cart_items[item_id] = ItemInCart(
            name=true_cart_item_name,
            quantity=true_cart_item_quantity,
            available=not true_cart_item.info.deleted,
        )

    carts[cart_id] = Cart(cart.id, true_cart_items, true_cart_price)

    return Cart(carts[cart_id].id, carts[cart_id].items, carts[cart_id].price)


def add_item_to_cart(cart_id: int, item_id: int) -> Cart | str:
    if cart_id not in carts:
        return "cart not found"
    if item_id not in items:
        return "item not found"
    if item_id in carts[cart_id].items:
        carts[cart_id].items[item_id].quantity += 1
    else:
        new_item = get_item_by_id(item_id)
        new_item_in_cart = ItemInCart(new_item.info.name, quantity=1, available=True)
        carts[cart_id].items[item_id] = new_item_in_cart

    carts[cart_id].price += items[item_id].price

    return Cart(id=cart_id, items=carts[cart_id].items, price=carts[cart_id].price)


def get_many_carts(
    offset: int = 0,
    limit: int = 10,
    min_price: float | None = None,
    max_price: float | None = None,
    min_quantity: int | None = None,
    max_quantity: int | None = None,
) -> Iterable[Cart]:

    curr = 0
    for cart in carts.values():
        if offset <= curr < offset + limit:
            if min_price is None or cart.price >= min_price:
                if max_price is None or cart.price <= max_price:
                    total_quantity = sum(item.quantity for item in cart.items.values())
                    if min_quantity is None or total_quantity >= min_quantity:
                        if max_quantity is None or total_quantity <= max_quantity:
                            yield cart
        curr += 1
