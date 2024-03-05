# Pezorium

Sitio web generado con Django como proyecto para el curso de Python ofrecido por CoderHouse. 
El sitio web es un blog con tienda integrada que permite a los usuarios compartir información sobre distintas temáticas relacionadas a la acuariofilia. Se utiliza como modelo el template de [ZenBlog](https://bootstrapmade.com/zenblog-bootstrap-blog-template/#download).

## Orden

1. Primero hacer las migraciones si es necesario `py manage.py makemigrations` y `py manage.py migrate`
2. Luego para correr el servidor `py manage.py runserver`

## Paquetes necesarios
- crispy-bootstrap5   2024.2
- Django              5.0.2
- django-crispy-forms 2.1
- pillow              10.2.0

## URLs funcionales
Todas las funcionalidades fueron implementadas dentro de la App "Blog" por lo que dentro del nav, los links de "Tienda" de momento no son funcionales.
El funcionamiento de la página es intiuitivo por lo que:
- Hacer click en el título de un post lleva a "http://127.0.0.1:8000/BlogPost/<int:pk>/" donde pk es la primary key del BlogPost object.
- En el navbar, hacer click en "Blog" lleva al index que muestra todos los posteos realizados ordenados por fecha de más nuevo a más viejos.
    - La lista desplegable contiene un único link que lleva a la vista para crear nuevos posts (http://127.0.0.1:8000/new_post/). Esta vista utiliza Crispy Forms para organizar la apariencia y layout del form "newPostForm", que a su vez permite la carga de imágenes y demás datos requeridos por el modelo BlogPost. 
- "Nostros" lleva a http://127.0.0.1:8000/about/ pero muestra un mensaje de error personalizado, al igual que "Contacto" (http://127.0.0.1:8000/contact/) ya que aún no han sido implementadas sus funcionalidades.
- Cada BlogPost tiene asociadas categorias a través del model Category que se muestran sobre o a un lado de la fecha de creación dependiendo de si el usuario se encuentra dentro de un BlogPost o en el Index. Hacer click en una categoría muestra una nueva vista (http://127.0.0.1:8000/category/<category>/) que filtra solo los BlogPost que contengan dicha Category asociada.
- El navbar contiene además una barra de búsqueda que permite buscar BlogPosts que contengan un cierto término tanto en el título como en el cuerpo. En caso de no haber coincidencias se muestra un mensaje personalizado.