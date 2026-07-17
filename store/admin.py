from django.contrib import admin

from .models import Category, ContactMessage, Order, OrderItem, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "price", "in_stock", "created_at"]
    list_filter = ["category", "in_stock"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["name", "phone", "created_at"]
    readonly_fields = ["created_at"]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ["product", "price", "quantity"]
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "full_name", "phone", "status", "total_price", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["full_name", "phone"]
    readonly_fields = ["full_name", "phone", "address", "note", "created_at"]
    inlines = [OrderItemInline]
