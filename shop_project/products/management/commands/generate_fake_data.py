import random

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker
from products.models import Category, SubCategory, Product


class Command(BaseCommand):
    """
    Команда для генерации данных: категорий, подкатегорий и продуктов
    """

    def handle(self, *args, **kwargs):
        """Генерируем данные"""
        fake = Faker(
            'ru_RU')

        def generate_unique_slug(model_class, base_name):
            """Генерируем уникальный slug"""
            slug = slugify(base_name)
            if model_class.objects.filter(slug=slug).exists():
                slug = f'{slug}-{random.randint(0, 9999)}'

        categories_data = {
            'Фрукты': ['Яблоки', 'Бананы', 'Груши', 'Апельсины'],
            'Овощи': ['Картофель', 'Морковь', 'Огурцы', 'Томаты'],
            'Молочные продукты': ['Молоко', 'Сыр', 'Творог', 'Йогурт'],
            'Хлебобулочные изделия': ['Хлеб', 'Батон', 'Булочки', 'Круассаны'],
            'Напитки': ['Вода', 'Сок', 'Чай', 'Кофе']
        }

        for category_name, subcategories in categories_data.items():
            category_slug = generate_unique_slug(Category, category_name)
            category = Category.objects.create(
                name=category_name,
                slug=category_slug,
                image=fake.image_url()
            )

            for subcategory_name in subcategories:
                subcategory_slug = generate_unique_slug(
                    SubCategory,
                    subcategory_name
                )
                subcategory = SubCategory.objects.create(
                    name=subcategory_name,
                    slug=subcategory_slug,
                    image=fake.image_url(),
                    parent_category=category
                )

                products = {
                    'Яблоки': ['Красные яблоки', 'Зеленые яблоки', 'Гала',
                               'Фуджи'],
                    'Бананы': ['Спелые бананы', 'Зеленые бананы'],
                    'Груши': ['Конференс', 'Комис'],
                    'Апельсины': ['Апельсины без косточек',
                                  'Апельсины с косточками'],
                    'Картофель': ['Красный картофель', 'Белый картофель'],
                    'Морковь': ['Морковь свежая', 'Морковь в сетке'],
                    'Огурцы': ['Огурцы свежие', 'Огурцы маринованные'],
                    'Томаты': ['Томаты черри', 'Томаты крупные'],
                    'Молоко': ['Молоко 2.5%', 'Молоко 3.2%'],
                    'Сыр': ['Сыр твердый', 'Сыр плавленый'],
                    'Творог': ['Творог 5%', 'Творог обезжиренный'],
                    'Йогурт': ['Йогурт с фруктами', 'Натуральный йогурт'],
                    'Хлеб': ['Ржаной хлеб', 'Пшеничный хлеб'],
                    'Батон': ['Батон нарезной', 'Батон классический'],
                    'Булочки': ['Булочки с маком', 'Булочки с сахаром'],
                    'Круассаны': ['Круассаны с шоколадом',
                                  'Круассаны с маслом'],
                    'Вода': ['Минеральная вода', 'Газированная вода'],
                    'Сок': ['Апельсиновый сок', 'Яблочный сок'],
                    'Чай': ['Черный чай', 'Зеленый чай'],
                    'Кофе': ['Растворимый кофе', 'Молотый кофе']
                }

                if subcategory_name in products:
                    for product_name in products[subcategory_name]:
                        product_slug = generate_unique_slug(
                            Product,
                            product_name
                        )
                        Product.objects.create(
                            name=product_name,
                            slug=product_slug,
                            price=random.uniform(50, 1000),
                            image_small=fake.image_url(),
                            image_medium=fake.image_url(),
                            image_large=fake.image_url(),
                            subcategory=subcategory
                        )

        self.stdout.write(self.style.SUCCESS('Данные успешно загружены в базу'))
