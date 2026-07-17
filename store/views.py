from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .cart import Cart
from .forms import ContactForm, OrderForm
from .models import Category, Order, OrderItem, Product


def _parse_quantity(raw, default=1):
    try:
        return int(raw)
    except (TypeError, ValueError):
        return default


def home(request):
    context = {
        "categories": Category.objects.all(),
        "featured_products": Product.objects.filter(in_stock=True)[:8],
        "contact_form": ContactForm(),
    }
    return render(request, "store/home.html", context)


def product_list(request):
    products = Product.objects.filter(in_stock=True)
    category_slug = request.GET.get("category")
    query = request.GET.get("q")
    active_category = None

    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=active_category)

    if query:
        products = products.filter(name__icontains=query)

    paginator = Paginator(products, 9)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "categories": Category.objects.all(),
        "page_obj": page_obj,
        "active_category": active_category,
        "query": query or "",
    }
    return render(request, "store/product_list.html", context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    related = Product.objects.filter(category=product.category, in_stock=True).exclude(pk=product.pk)[:4]
    context = {"product": product, "related_products": related}
    return render(request, "store/product_detail.html", context)


def cart_detail(request):
    return render(request, "store/cart.html", {"cart": Cart(request)})


@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, pk=product_id, in_stock=True)
    quantity = _parse_quantity(request.POST.get("quantity"))
    Cart(request).add(product, quantity=max(quantity, 1))
    messages.success(request, f"“{product.name}” savatga qo'shildi.")

    next_url = request.POST.get("next")
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect(next_url)
    return redirect("store:cart_detail")


@require_POST
def cart_update(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    quantity = _parse_quantity(request.POST.get("quantity"))
    Cart(request).set_quantity(product, quantity)
    return redirect("store:cart_detail")


@require_POST
def cart_remove(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    Cart(request).remove(product)
    messages.info(request, f"“{product.name}” savatdan o'chirildi.")
    return redirect("store:cart_detail")


def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, "Savatingiz bo'sh. Buyurtma berish uchun avval mahsulot tanlang.")
        return redirect("store:product_list")

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            OrderItem.objects.bulk_create([
                OrderItem(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )
                for item in cart
            ])
            cart.clear()
            return redirect("store:order_success", order_id=order.id)
    else:
        form = OrderForm()

    return render(request, "store/checkout.html", {"form": form, "cart": cart})


def order_success(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, "store/order_success.html", {"order": order})


@require_POST
def contact_submit(request):
    form = ContactForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Xabaringiz yuborildi! Tez orada siz bilan bog'lanamiz.")
    else:
        messages.error(request, "Xabarni yuborishda xatolik. Iltimos, ma'lumotlarni tekshiring.")
    return redirect(reverse("store:home") + "#contact")
