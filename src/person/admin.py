from django.contrib import admin
from .models import Expert, Skill


class ExpertsAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'nid', 'is_verify', 'is_online',
                    'timestamp', 'slug', 'last_update']
    search_fields = ['designation', 'Objective', 'name']
    # filter_vertical = ['designation']
    list_per_page = 25
    list_filter = ['designation', 'is_verify', 'timestamp']

    class Meta:
        Model = Expert


class SkillAdmin(admin.ModelAdmin):
    list_display = ['keyword', 'name', 'phone', 'email', 'level', 'is_verify',
                    'timestamp']
    search_fields = ['keyword', 'phone', 'name']
    # filter_vertical = ['designation']
    list_per_page = 25
    list_filter = ['level', 'is_verify', 'timestamp']

    class Meta:
        Model = Skill


admin.site.register(Expert, ExpertsAdmin)
admin.site.register(Skill, SkillAdmin)

# Register your models here.
