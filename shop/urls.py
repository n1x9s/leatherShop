from django.urls import path

from . import views

app_name = 'shop'
urlpatterns = [
    path("", views.Index.as_view(), name='index'),
    path('detail/<int:id_bag>', views.Detail.as_view(), name='detail'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('remove_item_from_cart/<int:item_id>/', views.remove_item_from_cart, name='remove_item_from_cart'),
    path('remove_all_from_cart/<int:item_id>/', views.remove_all_from_cart, name='remove_all_from_cart'),
    path('search/', views.search, name='search'),
    path('order/<int:product_id>/', views.order_bag, name='order_bag'),
    path('order_success/<int:order_id>/', views.order_success, name='order_success'),
    path('admin/bags/', views.admin_bag_list, name='admin_bag_list'),
    path('admin/bags/edit/<int:bag_id>/', views.admin_bag_edit, name='admin_bag_edit'),
    path('admin/bags/edit/', views.admin_bag_edit, name='admin_bag_edit'),
    path('admin/bags/delete/<int:bag_id>/', views.admin_bag_delete, name='admin_bag_delete'),

]
