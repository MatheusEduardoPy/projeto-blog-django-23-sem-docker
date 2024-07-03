from django.db import models

from utils.rands import slugify_new

class Tag(models.Model):
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    name = models.CharField(max_length=45)
    slug = models.SlugField(
        unique=True, default=None, null=True, blank=True, max_length=45
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.name, 5)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name    
class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=45)
    slug = models.SlugField(
        unique=True, default=None, null=True, blank=True, max_length=45
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.name, 5)
        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.name   
    
class Page(models.Model):
    title = models.CharField(max_length=65,)
    slug = models.SlugField(
        unique=True, default="", 
        null=False, blank=True, max_length=45
    )
    is_published = models.BooleanField(
        default=False,
        help_text=("Esse campo precisa estar marcado "
                   "para a página ser exibida publicamente")
        )
    content = models.TextField()
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.title, 5)
        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.title   
    
class Post(models.Model):
    class Meta:
        verbose_name='Post'
        verbose_name_plural='Posts'

    title = models.CharField(max_length=65,)
    slug = models.SlugField(
        unique=True, default="",
        null=False, blank=True, max_length=255
    )
    excerpt = models.CharField(max_length=100)
    is_published = models.BooleanField(
        default=False,
        help_text=("Esse campo precisa estar marcado "
                   "para o post ser exibido publicamente")
        )
    content = models.TextField()
    cover = models.ImageField(upload_to='posts/%Y/%m/', blank=True, default='')
    cover_in_post_content = models.BooleanField(
        default=True,
        help_text="Se marcado, exibirá a capa dentro do post.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        default=None
    )
    tags = models.ManyToManyField(Tag, blank=True, default='')