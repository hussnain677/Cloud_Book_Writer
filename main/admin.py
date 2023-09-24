from django.contrib import admin
from .models import Book, Section, Collaboration

# Apply some little designed and search filter on Admin Panel

class SectionInline(admin.TabularInline):
    model = Section
    extra = 1

class CollaborationInline(admin.TabularInline):
    model = Collaboration
    extra = 1

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    list_filter = ('author',)
    search_fields = ('title',)
    inlines = [SectionInline, CollaborationInline]

class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'book', 'parent_section')
    list_filter = ('book',)
    search_fields = ('title', 'book__title')

class CollaborationAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'can_edit')
    list_filter = ('book', 'can_edit')
    search_fields = ('user__username', 'book__title')

admin.site.register(Book, BookAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Collaboration, CollaborationAdmin)
