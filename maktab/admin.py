from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Grade, Subject, Section, Lesson, Methodology, Textbook, TextbookPage, Task

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['phone_number', 'first_name', 'last_name', 'role', 'created_at', 'last_login_time']
    list_filter = ['role', 'created_at', 'is_active']
    search_fields = ['phone_number', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Shaxsiy ma\'lumotlar', {'fields': ('first_name', 'last_name', 'birth_date', 'birth_place', 'role')}),
        ('Ruxsatlar', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Muhim sanalar', {'fields': ('last_login', 'date_joined', 'created_at', 'last_login_time')}),
    )
    readonly_fields = ['created_at', 'last_login_time']
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'first_name', 'last_name', 'role', 'password1', 'password2'),
        }),
    )

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
    list_display = ['title', 'lesson', 'created_at','link']
    list_filter = ['lesson__section__subject']
    search_fields = ['title']

@admin.register(Textbook)
class TextbookAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject']
    list_filter = ['subject']
    search_fields = ['title']

@admin.register(TextbookPage)
class TextbookPageAdmin(admin.ModelAdmin):
    list_display = ['textbook', 'lesson', 'page_number']
    list_filter = ['textbook']
    search_fields = ['textbook__title', 'lesson__title']

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson', 'difficulty', 'time_estimate', 'is_active', 'created_at']
    list_filter = ['difficulty', 'is_active', 'lesson__section__subject__grade']
    search_fields = ['title', 'lesson__title']
    readonly_fields = ['created_at']