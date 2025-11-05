from django.contrib import admin
from .models import Anime, FavoriteAnime


@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'score', 'episodes', 'is_favorite', 'created_at')
    list_filter = ('type', 'is_favorite', 'created_at')
    search_fields = ('title',)
    ordering = ('-created_at',)


@admin.register(FavoriteAnime)
class FavoriteAnimeAdmin(admin.ModelAdmin):
    list_display = ('title', 'mal_id', 'type', 'score', 'episodes', 'created_at')
    list_filter = ('type', 'created_at')
    search_fields = ('title',)
    ordering = ('-created_at',)
