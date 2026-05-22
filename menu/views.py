from django.shortcuts import get_object_or_404
from django.db.models import Sum, Count
from django.utils import timezone
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as drf_status

from .models import Category, SubCategory, MenuItem, MenuItemOption, Order, BrandAsset, EventPromo, JobPosting
from .serializers import (
    CategorySerializer, OrderTrackingSerializer, BrandAssetSerializer,
    EventPromoSerializer, JobPostingSerializer, OrderCreateSerializer,
    AdminOrderSerializer, AdminOrderStatusSerializer,
    AdminMenuItemSerializer, AdminMenuItemOptionSerializer,
    AdminSubCategorySerializer, AdminCategorySerializer, AdminEventSerializer, AdminJobSerializer,
)


# ── Public views ───────────────────────────────────────────────────────────────

class MenuListView(generics.ListAPIView):
    queryset = Category.objects.prefetch_related('menu_items__options').all()
    serializer_class = CategorySerializer


class OrderTrackingView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderTrackingSerializer


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer


class BrandAssetView(APIView):
    def get(self, request):
        asset = BrandAsset.objects.first()
        if asset:
            return Response(BrandAssetSerializer(asset, context={'request': request}).data)
        return Response({})


class EventPromoListView(generics.ListAPIView):
    queryset = EventPromo.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = EventPromoSerializer


class JobPostingListView(generics.ListAPIView):
    queryset = JobPosting.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = JobPostingSerializer


# ── Admin views ────────────────────────────────────────────────────────────────

class AdminStatsView(APIView):
    def get(self, request):
        today = timezone.now().date()
        breakdown = dict(
            Order.objects.values('status').annotate(c=Count('id')).values_list('status', 'c')
        )
        recent = Order.objects.prefetch_related(
            'order_items__menu_item', 'order_items__selected_option'
        ).order_by('-created_at')[:8]

        return Response({
            'total_orders':      Order.objects.count(),
            'total_revenue':     str(Order.objects.exclude(status='Cancelled').aggregate(s=Sum('total_amount'))['s'] or 0),
            'today_orders':      Order.objects.filter(created_at__date=today).count(),
            'today_revenue':     str(Order.objects.filter(created_at__date=today).exclude(status='Cancelled').aggregate(s=Sum('total_amount'))['s'] or 0),
            'pending_count':     breakdown.get('Pending', 0),
            'processing_count':  breakdown.get('Processing', 0),
            'delivery_count':    breakdown.get('Out for Delivery', 0),
            'delivered_count':   breakdown.get('Delivered', 0),
            'cancelled_count':   breakdown.get('Cancelled', 0),
            'status_breakdown':  breakdown,
            'recent_orders':     AdminOrderSerializer(recent, many=True).data,
        })


class AdminOrderListView(generics.ListAPIView):
    serializer_class = AdminOrderSerializer

    def get_queryset(self):
        qs = Order.objects.prefetch_related(
            'order_items__menu_item', 'order_items__selected_option'
        ).order_by('-created_at')
        s = self.request.query_params.get('status')
        if s:
            qs = qs.filter(status=s)
        return qs


class AdminOrderStatusUpdateView(generics.UpdateAPIView):
    serializer_class = AdminOrderStatusSerializer
    queryset = Order.objects.all()
    http_method_names = ['patch']


class AdminMenuItemListCreateView(generics.ListCreateAPIView):
    serializer_class = AdminMenuItemSerializer
    queryset = MenuItem.objects.select_related('category', 'subcategory').prefetch_related('options').all()


class AdminMenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AdminMenuItemSerializer
    queryset = MenuItem.objects.select_related('category', 'subcategory').prefetch_related('options').all()
    http_method_names = ['get', 'patch', 'delete']


class AdminMenuItemOptionCreateView(generics.CreateAPIView):
    serializer_class = AdminMenuItemOptionSerializer

    def perform_create(self, serializer):
        item = get_object_or_404(MenuItem, pk=self.kwargs['item_pk'])
        serializer.save(menu_item=item)


class AdminMenuItemOptionDeleteView(generics.DestroyAPIView):
    queryset = MenuItemOption.objects.all()


class AdminCategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = AdminCategorySerializer
    queryset = Category.objects.all()


class AdminCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AdminCategorySerializer
    queryset = Category.objects.all()
    http_method_names = ['get', 'patch', 'delete']


class AdminEventListCreateView(generics.ListCreateAPIView):
    serializer_class = AdminEventSerializer
    queryset = EventPromo.objects.all().order_by('-created_at')


class AdminEventDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AdminEventSerializer
    queryset = EventPromo.objects.all()
    http_method_names = ['get', 'patch', 'delete']


class AdminJobListCreateView(generics.ListCreateAPIView):
    serializer_class = AdminJobSerializer
    queryset = JobPosting.objects.all().order_by('-created_at')


class AdminJobDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AdminJobSerializer
    queryset = JobPosting.objects.all()
    http_method_names = ['get', 'patch', 'delete']


class AdminSubCategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = AdminSubCategorySerializer

    def get_queryset(self):
        qs = SubCategory.objects.all()
        cat = self.request.query_params.get('category')
        if cat:
            qs = qs.filter(category=cat)
        return qs


class AdminSubCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = AdminSubCategorySerializer
    http_method_names = ['get', 'patch', 'delete']
