from django.db import models
from django.utils import timezone

class Feedback(models.Model):
    STATUS_CHOICES = [
        ('new', 'Yangi'),
        ('in_progress', 'Ko\'rib chiqilmoqda'),
        ('resolved', 'Hal qilindi'),
    ]
    
    full_name = models.CharField(max_length=100, verbose_name="Ism familiya")
    phone_number = models.CharField(max_length=20, verbose_name="Telefon raqam")
    message = models.TextField(verbose_name="Murojaat matni")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='new',
        verbose_name="Holati"
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Yaratilgan vaqt")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="O'zgartirilgan vaqt")
    
    class Meta:
        verbose_name = "Murojaat"
        verbose_name_plural = "Murojaatlar"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.full_name} - {self.created_at.strftime('%d.%m.%Y')}"
