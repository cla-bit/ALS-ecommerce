from django.urls import path
from .views import home, recommend_products, search_and_recommend


app_name = 'recommendation'

urlpatterns = [
    path('', home, name='home'),
    path('recommendations/<int:product_id>/', recommend_products, name='recommend_items'),
    path('search/', search_and_recommend, name='search_products'),
]
