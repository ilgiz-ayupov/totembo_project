from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.contrib.contenttypes.models import ContentType

from django.contrib.auth import login, logout

from .models import Watches, Chains, Customers, Cart, CartProduct
from .forms import CustomersRegisterForm, CustomersLoginForm, CustomerProfileForm, OrderForm
from .mixins import CartMixin
from .utils import recalc_cart


class BaseView(View):
    def get(self, request):
        quartz_editions = Watches.objects.filter(watch_type="QE", is_published=True)
        automatic_editions = Watches.objects.filter(watch_type="AE", is_published=True)
        chains = Chains.objects.filter(is_published=True)

        return render(request, "shop/index.html", {
            "quartz_editions": quartz_editions,
            "automatic_editions": automatic_editions,
            "chains": chains,
            "title": "TOTEMBO"
        })


class CategoryDetailView(View):
    def get(self, request, *args, **kwargs):
        ct_model = kwargs.get("ct_model")  # "watches"/ "chains"
        content_type = ContentType.objects.get(model=ct_model)  # content type object "Watches object"
        # Watches.objects.filter()
        model = content_type.model_class()
        products = model.objects.filter(is_published=True)
        return render(request, "shop/category_detail.html", {
            "products": products,
            "title": model._meta.verbose_name_plural
        })


class ProductDetailView(View):
    def get(self, request, **kwargs):
        # localhost:8000/product/watches/1
        ct_model, pk = kwargs.get("ct_model"), kwargs.get("pk")
        content_type = ContentType.objects.get(model=ct_model)
        model = content_type.model_class()

        product = model.objects.get(is_published=True, pk=pk)

        return render(request, "shop/product_detail.html", {
            "product": product
        })


class ShowCartView(CartMixin):
    def get(self, request, **kwargs):
        form = OrderForm()
        recalc_cart(self.cart)
        return render(request, "shop/cart.html", {
            "title": "Ваша корзина",
            "cart": self.cart,
            "form": form
        })


class MakeOrderView(CartMixin):
    def post(self, request):
        form = OrderForm(data=request.POST)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = self.customer
            new_order.cart = self.cart

            new_order.save()

            self.cart.in_order = True
            self.cart.save()

            return redirect("home")
        else:
            return redirect("cart")


class AddProductView(CartMixin):
    def get(self, request, **kwargs):
        ct_model, pk = kwargs["ct_model"], kwargs["pk"]
        content_type = ContentType.objects.get(model=ct_model)
        model = content_type.model_class()

        product = model.objects.get(pk=pk)

        # Если объект найден то мы получаем сам cart_product, False
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.customer, cart=self.cart, content_type=content_type,
            object_id=product.pk
        )

        if created:
            cart_product.quantity = 1
            cart_product.final_price = product.price
            cart_product.save()

            self.cart.products.add(cart_product)
            self.cart.save()
        else:
            cart_product.quantity += 1
            cart_product.final_price += product.price
            cart_product.save()
        return redirect("cart")


class ChangeQtyView(CartMixin):
    def post(self, request, **kwargs):
        ct_model, pk = kwargs.get("ct_model"), kwargs.get("pk")

        content_type = ContentType.objects.get(model=ct_model)
        model = content_type.model_class()

        product = model.objects.get(pk=pk)

        cart_product = CartProduct.objects.get(
            user=self.customer, cart=self.cart, content_type=content_type,
            object_id=product.pk
        )

        qty = int(request.POST.get("qty"))
        if qty <= 10:
            cart_product.quantity = qty
            cart_product.final_price = product.price * qty
            cart_product.save()
        return redirect("cart")


class DeleteProductView(CartMixin):
    def get(self, request, **kwargs):
        ct_model, pk = kwargs.get("ct_model"), kwargs.get("pk")

        content_type = ContentType.objects.get(model=ct_model)
        model = content_type.model_class()

        product = model.objects.get(pk=pk)

        cart_product = CartProduct.objects.get(
            user=self.customer, cart=self.cart, content_type=content_type,
            object_id=product.pk
        )

        # Удаление cart_product из корзины
        self.cart.products.remove(cart_product)

        # Удаление cart_product
        cart_product.delete()
        return redirect("cart")


# Авторизация пользователей
class CustomerAuthView(View):
    def get(self, request):
        register_form = CustomersRegisterForm()
        login_form = CustomersLoginForm()
        return render(request, "shop/user_auth.html", {
            "register_form": register_form,
            "login_form": login_form,
            "title": "Регистрация",
        })


class CustomerRegisterView(View):
    @staticmethod
    def post(request):
        register_form = CustomersRegisterForm(data=request.POST)
        if register_form.is_valid():
            user = register_form.save()
            login(request, user)
            return redirect("profile")
        else:
            return redirect("auth")


class CustomerLoginView(View):
    @staticmethod
    def post(request):
        register_form = CustomersLoginForm(data=request.POST)
        if register_form.is_valid():
            user = register_form.get_user()
            login(request, user)
            return redirect("profile")
        else:
            return redirect("auth")


class UserProfileView(View):
    def get(self, request):
        customer = get_object_or_404(Customers, username=request.user.username)
        return render(request, "shop/profile.html", {
            "customer": customer
        })


class UserProfileUpdateView(UpdateView):
    form_class = CustomerProfileForm
    template_name = "shop/update_profile.html"

    def get_queryset(self):
        return Customers.objects.filter(pk=self.kwargs["pk"])

    def get_success_url(self):
        return reverse_lazy("profile")


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("home")


class OrdersView(View):
    def get(self, requests):
        pass
