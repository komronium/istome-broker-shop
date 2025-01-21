from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название категории')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='children',
                               verbose_name='Родительская категория')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        db_table = 'categories'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def product_count(self):
        count = self.products.count()
        for child in self.children.all():
            count += child.product_count
        return count


class Product(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название продукта')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True,
                                 verbose_name='Категория',
                                 related_name='products')
    sku = models.PositiveIntegerField(verbose_name='Артикул')
    price = models.PositiveIntegerField(verbose_name='Цена')
    old_price = models.PositiveIntegerField(null=True, blank=True, verbose_name='Старая цена')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество на складе')

    class Meta:
        db_table = 'products'
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['name']

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'product_images'
        ordering = ['created_at']
        verbose_name = 'Изображение продукта'
        verbose_name_plural = 'Изображения продукта'
