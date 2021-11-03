from django.urls import path
from .views import (BaseView, CategoryDetailView,
                    ProductDetailView, CustomerAuthView,
                    CustomerRegisterView, CustomerLoginView, UserProfileView,
                    UserLogoutView, UserProfileUpdateView, ShowCartView,
                    AddProductView, ChangeQtyView, DeleteProductView, MakeOrderView)

# ct_model -> content type model
urlpatterns = [
    path("", BaseView.as_view(), name="home"),
    path("category/<str:ct_model>", CategoryDetailView.as_view(), name="category_detail"),
    path("product/<str:ct_model>/<int:pk>", ProductDetailView.as_view(), name="product_detail"),

    path("cart/", ShowCartView.as_view(), name="cart"),
    path("add_product/<str:ct_model>/<int:pk>", AddProductView.as_view(), name="add_product"),
    path("change_qty/<str:ct_model>/<int:pk>", ChangeQtyView.as_view(), name="change_qty"),
    path("delete_product/<str:ct_model>/<int:pk>", DeleteProductView.as_view(), name="delete_product"),
    path("make_order/", MakeOrderView.as_view(), name="make_order"),

    path("auth/", CustomerAuthView.as_view(), name="auth"),
    path("register/", CustomerRegisterView.as_view(), name="register"),
    path("login/", CustomerLoginView.as_view(), name="login"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("edit_profile/<int:pk>", UserProfileUpdateView.as_view(), name="update_profile"),
]
