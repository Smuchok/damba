from django.urls import path, include

from .views import *

urlpatterns = [
    path('', index, name='main'), # http://127.0.0.1:8000/
    path('contact/', contact, name='contact'),

    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),

    path('houses/', houses, name='houses'),
    path('houses/<int:house_id>/', show_house, name='house'),
    path('houses/<int:house_id>/order/', order_house, name='order_house'),

    path('post/<int:post_id>/', show_post, name='post'),
    path('category/<int:cat_id>/', show_category, name='category'),

    path('test/<int:test_id>/', testpage), # http://127.0.0.1:8000/test/

    # django-debug-toolbar
    path('__debug__/', include('debug_toolbar.urls')),
]
