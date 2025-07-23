from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone_number', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['full_name', 'phone_number', 'message']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['status']
    
    fieldsets = (
        ('Murojaat ma\'lumotlari', {
            'fields': ('full_name', 'phone_number', 'message')
        }),
        ('Holat va vaqt', {
            'fields': ('status', 'created_at', 'updated_at')
        }),
    )
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
