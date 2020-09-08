from django.urls import path
from minesweeper.views import MainPageView


urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),
]
