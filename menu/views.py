from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category, Order, BrandAsset, EventPromo, JobPosting
from .serializers import CategorySerializer, OrderTrackingSerializer, BrandAssetSerializer, EventPromoSerializer, JobPostingSerializer, OrderCreateSerializer


class MenuListView(generics.ListAPIView):
    queryset = Category.objects.prefetch_related('menu_items').all()
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
            serializer = BrandAssetSerializer(asset, context={'request': request})
            return Response(serializer.data)
        return Response({})

class EventPromoListView(generics.ListAPIView):
    queryset = EventPromo.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = EventPromoSerializer

class JobPostingListView(generics.ListAPIView):
    queryset = JobPosting.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = JobPostingSerializer
