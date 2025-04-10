"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)

@pytest.fixture
def cart():
    return Cart()

class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        assert product.check_quantity(123)

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        product.buy(123)
        assert product.quantity == 877

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError) as exception:
            product.buy(1234)
        assert "Недостаточно товара" in str(exception.value)
        print(exception.value)

class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_add_product_to_cart(self, cart, product):
        """Тест увеличения количества существующего продукта на 1"""
        cart.add_product(product, 1)
        assert product in cart.products
        assert cart.products[product] == 1

    @pytest.mark.parametrize("invalid_count", [0, -555])
    def test_add_invalid_quantity(self, cart, product, invalid_count):
        """Тест обработки невалидного количества (должен вызывать ValueError)"""
        with pytest.raises(ValueError) as exc_info:
            cart.add_product(product, invalid_count)
        assert "Количество должно быть положительным" in str(exc_info.value)

    def test_increase_existing_product(self, cart, product):
        """Тест увеличения количества существующего продукта"""
        cart.add_product(product, 2)
        cart.add_product(product, 3)
        assert cart.products[product] == 5


    def test_remove_product_from_cart(self, cart, product):
        """Тест удаления валидного количества продуктов из корзины"""
        cart.add_product(product, 3)
        cart.remove_product(product, 1)
        assert cart.products[product] == 2

    def test_remove_more_products_then_have(self, cart, product):
        """Тест удаления всей позиции, когда remove_count больше, чем есть в корзине"""
        cart.add_product(product, 2)
        cart.remove_product(product, 7)
        assert product not in cart.products

    def test_remove_all_when_count_not_specified(self, cart, product):
        """Тест удаления всей позиции, когда remove_count не указан"""
        cart.add_product(product, 2)
        cart.remove_product(product)
        assert product not in cart.products

    def test_no_such_product_in_cart(self, cart, product):
        """Ошибка ValueError при попытке удалить товар, которого нет в корзине"""
        with pytest.raises(ValueError) as exception:
            cart.remove_product(product)
        assert "В корзине нет этого товара" in str(exception.value)


    def test_clear_cart(self, cart, product):
        """Проверка очистки корзины - после вызова метода clear корзина должна быть пуста"""
        cart.add_product(product, 2)
        cart.clear()
        assert product not in cart.products


    def test_total_price(self, cart, product):
        """Проверка корректного расчёта общей стоимости товаров в корзине"""
        cart.add_product(product, 7)
        assert cart.get_total_price() == 700.0

    def test_total_price_empty_cart(self, cart, product):
        """Проверка, что общая стоимость пустой корзины равна 0"""
        assert cart.get_total_price() == 0.0


    def test_successful_purchase(self, cart, product):
        """Проверка успешной покупки - количество товара на складе уменьшается, корзина очищается"""
        cart.add_product(product, 998)
        cart.buy()
        assert product.quantity == 2
        assert len(cart.products) == 0

    def test_insufficient_quantity(self, cart, product):
        """Проверка ошибки при попытке купить больше товара, чем есть на складе"""
        cart.add_product(product, 1003)
        with pytest.raises(ValueError):
            cart.buy()
        assert product.quantity == 1000




