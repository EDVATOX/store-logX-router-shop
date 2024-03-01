from django.urls import path
from .views import *


urlpatterns = [
    path('', store, name='store'),
    path('add/<product_id>/', add_to_cart, name='add'),
    path('add_quantity/<product_id>/',  add_quantity, name='add_quantity'),
    path('sub_quantity/<product_id>/',  sub_quantity, name='sub_quantity'),
    path('check_out/<int:cart_id>/', check_out, name='check_out'),
    path('search/', search, name='search'),
    path("shop/", shop, name='shop'),
    path('shop/<str:category>', category_filtered_page, name='category'),
    path('shop/detail/<int:product_id>', product_detail, name='product-detail'),
    path('shop/<int:vote>/agree', agree_vote, name='agree'),
    path('shop/<int:vote>/disagree', disagree_vote, name='disagree')
]
