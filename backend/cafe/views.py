import json
from decimal import Decimal, InvalidOperation

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import MenuItem, Order

# Temporary workshop storage. Mission 7 replaces this with the database.
temporary_menu = [
    {"id": 1, "name": "Iced Matcha", "price": "6.00", "available": True},
    {"id": 2, "name": "Latte", "price": "5.00", "available": True},
    {"id": 3, "name": "Americano", "price": "4.00", "available": True},
    {"id": 4, "name": "Chai Latte", "price": "5.50", "available": True},
]

temporary_orders = []


def menu_item_to_json(item):
    return {
        "id": item.id,
        "name": item.name,
        "price": f"{item.price:.2f}",
        "available": item.available,
    }


def order_to_json(order):
    return {
        "id": order.id,
        "customer_name": order.customer_name,
        "menu_item": menu_item_to_json(order.menu_item),
        "quantity": order.quantity,
        "status": order.status,
    }


def reject_if_unavailable(menu_item):
    # Already finished. Disabling a button in React does not enforce this rule.
    if isinstance(menu_item, dict):
        available = menu_item["available"]
    else:
        available = menu_item.available
    if not available:
        return JsonResponse({"error": "menu item is unavailable"}, status=400)
    return None


# Workshop demo only. Real applications should use real authentication
# and authorization instead of a shared hard-coded key.
def has_admin_access(request):
    return request.headers.get("X-ADMIN-KEY") == "binary-brews-demo"


@csrf_exempt
def menu_list(request):
    if request.method != "GET":
        return JsonResponse({"error": "method not allowed"}, status=405)

    # TODO-WORKSHOP-2
    # Return the temporary menu as JSON:
    return JsonResponse(temporary_menu, safe=False)

    # TODO-WORKSHOP-7
    # Replace temporary_menu with the database:
    # items = [menu_item_to_json(item) for item in MenuItem.objects.all()]
    # return JsonResponse(items, safe=False)


@csrf_exempt
def order_collection(request):
    if request.method == "GET":
        # TODO-WORKSHOP-7
        # orders = [
        #     order_to_json(order)
        #     for order in Order.objects.select_related("menu_item")
        # ]
        # return JsonResponse(orders, safe=False)
        return JsonResponse(temporary_orders, safe=False)

    if request.method == "POST":
        return create_order(request)

    return JsonResponse({"error": "method not allowed"}, status=405)


def create_order(request):
    try:
        data = json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "invalid JSON"}, status=400)

    customer_name = str(data.get("customer_name", "")).strip()
    if not customer_name:
        return JsonResponse({"error": "customer_name is required"}, status=400)

    try:
        menu_item_id = int(data.get("menu_item_id"))
    except (TypeError, ValueError):
        return JsonResponse({"error": "menu item not found"}, status=400)

    try:
        quantity = int(data.get("quantity", 1))
    except (TypeError, ValueError):
        return JsonResponse({"error": "quantity must be a positive integer"}, status=400)

    if quantity < 1:
        return JsonResponse({"error": "quantity must be a positive integer"}, status=400)

    # TODO-WORKSHOP-3
    menu_item = next((item for item in temporary_menu if item["id"] == menu_item_id), None)
    if menu_item is None:
        return JsonResponse({"error": "menu item not found"}, status=400)
    blocked = reject_if_unavailable(menu_item)
    if blocked is not None:
        return blocked
    order = {
        "id": len(temporary_orders) + 1,
        "customer_name": customer_name,
        "menu_item": dict(menu_item),
        "quantity": quantity,
        "status": "pending",
    }
    temporary_orders.append(order)
    return JsonResponse(order, status=201)

    # TODO-WORKSHOP-7
    # menu_item = MenuItem.objects.filter(id=menu_item_id).first()
    # if menu_item is None:
    #     return JsonResponse({"error": "menu item not found"}, status=400)
    # blocked = reject_if_unavailable(menu_item)
    # if blocked is not None:
    #     return blocked
    # order = Order.objects.create(
    #     customer_name=customer_name,
    #     menu_item=menu_item,
    #     quantity=quantity,
    #     status="pending",
    # )
    # return JsonResponse(order_to_json(order), status=201)


@csrf_exempt
def admin_menu_item(request, item_id):
    if request.method != "PATCH":
        return JsonResponse({"error": "method not allowed"}, status=405)

    # TODO-WORKSHOP-6
    # if not has_admin_access(request):
    #     return JsonResponse({"error": "admin access required"}, status=403)
    # try:
    #     data = json.loads(request.body or b"{}")
    # except json.JSONDecodeError:
    #     return JsonResponse({"error": "invalid JSON"}, status=400)
    # menu_item = next((item for item in temporary_menu if item["id"] == item_id), None)
    # if menu_item is None:
    #     return JsonResponse({"error": "menu item not found"}, status=404)
    # if "price" not in data:
    #     return JsonResponse({"error": "price is required"}, status=400)
    # try:
    #     price = Decimal(str(data["price"]))
    # except (InvalidOperation, ValueError):
    #     return JsonResponse({"error": "price must be a number"}, status=400)
    # if price < 0:
    #     return JsonResponse({"error": "price must be a number"}, status=400)
    # menu_item["price"] = f"{price:.2f}"
    # return JsonResponse(menu_item)

    # TODO-WORKSHOP-7
    # Save that price with the ORM instead of temporary_menu:
    # menu_item = MenuItem.objects.filter(id=item_id).first()
    # menu_item.price = price
    # menu_item.save()
    # return JsonResponse(menu_item_to_json(menu_item))

    # TODO-WORKSHOP-8
    # Also accept {"available": false} and save it on the menu item.

    return JsonResponse(
        {"error": "TODO-WORKSHOP-6 is not finished yet"},
        status=501,
    )
