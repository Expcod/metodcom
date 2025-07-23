from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from .forms import FeedbackForm
from .models import Feedback

def feedback_create(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save()
            messages.success(request, 'Murojaatingiz muvaffaqiyatli yuborildi! Tez orada siz bilan bog\'lanamiz.')
            return redirect('maktab:home')
        else:
            messages.error(request, 'Iltimos, barcha maydonlarni to\'g\'ri to\'ldiring.')
    else:
        form = FeedbackForm()
    
    return render(request, 'feedback/feedback_form.html', {'form': form})

@csrf_exempt
@require_POST
def feedback_ajax(request):
    try:
        data = json.loads(request.body)
        form = FeedbackForm(data)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'success': True,
                'message': 'Murojaatingiz muvaffaqiyatli yuborildi!'
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Xatolik yuz berdi. Qaytadan urinib ko\'ring.'
        })
