from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('gallery/', views.gallery, name='gallery'),
    path('faq/', views.faq, name='faq'),
    path('order/', views.make_order, name='make_order'),
    path('personal/', views.personal_page, name='personal_page'),
]
