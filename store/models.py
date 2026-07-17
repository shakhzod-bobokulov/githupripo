from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField("Nomi", max_length=100)
    slug = models.SlugField("Slug", max_length=100, unique=True)

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE,
        verbose_name="Kategoriya",
    )
    name = models.CharField("Nomi", max_length=200)
    slug = models.SlugField("Slug", max_length=200, unique=True)
    description = models.TextField("Tavsif", blank=True)
    price = models.DecimalField("Narxi", max_digits=10, decimal_places=0)
    icon = models.CharField(
        "Emoji belgisi", max_length=8, default="🛒",
        help_text="Rasm yuklanmagan bo'lsa shu emoji ko'rsatiladi",
    )
    image = models.ImageField("Rasm", upload_to="products/", blank=True, null=True)
    in_stock = models.BooleanField("Mavjud", default=True)
    created_at = models.DateTimeField("Qo'shilgan sana", auto_now_add=True)

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.slug])


class ContactMessage(models.Model):
    name = models.CharField("Ism", max_length=100)
    phone = models.CharField("Telefon", max_length=30)
    message = models.TextField("Xabar", blank=True)
    created_at = models.DateTimeField("Yuborilgan sana", auto_now_add=True)

    class Meta:
        verbose_name = "Xabar"
        verbose_name_plural = "Xabarlar"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.phone})"


class Order(models.Model):
    STATUS_CHOICES = [
        ("new", "Yangi"),
        ("processing", "Jarayonda"),
        ("done", "Bajarildi"),
        ("cancelled", "Bekor qilindi"),
    ]

    full_name = models.CharField("Ism familiya", max_length=150)
    phone = models.CharField("Telefon", max_length=30)
    address = models.CharField("Manzil", max_length=255)
    note = models.TextField("Izoh", blank=True)
    status = models.CharField("Holati", max_length=20, choices=STATUS_CHOICES, default="new")
    created_at = models.DateTimeField("Buyurtma sanasi", auto_now_add=True)

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Buyurtma #{self.pk} — {self.full_name}"

    @property
    def total_price(self):
        return sum(item.line_total for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="+", on_delete=models.PROTECT)
    price = models.DecimalField("Narxi", max_digits=10, decimal_places=0)
    quantity = models.PositiveIntegerField("Miqdori", default=1)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def line_total(self):
        return self.price * self.quantity
