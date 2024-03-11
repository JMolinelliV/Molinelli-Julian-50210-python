from django.db import models
#from ckeditor.fields import RichTextField

# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=250, verbose_name = "título")
    content = models.TextField(verbose_name = "contenido")
    post_author = models.CharField(max_length=30, verbose_name = "autor")
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='blog/files/blog_images', verbose_name = "imagen")
    categories = models.ManyToManyField('Category', related_name='posts', verbose_name = "categorias") #Relaciona el atributo con la clase Category y permite usar category.posts

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "blog post"
        verbose_name_plural = "blog posts"

class Category(models.Model):
    cat_name = models.CharField(max_length=50)

    def __str__(self):
        return self.cat_name
    
    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

class Comment(models.Model):
    comment_author = models.CharField(max_length=30)
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(default="email@prueba.com")
    post = models.ForeignKey("BlogPost", on_delete=models.CASCADE) #Cada comment solo puede estar relacionado a un BlogPost

    def __str__(self):
        return f"{self.comment_author} on '{self.post}'"
    
    class Meta:
        verbose_name = "comment"
        verbose_name_plural = "comments"

class Contact(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField()
