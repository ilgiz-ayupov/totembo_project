from django.contrib import admin
from .models import Watches, Chains, Comments, Customers, Cart, CartProduct, Orders

from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext as _


class WatchesAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "price", "photo", "time_create", "time_update", "is_published")
    list_display_links = ("title",)
    list_editable = ("photo", "is_published")


class ChainsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "price", "photo", "time_create", "time_update", "is_published")
    list_display_links = ("title",)
    list_editable = ("photo", "is_published")


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ("id", "username")
    list_display_links = ("username",)


class CustomersAdmin(UserAdmin):
    list_display = ("id", "username", "first_name", "last_name", "address", "phone")
    list_display_links = ("username",)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', "address", "phone")}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "first_name", "address", "order_status", "time_create", "time_order")
    list_display_links = ("customer", )


admin.site.register(Watches, WatchesAdmin)
admin.site.register(Chains, ChainsAdmin)
admin.site.register(Customers, CustomersAdmin)
admin.site.register(Cart)
admin.site.register(CartProduct)
