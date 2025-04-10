class Product:
    """
    Класс продукта
    """
    name: str
    price: float
    description: str
    quantity: int

    def __init__(self, name, price, description, quantity):
        self.name = name
        self.price = price
        self.description = description
        self.quantity = quantity


    def check_quantity(self, quantity) -> bool:
        """
        TODO Верните True если количество продукта больше или равно запрашиваемому
            и False в обратном случае
        """
        return quantity <= self.quantity


    def buy(self, quantity):
        """
        TODO реализуйте метод покупки
            Проверьте количество продукта используя метод check_quantity
            Если продуктов не хватает, то выбросите исключение ValueError
        """
        if not self.check_quantity(quantity):
            raise ValueError(f"Недостаточно товара '{self.name}'. Доступно: {self.quantity}, запрошено: {quantity}")

        self.quantity -= quantity
        print(f"Успешно куплено {quantity} единиц товара '{self.name}'. Остаток: {self.quantity}")

    def __hash__(self):
        return hash(self.name + self.description)


class Cart:
    """
    Класс корзины. В нем хранятся продукты, которые пользователь хочет купить.
    TODO реализуйте все методы класса
    """

    # Словарь продуктов и их количество в корзине
    products: dict[Product, int]

    def __init__(self):
        # По-умолчанию корзина пустая
        self.products = {}

    def add_product(self, product: Product, buy_count=1):
        """
        Метод добавления продукта в корзину.
        Если продукт уже есть в корзине, то увеличиваем количество
        """
        if buy_count <= 0:
            raise ValueError("Количество должно быть положительным")

        if product in self.products:
            self.products[product] += buy_count
        else:
            self.products[product] = buy_count

    def remove_product(self, product: Product, remove_count=None):
        """
        Метод удаления продукта из корзины.
        Если remove_count не передан, то удаляется вся позиция
        Если remove_count больше, чем количество продуктов в позиции, то удаляется вся позиция
        """
        if product not in self.products:
            raise ValueError("В корзине нет этого товара")

        if remove_count is None:
            del self.products[product]
        elif remove_count > self.products[product]:
            del self.products[product]
        else:
            self.products[product] -= remove_count

    def clear(self):
        """
        Метод очистки корзины
        """
        self.products.clear()

    def get_total_price(self) -> float:
        """
        Метод подсчета полной стоимости корзины
        """
        total_price = 0.0
        for product in self.products:
            total_price += product.price * self.products[product]
        return total_price

    def buy(self):
        """
        Метод покупки.
        Учтите, что товаров может не хватать на складе.
        В этом случае нужно выбросить исключение ValueError
        """

        # проверяем наличие товаров
        for product, quantity in self.products.items():
            if not product.check_quantity(quantity):
                raise ValueError(
                    f"Недостаточно товара '{product.name}'. "
                    f"Доступно: {product.quantity}, требуется: {quantity}")

        # Если товары в наличии - выполняем покупку
        total_price = 0.0
        for product, quantity in self.products.items():
            product.quantity -= quantity
            total_price += product.price * quantity
        print(f"Сумма покупки {total_price}")
        self.clear()


