from django.db import migrations


CATEGORIES = [
    {"name": "Oziq-ovqat", "slug": "oziq-ovqat"},
    {"name": "Kiyim-kechak", "slug": "kiyim"},
    {"name": "Elektronika", "slug": "elektronika"},
    {"name": "Uy-ro'zg'or", "slug": "uy"},
]

PRODUCTS = [
    {"name": "Olma", "slug": "olma", "category": "oziq-ovqat", "price": 12000, "icon": "🍎",
     "description": "Yangi, shirin qizil olma 1kg"},
    {"name": "Non", "slug": "non", "category": "oziq-ovqat", "price": 3000, "icon": "🍞",
     "description": "Issiq, yangi pishirilgan non"},
    {"name": "Sut", "slug": "sut", "category": "oziq-ovqat", "price": 9000, "icon": "🥛",
     "description": "Tabiiy sigir suti 1L"},
    {"name": "Erkaklar futbolkasi", "slug": "erkaklar-futbolkasi", "category": "kiyim", "price": 65000, "icon": "👕",
     "description": "100% paxta, turli ranglarda"},
    {"name": "Ayollar ko'ylagi", "slug": "ayollar-koylagi", "category": "kiyim", "price": 120000, "icon": "👗",
     "description": "Yozgi yengil ko'ylak"},
    {"name": "Krossovka", "slug": "krossovka", "category": "kiyim", "price": 250000, "icon": "👟",
     "description": "Qulay va sport krossovkasi"},
    {"name": "Simsiz quloqchin", "slug": "simsiz-quloqchin", "category": "elektronika", "price": 180000, "icon": "🎧",
     "description": "Bluetooth 5.0, kuchli tovush"},
    {"name": "Quvvatlovchi batareya", "slug": "quvvatlovchi-batareya", "category": "elektronika", "price": 150000, "icon": "🔋",
     "description": "10000mAh, tez zaryadlash"},
    {"name": "Aqlli soat", "slug": "aqlli-soat", "category": "elektronika", "price": 320000, "icon": "⌚",
     "description": "Fitnes va bildirishnomalar"},
    {"name": "Choy dastavkasi", "slug": "choy-dastavkasi", "category": "uy", "price": 95000, "icon": "🫖",
     "description": "Keramik, 6 kishilik"},
    {"name": "Yostiq", "slug": "yostiq", "category": "uy", "price": 45000, "icon": "🛏️",
     "description": "Yumshoq, gipoallergen"},
    {"name": "Oshxona pichog'i", "slug": "oshxona-pichogi", "category": "uy", "price": 38000, "icon": "🔪",
     "description": "Zanglamaydigan po'lat"},
]


def seed_data(apps, schema_editor):
    Category = apps.get_model("store", "Category")
    Product = apps.get_model("store", "Product")

    category_objs = {}
    for cat in CATEGORIES:
        obj, _ = Category.objects.get_or_create(slug=cat["slug"], defaults={"name": cat["name"]})
        category_objs[cat["slug"]] = obj

    for prod in PRODUCTS:
        Product.objects.get_or_create(
            slug=prod["slug"],
            defaults={
                "name": prod["name"],
                "category": category_objs[prod["category"]],
                "price": prod["price"],
                "icon": prod["icon"],
                "description": prod["description"],
            },
        )


def remove_data(apps, schema_editor):
    Category = apps.get_model("store", "Category")
    Product = apps.get_model("store", "Product")
    Product.objects.filter(slug__in=[p["slug"] for p in PRODUCTS]).delete()
    Category.objects.filter(slug__in=[c["slug"] for c in CATEGORIES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_data, remove_data),
    ]
