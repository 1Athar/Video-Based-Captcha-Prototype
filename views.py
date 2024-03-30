from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Video, CaptchaQuestion

def play_video(request):
    # Retrieve a random video from the database
    video = Video.objects.order_by('?').first()
    questions = CaptchaQuestion.objects.filter(video=video)
    context = {
        'video': video,
        'questions': questions
    }
    return render(request, 'videocaptcha/play_video.html', context)

def verify_captcha(request):
    if request.method == 'POST':
        video_id = request.POST.get('video_id')
        answers = request.POST.getlist('answers[]')
        # Fetch questions and answers from the database
        questions = CaptchaQuestion.objects.filter(video_id=video_id)
        correct_answers = [question.answer for question in questions]
        # Verify answers
        if answers == correct_answers:
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})
    return JsonResponse({'error': 'Invalid request method'})
def captcha_view(request):
    return render(request, 'videocaptcha/captcha.html')
def login_view(request):
    return(request, 'videocaptcha/login.html')
def register_view(request):
    return render(request, 'videocaptcha/register.html')
