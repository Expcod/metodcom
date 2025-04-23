from django.db import models

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
    description = models.TextField(blank=True, verbose_name="Tavsif")

    def __str__(self):
        return f"{self.textbook.title} - {self.page_number}-sahifa"

    class Meta:
        verbose_name = "Darslik sahifasi"
        verbose_name_plural = "Darslik sahifalari"