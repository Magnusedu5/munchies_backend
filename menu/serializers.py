from rest_framework import serializers
from .models import Category, SubCategory, MenuItem, MenuItemOption, Order, OrderItem, BrandAsset, EventPromo, JobPosting


class MenuItemOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItemOption
        fields = ['id', 'name', 'price']

class MenuItemSerializer(serializers.ModelSerializer):
    options = MenuItemOptionSerializer(many=True, read_only=True)
    subcategory = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price', 'image', 'is_available', 'options', 'subcategory']


class CategorySerializer(serializers.ModelSerializer):
    menu_items = MenuItemSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image', 'menu_items']


class OrderTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'status', 'customer_name']

class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['menu_item', 'selected_option', 'quantity', 'price_at_purchase']

class OrderCreateSerializer(serializers.ModelSerializer):
    order_items = OrderItemCreateSerializer(many=True)

    class Meta:
        model = Order
        fields = ['customer_name', 'phone_number', 'delivery_address', 'total_amount', 'order_items']

    def create(self, validated_data):
        items_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

class BrandAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandAsset
        fields = '__all__'

class EventPromoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventPromo
        fields = '__all__'

class JobPostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPosting
        fields = '__all__'