from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from .models import DATABASE
from django.http import HttpResponse, HttpResponseNotFound
from logic.services import filtering_category, add_to_cart, remove_from_cart, view_in_cart

def products_view(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        if id:
            if DATABASE.get(id) is not None:
                return JsonResponse(DATABASE.get(id), json_dumps_params={'ensure_ascii': False, 'indent': 4})
            return HttpResponseNotFound("Данного продукта нет в базе данных")
        category_key = request.GET.get('category')
        ordering_key = request.GET.get('ordering')
        if ordering_key:
            if request.GET.get('reverse') in ['true', 'True', 'TRUE']:
                data = filtering_category(DATABASE, category_key, ordering_key, True)
            else:
                data = filtering_category(DATABASE, category_key, ordering_key)
        else:
            data = filtering_category(DATABASE, category_key)
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False, 'indent': 4}, safe=False)


def shop_view(request):
    if request.method == 'GET':
        return render(request, 'store/shop.html', context={"products": DATABASE.values()})


def products_page_view(request, page):
    if request.method == 'GET':
        if isinstance(page, str):
            print('slug str')
            for data in DATABASE.values():
                if data['html'] == page: # Если значение переданного параметра совпадает именем html файла
                    with open(f'store/products/{page}.html', encoding="utf-8") as f:
                        data = f.read()
                    return HttpResponse(data)
        elif isinstance(page, int):
            print('int')
            data = DATABASE.get(str(page))
            if data:
                with open(f'store/products/{data["html"]}.html', encoding="utf-8") as f:
                    data = f.read()
                return HttpResponse(data)

        return HttpResponse(status=404)


def cart_view(request):
    if request.method == "GET":
        data = view_in_cart() # TODO Вызвать ответственную за это действие функцию
        if request.GET.get('format') == 'JSON':
            return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                     'indent': 4})
        products = []
        for product_id, quantity in data['products'].items():
            product = DATABASE.get(product_id)
            product['quantity'] = quantity
            product["price_total"] = f"{quantity * product['price_after']:.2f}"
            products.append(product)
        return render(request, "store/cart.html", context={"products": products})

def cart_add_view(request, id_product):
    if request.method == "GET":
        result = add_to_cart(id_product) # TODO Вызвать ответственную за это действие функцию и передать необходимые параметры
        if result:
            return JsonResponse({"answer": "Продукт успешно добавлен в корзину"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное добавление в корзину"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})

def cart_del_view(request, id_product):
    if request.method == "GET":
        result = remove_from_cart(id_product) # TODO Вызвать ответственную за это действие функцию и передать необходимые параметры
        if result:
            return JsonResponse({"answer": "Продукт успешно удалён из корзины"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное удаление из корзины"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})