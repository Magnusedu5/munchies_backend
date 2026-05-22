from django.urls import path
from .views import (
    MenuListView, OrderTrackingView, BrandAssetView,
    EventPromoListView, JobPostingListView, OrderCreateView,
    AdminStatsView,
    AdminOrderListView, AdminOrderStatusUpdateView,
    AdminMenuItemListCreateView, AdminMenuItemDetailView,
    AdminMenuItemOptionCreateView, AdminMenuItemOptionDeleteView,
    AdminCategoryListCreateView, AdminCategoryDetailView,
    AdminEventListCreateView, AdminEventDetailView,
    AdminJobListCreateView, AdminJobDetailView,
    AdminSubCategoryListCreateView, AdminSubCategoryDetailView,
)

urlpatterns = [
    # Public
    path('menu/',          MenuListView.as_view(),       name='menu-list'),
    path('track/<int:pk>/',OrderTrackingView.as_view(),  name='order-track'),
    path('order/create/',  OrderCreateView.as_view(),    name='order-create'),
    path('brand-assets/',  BrandAssetView.as_view(),     name='brand-assets'),
    path('events/',        EventPromoListView.as_view(), name='events-list'),
    path('jobs/',          JobPostingListView.as_view(),  name='jobs-list'),

    # Admin
    path('admin/stats/',                              AdminStatsView.as_view()),
    path('admin/orders/',                             AdminOrderListView.as_view()),
    path('admin/orders/<int:pk>/status/',             AdminOrderStatusUpdateView.as_view()),
    path('admin/menu-items/',                         AdminMenuItemListCreateView.as_view()),
    path('admin/menu-items/<int:pk>/',                AdminMenuItemDetailView.as_view()),
    path('admin/menu-items/<int:item_pk>/options/',   AdminMenuItemOptionCreateView.as_view()),
    path('admin/options/<int:pk>/',                   AdminMenuItemOptionDeleteView.as_view()),
    path('admin/categories/',                         AdminCategoryListCreateView.as_view()),
    path('admin/categories/<int:pk>/',                AdminCategoryDetailView.as_view()),
    path('admin/events/',                             AdminEventListCreateView.as_view()),
    path('admin/events/<int:pk>/',                    AdminEventDetailView.as_view()),
    path('admin/jobs/',                               AdminJobListCreateView.as_view()),
    path('admin/jobs/<int:pk>/',                      AdminJobDetailView.as_view()),
    path('admin/subcategories/',                      AdminSubCategoryListCreateView.as_view()),
    path('admin/subcategories/<int:pk>/',             AdminSubCategoryDetailView.as_view()),
]
