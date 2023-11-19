from django.contrib import admin
from schedule_keeper.models import Plant, Post


class PlantAdmin(admin.ModelAdmin):
    model = Plant
    list_display = ('name', 'category', 'watering_frequency')
    list_filter = ('watering_frequency', 'category')
    search_fields = ('name__icontains', 'category__name__icontains')


class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ('created_at', 'user')
    list_filter = ('created_at', 'plant__name')
    search_fields = ('user', 'content', 'plant__name')


admin.site.register(Plant, PlantAdmin)
admin.site.register(Post, PostAdmin)
