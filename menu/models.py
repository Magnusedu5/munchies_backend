from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to='brand_images/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Subcategories'

    def __str__(self):
        return f"{self.category.name} - {self.name}"


class MenuItem(models.Model):
    category = models.ForeignKey(Category, related_name='menu_items', on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, related_name='menu_items', on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class MenuItemOption(models.Model):
    menu_item = models.ForeignKey(MenuItem, related_name='options', on_delete=models.CASCADE)
    name = models.CharField(max_length=100) # e.g., "6pcs", "12pcs"
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.menu_item.name} - {self.name}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    customer_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    delivery_address = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} by {self.customer_name}"

    @property
    def calculated_total(self):
        return sum(item.price_at_purchase * item.quantity for item in self.order_items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(MenuItemOption, blank=True, null=True, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField(default=1)
    price_at_purchase = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    def __str__(self):
        if self.selected_option:
            return f"{self.quantity} x {self.menu_item.name} ({self.selected_option.name}) (Order #{self.order.id})"
        return f"{self.quantity} x {self.menu_item.name} (Order #{self.order.id})"


class BrandAsset(models.Model):
    logo = models.ImageField(upload_to='brand/', blank=True, null=True)
    header_image = models.ImageField(upload_to='brand/', blank=True, null=True)
    background_video = models.FileField(upload_to='brand/videos/', blank=True, null=True)

    def __str__(self):
        return "Brand Assets (Update this to change brand graphics)"

class EventPromo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class JobPosting(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
