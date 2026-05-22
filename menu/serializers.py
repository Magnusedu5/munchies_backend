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
        fields = ['id', 'name', 'description', 'price', 'image', 'is_available', 'recommended', 'options', 'subcategory']


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


# ── Admin serializers ──────────────────────────────────────────────────

class AdminOrderItemSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.CharField(source='menu_item.name', read_only=True)
    option_name = serializers.SerializerMethodField()

    def get_option_name(self, obj):
        return obj.selected_option.name if obj.selected_option else None

    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item_name', 'option_name', 'quantity', 'price_at_purchase']


class AdminOrderSerializer(serializers.ModelSerializer):
    order_items = AdminOrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'phone_number', 'delivery_address',
                  'total_amount', 'status', 'created_at', 'order_items']


class AdminOrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']


class AdminSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'category']


class AdminMenuItemOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItemOption
        fields = ['id', 'name', 'price']


class AdminMenuItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    subcategory_name = serializers.SerializerMethodField()
    options = AdminMenuItemOptionSerializer(many=True, read_only=True)

    def get_subcategory_name(self, obj):
        return obj.subcategory.name if obj.subcategory else None

    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price', 'image', 'is_available',
                  'recommended', 'category', 'category_name', 'subcategory',
                  'subcategory_name', 'options']


class AdminCategorySerializer(serializers.ModelSerializer):
    item_count = serializers.SerializerMethodField()

    def get_item_count(self, obj):
        return obj.menu_items.count()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image', 'item_count']


class AdminEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventPromo
        fields = '__all__'


class AdminJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPosting
        fields = '__all__'