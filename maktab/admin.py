from django.contrib import admin
from .models import Grade, Subject, Section, Lesson, Methodology, Textbook, TextbookPage

class MethodologyInline(admin.StackedInline):
    model = Methodology
    extra = 1

class TextbookPageInline(admin.StackedInline):
    model = TextbookPage
    extra = 1

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'grade']
    list_filter = ['grade']
    search_fields = ['name']

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject']
    list_filter = ['subject']
    search_fields = ['name']

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'section', 'order']
    list_filter = ['section__subject']
    search_fields = ['title']
    inlines = [MethodologyInline, TextbookPageInline]

@admin.register(Methodology)
class MethodologyAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson', 'created_at']
    list_filter = ['lesson__section__subject']
    search_fields = ['title']

@admin.register(Textbook)
class TextbookAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject']
    list_filter = ['subject']
    search_fields = ['title']

@admin.register(TextbookPage)
class TextbookAdmin(admin.ModelAdmin):
    list_display = ['textbook', 'lesson', 'page_number']
    list_filter = ['textbook__subject']
    search_fields = ['textbook__title']