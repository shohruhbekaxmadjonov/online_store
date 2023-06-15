from django.contrib import admin

from store.models import Category, Product, User, Order, Cart


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'username')
    list_display_links = ('id', 'first_name', 'last_name', 'username')
    search_fields = ('first_name', 'last_name', 'username')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    list_display_links = ('id', 'title')
    ordering = ['id']


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'seller')
    list_display_links = ('id', 'title', 'category', 'seller')
    search_fields = ('title', 'category', 'seller')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user', 'count')
    list_display_links = ('id', 'product', 'user', 'count')
    search_fields = ('product', 'user', 'count')


admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Cart)
