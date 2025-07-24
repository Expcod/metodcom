from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import JsonResponse
from django.urls import path
from .models import CustomUser, Grade, Subject, Section, Lesson, Methodology, Textbook, TextbookPage, Task

# Custom admin URLs uchun view
def get_sections_for_subject(request, subject_id):
    """AJAX endpoint to get sections for a subject"""
    sections = Section.objects.filter(subject_id=subject_id).values('id', 'name')
    return JsonResponse({'sections': list(sections)})

# Custom Admin Site
class CustomAdminSite(admin.AdminSite):
    site_header = "Maktab Boshqaruv Tizimi"
    site_title = "Maktab Admin"
    index_title = "Boshqaruv Paneli"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('get-sections/<int:subject_id>/', get_sections_for_subject, name='get_sections'),
        ]
        return custom_urls + urls

# Custom admin site instance
admin_site = CustomAdminSite(name='custom_admin')

class MethodologyInline(admin.StackedInline):
    model = Methodology
    extra = 1

class TextbookPageInline(admin.StackedInline):
    model = TextbookPage
    extra = 1

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

class GradeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'grade']
    list_filter = ['grade']
    search_fields = ['name']

class SectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject']
    list_filter = ['subject']
    search_fields = ['name']

class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'section', 'order']
    list_filter = ['section__subject']
    search_fields = ['title']
    inlines = [MethodologyInline, TextbookPageInline]

class MethodologyAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson', 'created_at','link']
    list_filter = ['lesson__section__subject']
    search_fields = ['title']

class TextbookAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'section']
    list_filter = ['subject', 'section']
    search_fields = ['title']
    
    class Media:
        js = ('admin/js/textbook_admin.js',)

class TextbookPageAdmin(admin.ModelAdmin):
    list_display = ['textbook', 'lesson', 'page_number']
    list_filter = ['textbook']
    search_fields = ['textbook__title', 'lesson__title']

class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson', 'difficulty', 'time_estimate', 'is_active', 'created_at']
    list_filter = ['difficulty', 'is_active', 'lesson__section__subject__grade']
    search_fields = ['title', 'lesson__title']
    readonly_fields = ['created_at']

# Modellarni ro'yxatdan o'tkazish
admin_site.register(CustomUser, CustomUserAdmin)
admin_site.register(Grade, GradeAdmin)
admin_site.register(Subject, SubjectAdmin)
admin_site.register(Section, SectionAdmin)
admin_site.register(Lesson, LessonAdmin)
admin_site.register(Methodology, MethodologyAdmin)
admin_site.register(Textbook, TextbookAdmin)
admin_site.register(TextbookPage, TextbookPageAdmin)
admin_site.register(Task, TaskAdmin)