from django.http.response import Http404
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound

from django.utils.safestring import mark_safe
from django.core.paginator import Paginator

from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout


from django.template.defaulttags import register
@register.filter
def get_range(value):
    return range(value)

import os
from datetime import date, datetime, timedelta

from .models import *
from .forms import *

# Create your views here.
menu = [
    {'title':"Контакти", 'url_name':'/contact'},
    {'title':"Будинки", 'url_name':'/houses'},
    # {'title':"Увійти", 'url_name':'/admin'},
    ]
map_legend = {
    'name':"Карта",
    'legend':['Парковка', 'Рецепшн', 'Дитяча площадка', 'Пляж', 'Вольєр з оленями', 'Адміністративна споруда', 'Адміністративна споруда'],
    }

def index(request): #HttpRequest
    posts = Price.objects.all()
    cats = Category.objects.all()
    context = {
        'menu':menu,
        'title':'Головна',
        'map_legend':map_legend,

        'posts':posts,
        'cats':cats,
        'cat_selected':0
        }
    return render(request, 'main/index.html', context=context)

def contact(request):
    context = {'menu':menu, 'title':'Контакти'}
    return render(request, 'main/contact.html', context=context)

def show_post(request, post_id):
    return HttpResponse(f"Пост ід = {post_id}\n{Price.objects.get(id=post_id).cat_id}")

def show_category(request, cat_id):
    # return HttpResponse(f"Кат ід = {cat_id}")
    posts = Price.objects.filter(cat_id=cat_id)
    cats = Category.objects.all()

    if len(posts) == 0:
        raise Http404

    context = {
        'menu':menu,
        'title':'По категоріям',
        'map_legend':map_legend,

        'posts':posts,
        'cats':cats,
        'cat_selected':cat_id
        }
    return render(request, 'main/index.html', context=context)


def houses(request):
    cards = Houses.objects.all()

    paginator = Paginator(cards, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title':'Будинки',
        'menu':menu,
        'cards':cards,
        'page_obj':page_obj,
    }
    return render(request, 'main/houses.html', context=context)

def get_photos_house(house_id):
    # files = os.listdir(os.getcwd() + '/static/main/img/houses')
    files = os.listdir('C:/D/Cursova/Django/site/damba/main/static/main/img/houses')
    c, photos = 0, []
    for i in files:
        c += 1
        file = 'house_' + str(house_id) + '_' + str(c) + '.jpg'
        if file in files:
            photos.append(file)
        else:
            pass
    return photos


def show_house(request, house_id):
    info = Houses.objects.get(id=house_id)

    context = {
        'title':f'Будинок {house_id} - {info.name}',
        'menu':menu,
        'info':info,
        'photos':get_photos_house(house_id),
    }
    return render(request, 'main/house_details.html', context=context)

def order_house(request, house_id):
    info = Houses.objects.get(id=house_id)
    infos = Houses.objects.all()
    book_dates = Book.objects.filter(house=house_id)

    def save_client(f:object):
        first_name = f['first_name']
        last_name = f['last_name']
        phone_number = f['phone']
        email = f['email']
        try:
            Clients.objects.get(email=email)
            print('ТАКИЙ email ВЖЕ Є')
        except Clients.DoesNotExist:
            client = Clients(first_name=first_name, last_name=last_name, phone_number=phone_number, email=email)
            client.save()
        print('SAVED client')
    def save_book(f:object):
        email = f['email']
        client = Clients.objects.get(email=email)
        house = Houses.objects.get(id=house_id)
        # date_booking = 
        count_of_days = f['count_of_days']
        date_future_settlment = f['date_future_settlment']
        date_future_checkout = date_future_settlment + timedelta(days=count_of_days)
        book = Book(client=client, house=house, date_future_settlment=date_future_settlment, date_future_checkout=date_future_checkout)
        book.save()
        print('SAVED book')

    def make_dates_arr(book_dates:list) -> list:
        dates_arr = []
        for bd in book_dates:
            date1, date2 = bd.date_future_settlment, bd.date_future_checkout
            days = (date2 - date1).days
            print(f'{date1} -- {date2} -> {days}')
            date_arr = []
            for i in range(days):
                date2 -= timedelta(days=1)
                date_arr.append(date2)
            dates_arr.append(date_arr)
        # print(date)
        return dates_arr
    dates_arr = make_dates_arr(book_dates)

    if request.method == 'POST':
        form = OrderHouse(request.POST)
        if form.is_valid():
            f = form.cleaned_data
            print('  Валідована форма:', f)
            save_client(f)
            save_book(f)
        else:
            print('  НE валідована форма:', form.cleaned_data)
    else:
        form = OrderHouse()

    context = {
        'title':f"Замовлення будинку {house_id} - {info.name}",
        'menu':menu,
        'info':info,

        'form':form,
        'infos':infos,
        'book_dates':dates_arr,
    }
    return render(request, 'main/order_house.html', context=context)

def register_user(request):
    form = RegisterUserForm # UserCreationForm

    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    context = {
        'title':"Реєстрація",
        'menu':menu,
        'form':form,
    }
    return render(request, 'main/register.html', context=context)

def login_user(request):
    form = LoginUserForm # AuthenticationForm
    # import pdb; pdb.set_trace() #debug

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('houses')

    context = {
        'title':"Вхід",
        'menu':menu,
        'form':form,
        'success':'УСПІШНО',
    }
    return render(request, 'main/login.html', context=context)

def logout_user(request):
    logout(request)
    return redirect('main')

def testpage(request, test_id):
    return HttpResponse(f"Сторінка testpage {test_id}")


# для 404
def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Сторінку не знайдено</h1></br><a href="http://192.168.0.100:8000/"><h3>Головна</h3></a>')