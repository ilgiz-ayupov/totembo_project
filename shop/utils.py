from django.db.models import Sum


def recalc_cart(cart):
    cart_data = cart.products.aggregate(Sum("quantity"), Sum("final_price"))
    if not cart_data.get("quantity__sum"):
        cart_data["quantity__sum"] = 0

    if not cart_data.get("final_price__sum"):
        cart_data["final_price__sum"] = 0

    cart.total_products = cart_data["quantity__sum"]
    cart.total_price = cart_data["final_price__sum"]
    cart.save()
