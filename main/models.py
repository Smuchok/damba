from django.db import models
from django.urls import reverse

# Create your models here.
# З уроків ютубу
class Price(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d", blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True) # cat_id

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id':self.pk})

    class Meta:
        verbose_name = 'Відомі жінки'
        verbose_name_plural = 'Відомі жінки (ютуб)'
        ordering = ['time_create', 'title']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_id':self.pk})

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії (ютуб)'
        ordering = ['id']


# Основні моделі

class Houses(models.Model):
    name = models.CharField(max_length=32)
    photo = models.ImageField(null=True, blank=True) #
    price = models.FloatField()
    capacity = models.IntegerField()
    rooms = models.IntegerField(null=True) #
    beds = models.IntegerField()
    wifi = models.BooleanField(default=True)
    kitchen = models.BooleanField(default=True)
    bathroom = models.BooleanField(default=True)
    floors = models.IntegerField()
    central_heat = models.BooleanField(default=False) #
    pets_allow = models.BooleanField(default=False) #
    description = models.CharField(max_length= 255, null=True) #


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('house', kwargs={'house_id':self.pk})

    class Meta:
        verbose_name = 'Будинок'
        verbose_name_plural = 'Будинки'
        ordering = ['id']


class Clients(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    phone_number = models.IntegerField()
    email = models.EmailField()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Клієнт'
        verbose_name_plural = 'Клієнти'
        ordering = ['-id']


class Book(models.Model):
    client = models.ForeignKey('Clients', on_delete=models.PROTECT) # client_id
    house = models.ForeignKey('Houses', on_delete=models.PROTECT)   # house_id
    date_booking = models.DateTimeField(auto_now=True)           # Дата бронювання
    date_future_settlment = models.DateTimeField()  # Дата майбутнього заселення
    date_future_checkout = models.DateTimeField()   # Дата майбутнього виселення

    # def __str__(self):
    #     return self.pk

    class Meta:
        verbose_name = 'Бронювання'
        verbose_name_plural = 'Бронювання'
        ordering = ['-date_future_settlment']


class Settlment(models.Model):
    book = models.ForeignKey('Book', on_delete=models.PROTECT, null=True) # # book_id
    client = models.ForeignKey('Clients', on_delete=models.PROTECT) # client_id
    house = models.ForeignKey('Houses', on_delete=models.PROTECT)   # house_id
    date_of_settlment = models.DateTimeField()  # Дата фактичного заселення
    date_of_checkout = models.DateTimeField()   # Дата фактичного виселення

    # def __str__(self):
    #     return self.pk

    class Meta:
        verbose_name = 'Заселення'
        verbose_name_plural = 'Заселення'
        ordering = ['-date_of_settlment']

