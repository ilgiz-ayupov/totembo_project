from django.views import View
from django.shortcuts import redirect
from .models import Cart, Customers


class CartMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.customer = Customers.objects.get(username=request.user.username)
            cart = Cart.objects.filter(owner=self.customer, in_order=False).first()
            if not cart:
                cart = Cart.objects.create(owner=self.customer)
            self.cart = cart
            return super(CartMixin, self).dispatch(request, *args, **kwargs)
        else:
            return redirect("home")
