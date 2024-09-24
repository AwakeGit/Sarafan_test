from django.core.management.base import BaseCommand
from products.models import Category, SubCategory, Product


class Command(BaseCommand):
    """Удаление основных данных: категорий, подкатегорий и продуктов"""

    def handle(self, *args, **kwargs):
        """Удаление основных данных: категорий, подкатегорий и продуктов"""
        Product.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Все продукты удалены'))
        SubCategory.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Все подкатегории удалены'))
        Category.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Все категории удалены'))
        self.stdout.write(self.style.SUCCESS('Данные успешно удалены из базы'))
