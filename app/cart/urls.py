from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.BasketView.as_view(), name='basket')
]
