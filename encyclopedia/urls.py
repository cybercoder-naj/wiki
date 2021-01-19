from django.urls import path
from . import views

app_name = 'encyclopedia'
urlpatterns = [
    path('', views.index, name="index"),
    path('wiki/new_page', views.new_page, name='new_page'),
    path('wiki/random_page', views.random_page, name='random_page'),
    path('wiki/edit_page/<str:title>', views.edit_page, name='edit_page'),
    path('wiki/<str:title>', views.entry_page, name='entry_page')
]
