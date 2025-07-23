from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Grade, Subject, Section, Lesson, Methodology, Textbook, TextbookPage, CustomUser, Task
from .forms import LoginForm, RegistrationForm

def home(request):
    return render(request, 'school/index.html', {})

@login_required
def grade_list(request):
    # Agar foydalanuvchi ota-ona bo'lsa, metodikalarga kirishni taqiqlash
    if request.user.role == 'parent':
        messages.error(request, "Kechirasiz, bu bo'lim faqat o'qituvchilar uchun!")
        return redirect('maktab:home')
    
    grades = Grade.objects.all()
    return render(request, 'school/grade_list.html', {'grades': grades})

@login_required
def subject_list(request, grade_id):
    """Metodikalar - Tanlangan sinfdagi fanlar ro'yxati"""
    # Agar foydalanuvchi ota-ona bo'lsa, metodikalarga kirishni taqiqlash
    if request.user.role == 'parent':
        messages.error(request, "Kechirasiz, bu bo'lim faqat o'qituvchilar uchun!")
        return redirect('maktab:home')
    
    grade = get_object_or_404(Grade, id=grade_id)
    subjects = Subject.objects.filter(grade=grade)
    
    context = {
        'grade': grade,
        'subjects': subjects,
    }
    
    return render(request, 'school/subject_list.html', context)

@login_required  
def section_list(request, subject_id):
    """Metodikalar - Tanlangan fandagi qismlar ro'yxati"""
    # Agar foydalanuvchi ota-ona bo'lsa, metodikalarga kirishni taqiqlash
    if request.user.role == 'parent':
        messages.error(request, "Kechirasiz, bu bo'lim faqat o'qituvchilar uchun!")
        return redirect('maktab:home')
    
    subject = get_object_or_404(Subject, id=subject_id)
    sections = Section.objects.filter(subject=subject)
    
    context = {
        'subject': subject,
        'grade': subject.grade,
        'sections': sections,
    }
    
    return render(request, 'school/section_list.html', context)

@login_required
def lesson_list(request, section_id):
    """Metodikalar - Tanlangan qismdagi darslar ro'yxati"""
    # Agar foydalanuvchi ota-ona bo'lsa, metodikalarga kirishni taqiqlash
    if request.user.role == 'parent':
        messages.error(request, "Kechirasiz, bu bo'lim faqat o'qituvchilar uchun!")
        return redirect('maktab:home')
    
    section = get_object_or_404(Section, id=section_id)
    lessons = Lesson.objects.filter(section=section).order_by('order')
    
    context = {
        'section': section,
        'lessons': lessons,
        'subject': section.subject,
        'grade': section.subject.grade,
    }
    
    return render(request, 'school/lesson_list.html', context)

@login_required
def lesson_detail(request, lesson_id):
    # Agar foydalanuvchi ota-ona bo'lsa, metodikalarga kirishni taqiqlash
    if request.user.role == 'parent':
        messages.error(request, "Kechirasiz, bu bo'lim faqat o'qituvchilar uchun!")
        return redirect('maktab:home')
    
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

@login_required
def textbook_list(request):
    textbooks = Textbook.objects.all()
    return render(request, 'school/textbook_list.html', {'textbooks': textbooks})

@login_required
def textbook_detail(request, textbook_id, section_id):
    textbook = get_object_or_404(Textbook, id=textbook_id)
    
    if section_id == 0:
        # Agar section_id 0 bo'lsa, birinchi sectionni olish
        section = textbook.subject.sections.first()
    else:
        section = get_object_or_404(Section, id=section_id)
    
    # Section ga tegishli darslarni olish
    lessons = section.lessons.all() if section else []
    
    return render(request, 'school/textbook_detail.html', {
        'textbook': textbook,
        'section': section,
        'lessons': lessons,
    })

# Authentication Views
def user_login(request):
    if request.user.is_authenticated:
        return redirect('maktab:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # So'nggi kirgan vaqtni yangilash
                user.last_login_time = timezone.now()
                user.save()
                messages.success(request, f"Xush kelibsiz, {user.first_name}!")
                return redirect('maktab:home')
            else:
                messages.error(request, "Telefon raqam yoki parol noto'g'ri.")
        else:
            messages.error(request, "Barcha maydonlarni to'ldiring.")
    
    return render(request, 'school/login.html')

def user_register(request):
    if request.user.is_authenticated:
        return redirect('maktab:home')
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        role = request.POST.get('role')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Validatsiya
        if not all([first_name, last_name, phone_number, role, password1, password2]):
            messages.error(request, "Barcha maydonlarni to'ldiring.")
        elif password1 != password2:
            messages.error(request, "Parollar bir xil emas.")
        elif role not in ['teacher', 'parent']:
            messages.error(request, "Iltimos, to'g'ri rol tanlang.")
        elif CustomUser.objects.filter(phone_number=phone_number).exists():
            messages.error(request, "Bu telefon raqam allaqachon ro'yxatdan o'tgan.")
        else:
            try:
                # Foydalanuvchi yaratish
                user = CustomUser.objects.create_user(
                    phone_number=phone_number,
                    first_name=first_name,
                    last_name=last_name,
                    role=role,
                    password=password1
                )
                
                # Avtomatik login qilish
                user = authenticate(request, username=phone_number, password=password1)
                if user:
                    login(request, user)
                    user.last_login_time = timezone.now()
                    user.save()
                    
                    # Role asosida xabar
                    if role == 'teacher':
                        messages.success(request, f"Xush kelibsiz, {user.first_name}! Siz o'qituvchi sifatida barcha bo'limlarga kirish huquqiga egasiz.")
                    else:
                        messages.success(request, f"Xush kelibsiz, {user.first_name}! Siz ota-ona sifatida darsliklar va vazifalar bo'limlaridan foydalanishingiz mumkin.")
                    
                    return redirect('maktab:home')
                else:
                    messages.success(request, "Muvaffaqiyatli ro'yxatdan o'tdingiz! Endi kirishingiz mumkin.")
                    return redirect('maktab:login')
            except Exception as e:
                messages.error(request, f"Xatolik yuz berdi: {str(e)}")
    
    return render(request, 'school/register.html')

def user_logout(request):
    logout(request)
    messages.success(request, "Muvaffaqiyatli chiqtingiz.")
    return redirect('maktab:home')

@login_required
def user_profile(request):
    if request.method == 'POST':
        birth_date = request.POST.get('birth_date')
        birth_place = request.POST.get('birth_place')
        
        # Ma'lumotlarni yangilash (role bundan mustasno)
        user = request.user
        user.birth_date = birth_date if birth_date else None
        user.birth_place = birth_place
        user.save()
        
        messages.success(request, "Profil ma'lumotlari muvaffaqiyatli yangilandi!")
        return redirect('maktab:profile')
    
    return render(request, 'school/profile.html')

@login_required
def task_list(request):
    """Vazifalar - Sinflar ro'yxati sahifasi (grade_list kabi)"""
    grades = Grade.objects.all()
    return render(request, 'school/task_grade_list.html', {'grades': grades})

@login_required
def task_subject_list(request, grade_id):
    """Vazifalar - Tanlangan sinfdagi fanlar ro'yxati"""
    grade = get_object_or_404(Grade, id=grade_id)
    subjects = Subject.objects.filter(grade=grade)
    
    context = {
        'grade': grade,
        'subjects': subjects,
    }
    
    return render(request, 'school/task_subject_list.html', context)

@login_required
def task_by_subject(request, section_id):
    """Vazifalar - Tanlangan qismdagi vazifalar ro'yxati"""
    section = get_object_or_404(Section, id=section_id)
    lessons = Lesson.objects.filter(section=section).order_by('order')
    
    # Barcha darslardan vazifalarni olish
    tasks = []
    for lesson in lessons:
        lesson_tasks = Task.objects.filter(lesson=lesson, is_active=True).order_by('title')
        for task in lesson_tasks:
            tasks.append(task)
    
    context = {
        'section': section,
        'lessons': lessons,
        'subject': section.subject,
        'grade': section.subject.grade,
        'tasks': tasks,
    }
    
    return render(request, 'school/task_final_list.html', context)

@login_required
def task_detail(request, task_id):
    """Vazifa batafsil sahifasi"""
    task = get_object_or_404(Task, id=task_id, is_active=True)
    
    context = {
        'task': task,
        'lesson': task.lesson,
        'section': task.lesson.section,
        'subject': task.lesson.section.subject,
        'grade': task.lesson.section.subject.grade,
    }
    
    return render(request, 'school/task_detail.html', context)