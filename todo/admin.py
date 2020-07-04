from django.contrib import admin
from .models import Todo
# if admin wants to see the created as readonly below class
class TodoAdmin(admin.ModelAdmin):
    readonly_fields=('created',)

admin.site.register(Todo,TodoAdmin)
