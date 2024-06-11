from typing import List
from uuid import UUID
import pytest
from store.core.exceptions import NotFoundException
from store.schemas.product import ProductOut, ProductUpdateOut
from store.usecases.product import product_usecase


async def test_usecases_create_should_return_success(product_in):
    result = await product_usecase.create(body=product_in)

    assert isinstance(result, ProductOut)
    assert result.name == "Iphone XX"


async def test_usecases_get_should_return_success(product_inserted):
    result = await product_usecase.get(id=product_inserted.id)

    assert isinstance(result, ProductOut)
    assert result.name == "Iphone XX"


async def test_usecases_get_should_return_not_found():
    with pytest.raises(NotFoundException) as err:
        await product_usecase.get(id=UUID("c9952620-5412-4d5d-8e32-ff717c361000"))

    assert (
        err.value.message
        == "Product not found with filter: c9952620-5412-4d5d-8e32-ff717c361000"
    )


@pytest.mark.usefixtures("products_inserted")
async def test_usecases_query_should_return_success():
    result = await product_usecase.query(apply_filter=False)

    assert isinstance(result, List)
    assert len(result) > 1


async def test_usecases_update_should_return_success(product_inserted, product_up):
    product_up.price = "9.500"
    result = await product_usecase.update(id=product_inserted.id, body=product_up)

    assert isinstance(result, ProductUpdateOut)


async def test_usecases_update_should_return_not_found(product_up, product_inserted):
    product_inserted.id = UUID("c9952620-5412-4d5d-8e32-ff717c361000")

    with pytest.raises(NotFoundException) as err:
        await product_usecase.update(id=product_inserted.id, body=product_up)

    assert (
        err.value.message
        == "Product not found with filter: c9952620-5412-4d5d-8e32-ff717c361000"
    )


async def test_usecases_delete_should_return_success(product_inserted):
    result = await product_usecase.delete(id=product_inserted.id)

    assert result is True


async def test_usecases_delete_should_return_not_found():
    with pytest.raises(NotFoundException) as err:
        await product_usecase.delete(id=UUID("c9952620-5412-4d5d-8e32-ff717c361000"))

    assert (
        err.value.message
        == "Product not found with filter: c9952620-5412-4d5d-8e32-ff717c361000"
    )
