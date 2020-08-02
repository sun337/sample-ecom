from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.BasketRetrieveCreate.as_view(), name='basket')
]
