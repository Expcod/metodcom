#!/usr/bin/env python
import os
import django
import sys

# Add the parent directory to the Python path
sys.path.append('/Users/noutbukcom/Desktop/metodcom')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'metod.settings')
django.setup()

from maktab.models import Grade, Subject, Section, Lesson

# Create sample data
def create_sample_data():
    # Create grades
    grade1, created = Grade.objects.get_or_create(
        name="1-sinf",
        defaults={'description': 'Boshlang\'ich sinf o\'quvchilari uchun'}
    )
    grade2, created = Grade.objects.get_or_create(
        name="2-sinf", 
        defaults={'description': 'Ikkinchi sinf o\'quvchilari uchun'}
    )
    grade3, created = Grade.objects.get_or_create(
        name="3-sinf", 
        defaults={'description': 'Uchinchi sinf o\'quvchilari uchun'}
    )
    
    # Create subjects for grade 1
    matematika1, created = Subject.objects.get_or_create(
        name="Matematika",
        grade=grade1,
        defaults={'description': 'Matematika fanidan darslar'}
    )
    ona_tili1, created = Subject.objects.get_or_create(
        name="Ona tili",
        grade=grade1,
        defaults={'description': 'Ona tili fanidan darslar'}
    )
    tabiiy1, created = Subject.objects.get_or_create(
        name="Tabiatshunoslik",
        grade=grade1,
        defaults={'description': 'Tabiatshunoslik fanidan darslar'}
    )
    
    # Create sections for Matematika 1-sinf
    section1, created = Section.objects.get_or_create(
        name="Sonlar",
        subject=matematika1,
        defaults={'description': 'Sonlar bilan ishlash'}
    )
    section2, created = Section.objects.get_or_create(
        name="Amallar",
        subject=matematika1,
        defaults={'description': 'Matematik amallar'}
    )
    
    # Create lessons
    lesson1, created = Lesson.objects.get_or_create(
        title="Sonlarni qo'shish",
        section=section1,
        defaults={
            'order': 1,
            'description': '1 dan 10 gacha sonlarni qo\'shish amalini o\'rgatish'
        }
    )
    
    lesson2, created = Lesson.objects.get_or_create(
        title="Sonlarni ayirish",
        section=section1,
        defaults={
            'order': 2,
            'description': '1 dan 10 gacha sonlarni ayirish amalini o\'rgatish'
        }
    )
    
    print("Sample data yaratildi!")
    print(f"Sinflar: {Grade.objects.count()}")
    print(f"Fanlar: {Subject.objects.count()}")
    print(f"Bo'limlar: {Section.objects.count()}")
    print(f"Darslar: {Lesson.objects.count()}")

if __name__ == '__main__':
    create_sample_data()
