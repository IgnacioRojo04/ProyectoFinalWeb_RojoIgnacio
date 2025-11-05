import requests
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Anime, FavoriteAnime

class AnimeListView(TemplateView):

    template_name = 'myapp/anime_list.html'
    api_url = "https://api.jikan.moe/v4/top/anime"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        show_favorites_only = self.request.GET.get('favorites', 'false') == 'true'
        all_animes = []

        favorite_api_ids = set(FavoriteAnime.objects.values_list('mal_id', flat=True))
        if show_favorites_only:
            local_animes = Anime.objects.filter(is_favorite=True)
        else:
            local_animes = Anime.objects.all()

        for anime in local_animes:
            all_animes.append({
                'mal_id': anime.id,
                'title': anime.title,
                'score': float(anime.score),
                'episodes': anime.episodes,
                'type': anime.type,
                'images': {
                    'jpg': {
                        'image_url': anime.image_url
                    }
                },
                'is_local': True,
                'is_favorite': anime.is_favorite
            })

        try:
            response = requests.get(self.api_url, timeout=5)
            response.raise_for_status()

            data = response.json()
            anime_data = data.get('data', [])

            print(f"API respondió con {len(anime_data)} animes")

            for anime in anime_data:
                anime['is_local'] = False
                anime['is_favorite'] = anime['mal_id'] in favorite_api_ids

            if show_favorites_only:
                anime_data = [anime for anime in anime_data if anime['is_favorite']]

            all_animes.extend(anime_data)

            if show_favorites_only:
                context['titulo'] = "Mis Animes Favoritos"
            else:
                context['titulo'] = "Animes Populares y Mi Colección"

        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con la API: {e}")
            context['error_mensaje'] = "No se pudieron cargar los animes de la API. Mostrando solo tu colección local."
            if show_favorites_only:
                context['titulo'] = "Mis Favoritos (Solo Locales)"
            else:
                context['titulo'] = "Mi Colección de Animes"

        context['animes'] = all_animes

        return context

class AnimeDetailView(TemplateView):
    template_name = 'myapp/anime_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        anime_id = kwargs.get('pk')

        try:
            local_anime = Anime.objects.get(id=anime_id)

            context['anime'] = {
                'mal_id': local_anime.id,
                'title': local_anime.title,
                'score': float(local_anime.score),
                'episodes': local_anime.episodes,
                'type': local_anime.type,
                'images': {
                    'jpg': {
                        'image_url': local_anime.image_url
                    }
                },
                'synopsis': 'Anime de tu colección personal.',
                'is_local': True
            }
            context['titulo'] = local_anime.title
            context['is_local'] = True

        except Anime.DoesNotExist:
            try:
                api_url = f"https://api.jikan.moe/v4/anime/{anime_id}"
                response = requests.get(api_url)
                response.raise_for_status()
                data = response.json()
                anime_data = data.get('data', {})

                context['anime'] = anime_data
                context['titulo'] = anime_data.get('title', 'Detalle del Anime')
                context['is_local'] = False

            except requests.exceptions.RequestException as e:
                print(f"Error al obtener el anime de la API: {e}")
                context['error_mensaje'] = "No se pudo cargar la información del anime."
                context['anime'] = None
                context['is_local'] = False

        return context


class AnimeCreateView(CreateView):
    model = Anime
    fields = ['title', 'score', 'episodes', 'type', 'image_url']
    success_url = reverse_lazy('anime_list')

    def form_valid(self, form):
        anime = form.save()
        print(f"Anime creado: {anime.title}")
        print(f"URL de imagen guardada: {anime.image_url}")
        messages.success(self.request, f'¡Anime "{anime.title}" creado exitosamente!')
        return redirect('anime_list')


class AnimeUpdateView(UpdateView):
    model = Anime
    fields = ['title', 'score', 'episodes', 'type', 'image_url']
    template_name = 'myapp/anime_form.html'

    def get_success_url(self):
        return reverse_lazy('anime_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):

        response = super().form_valid(form)
        messages.success(self.request, f'¡Anime "{form.instance.title}" actualizado exitosamente!')
        return response


class AnimeDeleteView(DeleteView):

    model = Anime
    template_name = 'myapp/anime_confirm_delete.html'
    success_url = reverse_lazy('anime_list')

    def delete(self, request, *args, **kwargs):

        anime = self.get_object()
        messages.success(request, f'¡Anime "{anime.title}" eliminado exitosamente!')
        return super().delete(request, *args, **kwargs)


@require_POST
def toggle_favorite(request):

    import json

    try:
        data = json.loads(request.body)
        anime_id = data.get('anime_id')
        is_local = data.get('is_local', False)

        if is_local:
            anime = get_object_or_404(Anime, id=anime_id)
            anime.is_favorite = not anime.is_favorite
            anime.save()
            is_favorite = anime.is_favorite
        else:
            favorite, created = FavoriteAnime.objects.get_or_create(
                mal_id=anime_id,
                defaults={
                    'title': data.get('title', ''),
                    'image_url': data.get('image_url', ''),
                    'score': data.get('score', 0.00),
                    'episodes': data.get('episodes', 0),
                    'type': data.get('type', 'TV'),
                }
            )

            if not created:
                favorite.delete()
                is_favorite = False
            else:
                is_favorite = True

        return JsonResponse({
            'success': True,
            'is_favorite': is_favorite
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)