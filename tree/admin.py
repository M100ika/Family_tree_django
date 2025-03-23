from django.contrib import admin
from .models import Person

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name', 'date_of_birth')
    list_filter = ('last_name', 'first_name')
    search_fields = ('last_name', 'first_name', 'middle_name')
    readonly_fields = ('created_at',)
    
    def get_children_count(self, obj):
        return obj.children.count()
    get_children_count.short_description = 'Количество детей'
    
    list_display = ('last_name', 'first_name', 'middle_name', 'date_of_birth', 'get_children_count') 