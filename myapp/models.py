from django.db import models


class Anime(models.Model):
    TYPE_CHOICES = [
        ('TV', 'TV'),
        ('Movie', 'Película'),
        ('OVA', 'OVA'),
        ('Other', 'Otro'),
    ]

    title = models.CharField(max_length=200, verbose_name="Título")
    score = models.DecimalField(max_digits=4, decimal_places=2, default=0.00, verbose_name="Puntuación")
    episodes = models.IntegerField(default=0, verbose_name="Episodios")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='TV', verbose_name="Tipo")
    image_url = models.URLField(max_length=500, verbose_name="URL de la Imagen")
    is_favorite = models.BooleanField(default=False, verbose_name="Favorito")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última actualización")

    class Meta:
        verbose_name = "Anime"
        verbose_name_plural = "Animes"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class FavoriteAnime(models.Model):

    mal_id = models.IntegerField(unique=True, verbose_name="ID de MyAnimeList")
    title = models.CharField(max_length=200, verbose_name="Título")
    image_url = models.URLField(max_length=500, verbose_name="URL de la Imagen")
    score = models.DecimalField(max_digits=4, decimal_places=2, default=0.00, verbose_name="Puntuación")
    episodes = models.IntegerField(default=0, verbose_name="Episodios")
    type = models.CharField(max_length=20, default='TV', verbose_name="Tipo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    class Meta:
        verbose_name = "Anime Favorito (API)"
        verbose_name_plural = "Animes Favoritos (API)"
        ordering = ['-created_at']

    def __str__(self):
        return self.title
