from django.contrib import admin
from django.urls import path
from myapp.views import (
    AnimeListView,
    AnimeDetailView,
    AnimeCreateView,
    AnimeUpdateView,
    AnimeDeleteView,
    toggle_favorite
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', AnimeListView.as_view(), name='anime_list'),
    path('anime/create/', AnimeCreateView.as_view(), name='anime_create'),
    path('anime/<int:pk>/', AnimeDetailView.as_view(), name='anime_detail'),
    path('anime/<int:pk>/edit/', AnimeUpdateView.as_view(), name='anime_update'),
    path('anime/<int:pk>/delete/', AnimeDeleteView.as_view(), name='anime_delete'),
    path('api/toggle-favorite/', toggle_favorite, name='toggle_favorite'),
]