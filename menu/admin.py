from django.contrib import admin
from .models import Category, SubCategory, MenuItem, MenuItemOption, Order, OrderItem, BrandAsset, EventPromo, JobPosting


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)


class MenuItemOptionInline(admin.TabularInline):
    model = MenuItemOption
    extra = 1

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'subcategory', 'price', 'is_available')
    list_filter = ('is_available', 'category', 'subcategory')
    search_fields = ('name', 'description')
    inlines = [MenuItemOptionInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    raw_id_fields = ('menu_item', 'selected_option')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'phone_number', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer_name', 'phone_number', 'delivery_address')
    inlines = [OrderItemInline]
    ordering = ('-created_at',)


@admin.register(BrandAsset)
class BrandAssetAdmin(admin.ModelAdmin):
    pass

@admin.register(EventPromo)
class EventPromoAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')

@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
