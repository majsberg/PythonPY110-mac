import json
import os
from store.models import DATABASE
from django.contrib.auth import get_user

def add_user_to_cart(request, username: str) -> None:
    """
    Добавляет пользователя в базу данных корзины, если его там не было.

    :param username: Имя пользователя
    :return: None
    """
    cart_users = view_in_cart(request)  # Чтение всей базы корзин

    cart = cart_users.get(username)  # Получение корзины конкретного пользователя

    if not cart:  # Если пользователя до настоящего момента не было в корзине, то создаём его и записываем в базу
        with open('cart.json', mode='w', encoding='utf-8') as f:
            cart_users[username] = {'products': {}}
            json.dump(cart_users, f)


def filtering_category(database: dict[str, dict],
                       category_key: [None, str] = None,
                       ordering_key: [None, str] = None,
                       reverse: bool = False):
    """
        Функция фильтрации данных по параметрам

        :param database: База данных. (словарь словарей. При проверке в качестве database будет передаваться словарь DATABASE из models.py)
        :param category_key: [Опционально] Ключ для группировки категории. Если нет ключа, то рассматриваются все товары.
        :param ordering_key: [Опционально] Ключ по которому будет произведена сортировка результата.
        :param reverse: [Опционально] Выбор направления сортировки:
            False - сортировка по возрастанию;
            True - сортировка по убыванию.
        :return: list[dict] список товаров с их характеристиками, попавших под условия фильтрации. Если нет таких элементов,
        то возвращается пустой список
        """
    if category_key is not None:
        print(database.values())
        for each in database.values():
            print(each.get('category'))
        result = [product for product in database.values() if product.get('category') == category_key]
        print(result)

    else:
        result = list(database.values())
        print(result)


    if ordering_key is not None:
        result.sort(key=lambda x: x[ordering_key], reverse=reverse)
    return result


def view_in_cart(request) -> dict:  # Уже реализовано, не нужно здесь ничего писать
    """
    Просматривает содержимое cart.json

    :return: Содержимое 'cart.json'
    """
    if os.path.exists('cart.json'):  # Если файл существует
        with open('cart.json', encoding='utf-8') as f:
            return json.load(f)

    user = get_user(request).username
    cart = {user: {'products': {}}}  # Создаём пустую корзину
    with open('cart.json', mode='x', encoding='utf-8') as f:   # Создаём файл и записываем туда пустую корзину
        json.dump(cart, f)

    return cart


def add_to_cart(request, id_product: str) -> bool:
    """
    Добавляет продукт в корзину. Если в корзине нет данного продукта, то добавляет его с количеством равное 1.
    Если в корзине есть такой продукт, то добавляет количеству данного продукта + 1.

    :param id_product: Идентификационный номер продукта в виде строки.
    :return: Возвращает True в случае успешного добавления, а False в случае неуспешного добавления(товара по id_product
    не существует).
    """
    cart_user = view_in_cart(request)
    cart = cart_user[get_user(request).username]  # TODO Помните, что у вас есть уже реализация просмотра корзины,
    # поэтому, чтобы загрузить данные из корзины, не нужно заново писать код.

    # ! Обратите внимание, что в переменной cart находится словарь с ключом products.
    # ! Именно в cart["products"] лежит словарь гдк по id продуктов можно получить число продуктов в корзине.
    # ! Т.е. чтобы обратиться к продукту с id_product = "1" в переменной cart нужно вызвать
    # ! cart["products"][id_product]
    # ! Далее уже сами решайте как и в какой последовательности дальше действовать.


    if id_product in DATABASE and id_product in cart['products']:
        cart['products'][id_product] += 1
    elif id_product in DATABASE and id_product not in cart['products']:
        cart['products'][id_product] = 1
    else:
        return False
    with open('cart.json', 'w', encoding='utf-8') as f:
        json.dump(cart_user, f)
    return True


def remove_from_cart(request, id_product: str) -> bool:
    """
    Добавляет позицию продукта из корзины. Если в корзине есть такой продукт, то удаляется ключ в словаре
    с этим продуктом.

    :param id_product: Идентификационный номер продукта в виде строки.
    :return: Возвращает True в случае успешного удаления, а False в случае неуспешного удаления(товара по id_product
    не существует).
    """
    cart_users = view_in_cart(request)
    cart = cart_users[get_user(request).username]  # TODO Помните, что у вас есть уже реализация просмотра корзины,
    # поэтому, чтобы загрузить данные из корзины, не нужно заново писать код.
    if id_product not in cart['products']:
        return False
    else:
        cart['products'].pop(id_product)
    with open('cart.json', 'w', encoding='utf-8') as f:
        json.dump(cart_users, f)
    # С переменной cart функции remove_from_cart ситуация аналогичная, что с cart функции add_to_cart

    # TODO Проверьте, а существует ли такой товар в корзине, если нет, то возвращаем False.

    # TODO Если существует товар, то удаляем ключ 'id_product' у cart['products'].

    # TODO Не забываем записать обновленные данные cart в 'cart.json'

    return True


def view_in_wishlist(request) -> dict:
    """
    Просматривает содержимое wishlist.json

    :return: Содержимое 'wishlist.json'
    """
    if os.path.exists('wishlist.json'):  # Если файл существует
        with open('wishlist.json', encoding='utf-8') as f:
            return json.load(f)

    user = get_user(request).username
    wishlist = {user: {'products': []}}  # Создаём пустой список покупок
    with open('wishlist.json', mode='x', encoding='utf-8') as f:   # Создаём файл и записываем туда пустую корзину
        json.dump(wishlist, f)

    return wishlist


def add_to_wishlist(request, id_product: str) -> bool:
    """
    Добавляет продукт в список. Если в списке нет данного продукта, то добавляет его.
    Если в списке есть такой продукт, то не добавляет его.

    :param id_product: Идентификационный номер продукта в виде строки.
    :return: Возвращает True в случае успешного добавления, а False в случае неуспешного добавления(товара по id_product
    не существует).
    """
    wishlist_user = view_in_wishlist(request)
    wishlist = wishlist_user[get_user(request).username]  # TODO Помните, что у вас есть уже реализация просмотра списка,
    # поэтому, чтобы загрузить данные из списка, не нужно заново писать код.

    # ! Обратите внимание, что в переменной wishlist находится словарь с ключом products.
    # ! Именно в wishlist["products"] лежит словарь гдк по id продуктов можно получить наличие продута в списке.
    # ! Т.е. чтобы обратиться к продукту с id_product = "1" в переменной wishlist нужно вызвать
    # ! wishlist["products"][id_product]
    # ! Далее уже сами решайте как и в какой последовательности дальше действовать.

    # if id_product in DATABASE and id_product in wishlist['products']:
    #     wishlist['products'][id_product] += 0
    if id_product in DATABASE and id_product not in wishlist['products']:
        wishlist['products'].append(id_product)
    else:
        return False
    with open('wishlist.json', 'w', encoding='utf-8') as f:
        json.dump(wishlist_user, f)
    return True


def remove_from_wishlist(request, id_product: str) -> bool:
    """
    Добавляет позицию продукта из списка. Если в списке есть такой продукт, то удаляется ключ в словаре
    с этим продуктом.

    :param id_product: Идентификационный номер продукта в виде строки.
    :return: Возвращает True в случае успешного удаления, а False в случае неуспешного удаления(товара по id_product
    не существует).
    """
    wishlist_users = view_in_wishlist(request)
    wishlist = wishlist_users[get_user(request).username]  # TODO Помните, что у вас есть уже реализация просмотра списка,
    # поэтому, чтобы загрузить данные из него, не нужно заново писать код.
    if id_product not in wishlist['products']:
        return False
    else:
        wishlist['products'].remove(id_product)
    with open('wishlist.json', 'w', encoding='utf-8') as f:
        json.dump(wishlist_users, f)
    # С переменной cart функции remove_from_wishlist ситуация аналогичная, что с wishlist функции add_to_wishlist

    # TODO Проверьте, а существует ли такой товар в корзине, если нет, то возвращаем False.

    # TODO Если существует товар, то удаляем ключ 'id_product' у wishlist['products'].

    # TODO Не забываем записать обновленные данные cart в 'wishlist.json'

    return True


def add_user_to_wishlist(request, username: str) -> None:
    """
    Добавляет пользователя в базу данных списка, если его там не было.

    :param username: Имя пользователя
    :return: None
    """
    wishlist_users = view_in_wishlist(request)  # Чтение всей базы списков
    wishlist = wishlist_users.get(username)  # Получение списка конкретного пользователя

    if not wishlist:  # Если пользователя до настоящего момента не было в списке, то создаём его и записываем в базу
        with open('wishlist.json', mode='w', encoding='utf-8') as f:
            wishlist_users[username] = {'products': {}}
            json.dump(wishlist_users, f)


if __name__ == "__main__":
    from store.models import DATABASE

    test = [
        {'name': 'Клубника', 'discount': None, 'price_before': 500.0,
         'price_after': 500.0,
         'description': 'Сладкая и ароматная клубника, полная витаминов, чтобы сделать ваш день ярче.',
         'rating': 5.0, 'review': 200, 'sold_value': 700,
         'weight_in_stock': 400,
         'category': 'Фрукты', 'id': 2, 'url': 'store/images/product-2.jpg',
         'html': 'strawberry'},

        {'name': 'Яблоки', 'discount': None, 'price_before': 130.0,
         'price_after': 130.0,
         'description': 'Сочные и сладкие яблоки - идеальная закуска для здорового перекуса.',
         'rating': 4.7, 'review': 30, 'sold_value': 70, 'weight_in_stock': 200,
         'category': 'Фрукты', 'id': 10, 'url': 'store/images/product-10.jpg',
         'html': 'apple'}
    ]

    print(filtering_category(DATABASE, 'Фрукты', 'price_after', True) == test)  # True