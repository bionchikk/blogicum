from django.db import models
from django.contrib.auth import get_user_model
from core.models import PublishedModel,CreatedAtModel
from django.urls import reverse


User = get_user_model()



class Category(PublishedModel,CreatedAtModel):
    title = models.CharField(max_length=256,verbose_name="Заголовок")
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(max_length=64, unique=True ,verbose_name='Слаг', help_text="Идентификатор страницы для URL; разрешены символы латиницы, цифры, дефис и подчёркивание.")

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
    
    def __str__(self):
        return self.title
    


class Location(PublishedModel,CreatedAtModel):
    name = models.CharField(max_length=256,verbose_name="Название места")

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Post (PublishedModel,CreatedAtModel):
    title   = models.CharField(max_length=256,verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст")
    pub_date = models.DateTimeField(verbose_name="Дата и время публицации", help_text="Если установить дату и время в будущем — можно делать отложенные публикации.")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name= 'Автор публикации'           
    )
    location = models.ForeignKey(Location,on_delete=models.SET_NULL, null=True,verbose_name= 'Местоположение')
    category = models.ForeignKey(Category,on_delete=models.SET_NULL, null=True,verbose_name= 'Категория')
    image = models.ImageField('Фото',upload_to='posts_images',blank=True)

    

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации' 

    def __str__(self):
        return self.title

    def get_absolute_urls(self):
        return reverse('blog:post_detail',kwargs = {'pk': self.pk})

    
