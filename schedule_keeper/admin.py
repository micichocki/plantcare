from django.contrib import admin
from schedule_keeper.models import Plant, Post, Category


class PlantAdmin(admin.ModelAdmin):
    model = Plant
    list_display = ('name', 'category', 'watering_frequency', 'creator')
    list_filter = ('watering_frequency', 'category')
    search_fields = ('name__icontains', 'category__name__icontains')


class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ('created_at', 'creator')
    list_filter = ('created_at', 'plant__name')
    search_fields = ('creator', 'content', 'plant__name')


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)


admin.site.register(Plant, PlantAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
