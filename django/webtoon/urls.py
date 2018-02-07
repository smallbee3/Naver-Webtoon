from django.urls import path

from . import views

app_name = 'webtoon'
urlpatterns = [

    path('', views.webtoon_list, name='list'),
    path('<int:pk>/', views.webtoon_detail, name='detail'),

]