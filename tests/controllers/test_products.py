from typing import List

import pytest
from tests.factories import product_data
from fastapi import status


async def test_controller_create_should_return_success(client, products_url):
    response = await client.post(products_url, json=product_data())

    content = response.json()

    del content["id"]
    del content["created_at"]
    del content["updated_at"]

    assert response.status_code == status.HTTP_201_CREATED
    assert content == {
        "name": "Iphone XX",
        "quantity": 10,
        "price": "10.500",
        "status": True,
    }


async def test_controller_get_should_return_success(
    client, products_url, product_inserted
):
    response = await client.get(f"{products_url}{product_inserted.id}")

    content = response.json()

    del content["created_at"]
    del content["updated_at"]

    assert response.status_code == status.HTTP_200_OK
    assert content == {
        "id": str(product_inserted.id),
        "name": "Iphone XX",
        "quantity": 10,
        "price": "10.500",
        "status": True,
    }


async def test_controller_get_should_return_not_found(client, products_url):
    response = await client.get(f"{products_url}80129791-dd95-4095-b341-ea4fd627912e")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Product not found with filter: 80129791-dd95-4095-b341-ea4fd627912e"
    }


@pytest.mark.usefixtures("products_inserted")
async def test_controller_query_should_return_success(client, products_url):
    response = await client.get(products_url)

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), List)
    assert len(response.json()) > 1


async def test_controller_patch_should_return_success(
    client, products_url, product_inserted
):
    response = await client.patch(
        f"{products_url}{product_inserted.id}", json={"price": "7.500"}
    )

    content = response.json()

    del content["created_at"]
    del content["updated_at"]

    assert response.status_code == status.HTTP_200_OK
    assert content == {
        "id": str(product_inserted.id),
        "name": "Iphone XX",
        "quantity": 10,
        "price": "7.500",
        "status": True,
    }


async def test_controller_patch_should_return_not_found(
    client,
    products_url,
):
    response = await client.patch(
        f"{products_url}80129791-dd95-4095-b341-ea4fd627912e", json={"price": "7.500"}
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Product not found with filter: 80129791-dd95-4095-b341-ea4fd627912e"
    }


async def test_controller_delete_should_return_no_content(
    client, products_url, product_inserted
):
    response = await client.delete(f"{products_url}{product_inserted.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_controller_delete_should_return_not_found(client, products_url):
    response = await client.delete(
        f"{products_url}80129791-dd95-4095-b341-ea4fd627912e"
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Product not found with filter: 80129791-dd95-4095-b341-ea4fd627912e"
    }
