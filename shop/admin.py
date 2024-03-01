from django.contrib import admin, messages
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price')
    list_filter = ('price', 'category')

    actions = ['get_max_sells']
    def get_max_sells(self, request, query_set):
        maxim = query_set.order_by('-num_of_buy')[0]
        self.message_user(request, f'the product with -> \nid: {maxim.id}\n title:{maxim.title}\n number_of_selling: {maxim.num_of_buy} ',
                          messages.SUCCESS)
        return maxim

    get_max_sells.short_description = 'get maximum sell'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user',)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'date_added')


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('title', )
    list_filter = ('date_submitted', )
