from django.contrib import admin
from .models import Product, Order, OrderItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price_in_inr", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name",)
    ordering = ("id",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "quantity", "unit_price_inr")
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "status",
        "total_amount_inr",
        "stripe_session_id",
        "stripe_payment_intent_id",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("id", "user__username", "stripe_session_id", "stripe_payment_intent_id")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)

    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product", "quantity", "unit_price_inr")
    list_filter = ("product",)
    search_fields = ("order__id", "product__name")
    ordering = ("-id",)
