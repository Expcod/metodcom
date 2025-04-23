from django.shortcuts import render, get_object_or_404
from .models import Grade, Subject, Section, Lesson, Methodology, Textbook, TextbookPage

def home(request):
    return render(request, 'school/index.html', {})

def grade_list(request):
    grades = Grade.objects.all()
    return render(request, 'school/grade_list.html', {'grades': grades})

def subject_list(request, grade_id):
    grade = get_object_or_404(Grade, id=grade_id)
    subjects = Subject.objects.filter(grade=grade)
    
    context = {
        'grade': grade,
        'subjects': subjects,
    }
    
    return render(request, 'school/subject_list.html', context)

def lesson_list(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    lessons = Lesson.objects.filter(section=section).order_by('order')
    
    context = {
        'section': section,
        'lessons': lessons,
        'subject': section.subject,
        'grade': section.subject.grade,
    }
    
    return render(request, 'school/lesson_list.html', context)

def section_list(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    sections = Section.objects.filter(subject=subject)
    return render(request, 'school/section_list.html', {'subject': subject, 'sections': sections})

def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    methodologies = Methodology.objects.filter(lesson=lesson)
    
    # Darslik sahifasini topish
    textbook_page = None
    textbook = None
    
    # Agar darsga bog'langan darslik sahifasi bo'lsa
    if hasattr(lesson, 'textbook_pages') and lesson.textbook_pages.exists():
        textbook_page = lesson.textbook_pages.first()
        textbook = textbook_page.textbook
    
    context = {
        'lesson': lesson,
        'methodologies': methodologies,
        'textbook_page': textbook_page,
        'textbook': textbook,
    }
    
    return render(request, 'school/lesson_detail.html', context)

def textbook_list(request):
    textbooks = Textbook.objects.all()
    return render(request, 'school/textbook_list.html', {'textbooks': textbooks})

def textbook_detail(request, textbook_id, lesson_id):
    textbook = get_object_or_404(Textbook, id=textbook_id)
    lesson = get_object_or_404(Lesson, id=lesson_id)
    page = TextbookPage.objects.filter(textbook=textbook, lesson=lesson).first()
    methodologies = Methodology.objects.filter(lesson=lesson)
    return render(request, 'school/textbook_detail.html', {
        'textbook': textbook,
        'lesson': lesson,
        'page': page,
        'methodologies': methodologies
    })