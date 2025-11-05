# Proyecto de Gestión de Anime

Este proyecto es una aplicación web desarrollada con Django que permite gestionar una lista personal de anime, incluyendo funcionalidades para agregar, editar, eliminar y marcar como favoritos diferentes títulos.

## Estructura del Proyecto

# Archivos Principales
- `manage.py`: Script principal para gestionar el proyecto Django
- `ProyectoFinalWeb/settings.py`: Configuraciones generales del proyecto
- `ProyectoFinalWeb/urls.py`: Enrutamiento principal de la aplicación
- `ProyectoFinalWeb/wsgi.py`: Configuración para despliegue WSGI

# Aplicación Principal (myapp)
- `myapp/models.py`: Define el modelo Anime con sus atributos
- `myapp/views.py`: Contiene las vistas basadas en clase para CRUD
- `myapp/urls.py`: Enrutamiento específico de la aplicación
- `myapp/forms.py`: Formularios para la creación y edición de anime

# Templates
- `myapp/templates/myapp/base.html`: Plantilla base con Bootstrap 5
- `myapp/templates/myapp/anime_list.html`: Lista de animes
- `myapp/templates/myapp/anime_form.html`: Formulario para crear/editar
- `myapp/templates/myapp/anime_detail.html`: Detalles de un anime
- `myapp/templates/myapp/anime_confirm_delete.html`: Confirmación de eliminación

# Instalación y Ejecución Local

1. Crear y activar entorno virtual:
```bash
py -m venv .venv
.\.venv\Scripts\activate
```

2. Instalar django:
```bash
pip install django
pip install requests
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Ejecutar servidor de desarrollo:
```bash
python manage.py runserver
```

5. Abrir en navegador:
```
http://127.0.0.1:8000/
```

# Funcionalidades
- Listado de animes con paginación
- Creación, edición y eliminación de animes
- Marcar/desmarcar animes como favoritos
- Interfaz responsiva con Bootstrap 5
- Sistema de búsqueda y filtrado

# Tecnologías Utilizadas
- Django 5.2
- Bootstrap 5
- SQLite
- HTML/CSS
- JavaScript

# Autor
Ignacio Rojo
