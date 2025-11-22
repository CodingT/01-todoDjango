from django.contrib import admin
from .models import Task, Project, Tag

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'completed', 'due_date', 'priority')
    list_filter = ('completed', 'priority', 'owner')
    search_fields = ('title', 'description')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')
    search_fields = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')
    search_fields = ('name',)
