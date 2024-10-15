from django.contrib import admin

# Register your models here.
from .models import Post,Category,Location



admin.site.empty_value_display = 'Не задано'

class PostInline(admin.StackedInline):
    model = Post
    extra = 0

class CategoryAdmin(admin.ModelAdmin):
    inlines = (PostInline,)

class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'pub_date',
        'is_published',
        'author',
        'location',
        'category'
    )
    list_editable =(
        'is_published',
        'category'
    )
    search_fields =('title',)
    list_filter = ('is_published',)
    list_display_links = ('title',)



admin.site.register(Post,PostAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Location)
