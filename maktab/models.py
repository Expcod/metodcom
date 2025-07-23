from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, first_name, last_name, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('Telefon raqam kiritilishi shart')
        if not first_name:
            raise ValueError('Ism kiritilishi shart')
        if not last_name:
            raise ValueError('Familiya kiritilishi shart')
        
        user = self.model(
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone_number, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'teacher')  # Default role for superuser
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser is_staff=True bo\'lishi kerak.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser is_superuser=True bo\'lishi kerak.')
        
        return self.create_user(phone_number, first_name, last_name, password, **extra_fields)

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('teacher', 'O\'qituvchi'),
        ('parent', 'Ota-ona'),
    ]
    
    # Asosiy ma'lumotlar (register paytida)
    phone_number = models.CharField(max_length=20, unique=True, verbose_name="Telefon raqam")
    
    # Qo'shimcha ma'lumotlar (profile paytida to'ldiriladi)
    birth_date = models.DateField(null=True, blank=True, verbose_name="Tug'ilgan sana")
    birth_place = models.CharField(max_length=100, null=True, blank=True, verbose_name="Tug'ilgan joy")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=True, blank=True, verbose_name="Rol")
    
    # Vaqt ma'lumotlari
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ro'yxatdan o'tgan vaqt")
    last_login_time = models.DateTimeField(null=True, blank=True, verbose_name="So'nggi kirgan vaqt")
    
    # Django default username field o'rniga telefon raqam ishlatamiz
    username = None
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.phone_number})"

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"

class Grade(models.Model):
    name = models.CharField(max_length=50, verbose_name="Sinf nomi")  # Masalan, 1-sinf
    description = models.TextField(blank=True, verbose_name="Tavsif")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Sinf"
        verbose_name_plural = "Sinflar"

class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name="Fan nomi")  # Masalan, Ona tili
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name="subjects", verbose_name="Sinf")
    description = models.TextField(blank=True, verbose_name="Tavsif")

    def __str__(self):
        return f"{self.name} ({self.grade.name})"

    class Meta:
        verbose_name = "Fan"
        verbose_name_plural = "Fanlar"

class Section(models.Model):
    name = models.CharField(max_length=50, verbose_name="Qism nomi")  # Masalan, 1-qism
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="sections", verbose_name="Fan")
    description = models.TextField(blank=True, verbose_name="Tavsif")

    def __str__(self):
        return f"{self.name} ({self.subject.name})"

    class Meta:
        verbose_name = "Qism"
        verbose_name_plural = "Qismlar"

class Lesson(models.Model):
    title = models.CharField(max_length=200, verbose_name="Dars nomi")  # Masalan, Kirish
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="lessons", verbose_name="Qism")
    order = models.PositiveIntegerField(default=1, verbose_name="Tartib raqami")
    description = models.TextField(blank=True, verbose_name="Tavsif")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Dars"
        verbose_name_plural = "Darslar"
        ordering = ['order']

class Methodology(models.Model):
    title = models.CharField(max_length=200, verbose_name="Metodika nomi")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="methodologies", verbose_name="Dars")
    content = models.TextField(verbose_name="Metodika mazmuni")
    image = models.ImageField(upload_to='methodologies/images/', blank=True, null=True, verbose_name="Rasm")
    file = models.FileField(upload_to='methodologies/files/', blank=True, null=True, verbose_name="Fayl")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    link = models.CharField(max_length=200, blank=True, null=True, verbose_name="Havola")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Metodika"
        verbose_name_plural = "Metodikalar"

class Textbook(models.Model):
    title = models.CharField(max_length=200, verbose_name="Darslik nomi")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="textbooks", verbose_name="Fan")
    pdf_file = models.FileField(upload_to='textbooks/', verbose_name="PDF fayl")
    cover_image = models.ImageField(upload_to='textbooks/covers/', blank=True, null=True, verbose_name="Muqova rasmi")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Darslik"
        verbose_name_plural = "Darsliklar"

class TextbookPage(models.Model):
    textbook = models.ForeignKey(Textbook, on_delete=models.CASCADE, related_name="pages", verbose_name="Darslik")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="textbook_pages", verbose_name="Dars")
    page_number = models.PositiveIntegerField(verbose_name="Sahifa raqami")
    description = models.TextField(blank=True, verbose_name="Sahifa mazmuni")

    def __str__(self):
        return f"{self.textbook.title} - {self.page_number}-sahifa"

    class Meta:
        verbose_name = "Darslik sahifasi"
        verbose_name_plural = "Darslik sahifalari"

class Task(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Oson'),
        ('medium', 'Orta'),
        ('hard', 'Qiyin'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Vazifa nomi")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="tasks", verbose_name="Dars")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium', verbose_name="Qiyinlik darajasi")
    description = models.TextField(verbose_name="Vazifa tavsifi")
    instructions = models.TextField(verbose_name="Bajarish yo'riqnomasi")
    time_estimate = models.PositiveIntegerField(default=30, verbose_name="Bajarish vaqti (daqiqa)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    def __str__(self):
        return f"{self.title} ({self.lesson.title})"

    class Meta:
        verbose_name = "Vazifa"
        verbose_name_plural = "Vazifalar"
        ordering = ['lesson__order', 'title']