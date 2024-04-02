from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate,login
from .models.users import RegisteredUser
from django.http import JsonResponse
from .models.models import Video, CaptchaQuestion

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
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('captcha_view/')  # Redirect to a protected page after successful login
        else:
            # Authentication failed
            return render(request, 'videocaptcha/login.html', {'error': 'Invalid email or password'})
    else:
        return render(request, 'videocaptcha/login.html')
    
def register_view(request):
     if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        # Hash the password before saving
        hashed_password = make_password(password)
        user = RegisteredUser(email=email, password=hashed_password)
        user.save()
        return redirect('login')
     else: 
        return render(request, 'videocaptcha/register.html')