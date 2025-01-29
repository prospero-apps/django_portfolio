from django.contrib import admin
from .models import Category, Technology, Project, Link

class LinkInline(admin.StackedInline):
    model = Link

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_added', 'category', 'display_technologies')
    list_filter = ('category', 'date_added', 'technologies')
    #fields = ['name', 'description', ('date_added', 'image'), 'category', 'technologies']
    inlines = [LinkInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'description')
        }),
        ('Project Details', {
            'fields': (('date_added', 'image'), 'category', 'technologies')
        }),
    )

class LinkAdmin(admin.ModelAdmin):
    list_display = ('display_link',)
    list_filter = ('name',)

admin.site.register(Category)
admin.site.register(Technology)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Link, LinkAdmin)
