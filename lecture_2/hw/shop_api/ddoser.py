from concurrent.futures import ThreadPoolExecutor, as_completed

import requests


def create_item():
    for i in range(500):
        response = requests.post(
            "http://localhost:8080/item",
            json={
                "name": f"Тестовый товар {i}",
                "price": 2000.0,
            },
        )

        print(response)


def get_item():
    for i in range(500):

        response = requests.get(
            f"http://localhost:8080/item/{i}",
        )
        print(response)


with ThreadPoolExecutor() as executor:
    futures = {}

    for i in range(15):
        futures[executor.submit(create_item)] = f"create-item-{i}"

    for _ in range(15):
        futures[executor.submit(get_item)] = f"get-item-{i}"

    for future in as_completed(futures):
        print(f"completed {futures[future]}")
