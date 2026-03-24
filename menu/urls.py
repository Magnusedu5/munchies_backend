from django.urls import path
from .views import MenuListView, OrderTrackingView, BrandAssetView, EventPromoListView, JobPostingListView, OrderCreateView

urlpatterns = [
    path('menu/', MenuListView.as_view(), name='menu-list'),
    path('track/<int:pk>/', OrderTrackingView.as_view(), name='order-track'),
    path('order/create/', OrderCreateView.as_view(), name='order-create'),
    path('brand-assets/', BrandAssetView.as_view(), name='brand-assets'),
    path('events/', EventPromoListView.as_view(), name='events-list'),
    path('jobs/', JobPostingListView.as_view(), name='jobs-list'),
]