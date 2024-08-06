from django.urls import path
from .views import *
urlpatterns = [
    path('', MainPage.as_view(), name='main-page'),
    path('results/', SearchView.as_view(), name='search'),
    path('<str:language>/', LanguageList.as_view(), name='language-page'),
    path('<str:language>/<int:pk>/', DetailTopic.as_view(), name='detail-topic'),

]
