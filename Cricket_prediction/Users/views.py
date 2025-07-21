from django.shortcuts import render
import requests
# Create your views here.

def Homepage(request):
     return render(request, 'Users/home.html')

from datetime import datetime
import pytz

API_KEY = "5a292b2b-72c4-492c-bd88-399d2c8e37b3"

def Dashboard(request):
    current_matches_url = f"https://api.cricapi.com/v1/currentMatches?apikey=5a292b2b-72c4-492c-bd88-399d2c8e37b3&offset=0"
    current_matches_response = requests.get(current_matches_url)
    current_matches_data = current_matches_response.json()
    # print(current_matches_data)

    all_matches_url = f"https://api.cricapi.com/v1/matches?apikey=5a292b2b-72c4-492c-bd88-399d2c8e37b3&offset=0"
    all_matches_response =requests.get(all_matches_url)
    all_matches_data = all_matches_response.json()
    # print(all_matches_data)
    
    current_matches = []
    upcoming_matches = []
    previous_matches = []

    if current_matches_data.get("status") == "success":
        # for live_match in data.get("live_matches_data", []):
        #         match_datetime = live_match.get("dateTimeGMT")
        #         live_status = match.get("status","").lower()
        #         matchEnded = live_match.get("matchEnded", "").lower()
        #         local_time = datetime.strptime(match_datetime, "%Y-%m-%dT%H:%M:%S")
        #         local_time = local_time.replace(tzinfo=pytz.UTC).astimezone(pytz.timezone("Asia/Kolkata"))
        # print(live_status)
        for match in current_matches_data.get("data", []):
            match_datetime = match.get("dateTimeGMT")
            status = match.get("status", "").lower()
            local_time = datetime.strptime(match_datetime, "%Y-%m-%dT%H:%M:%S")
            local_time = local_time.replace(tzinfo=pytz.UTC).astimezone(pytz.timezone("Asia/Kolkata"))
            matchStarted = match.get("matchStarted", "")
            matchEnded  = match.get("matchEnded" , "")
        # print(status)
            if 'Match not started' in status :
                upcoming_matches.append(match)
            
            elif matchStarted and matchEnded:
                previous_matches.append(match)


    if all_matches_data.get("status") == "success":
        for match in all_matches_data.get("data", []):
            match_datetime = match.get("dateTimeGMT")
            status = match.get("status", "").lower()
            local_time = datetime.strptime(match_datetime, "%Y-%m-%dT%H:%M:%S")
            local_time = local_time.replace(tzinfo=pytz.UTC).astimezone(pytz.timezone("Asia/Kolkata"))
            matchStarted = match.get("matchStarted", "")
            matchEnded  = match.get("matchEnded" , "")

            if 'Match not started' or 'scheduled' in status :
                upcoming_matches.append(match)

        
    all_leagues_url = f"https://apiv2.api-cricket.com/cricket/?method=get_leagues&APIkey=1496ef731183450b869852b88ae5f64cf062e50caec83fd551ade6774dc43df3"
    all_leagues_response = requests.get(all_leagues_url)
    all_leagues_data = all_leagues_response.json()

    all_leagues = []
    for leagues in all_leagues_data.get('result', []):
        league_name = leagues.get('league_name')
        league_year = leagues.get("league_year")
        
        if "2025" in league_year:
            all_leagues.append(leagues)


# Then define context
    context = {
    "current_matches": current_matches,
    "upcoming_matches": upcoming_matches,
    "previous_matches": previous_matches,
    "all_leagues": all_leagues 
}


    # event_url = f"https://api.api-cricket.com/?method=get_livescore&APIkey=1496ef731183450b869852b88ae5f64cf062e50caec83fd551ade6774dc43df3"
    # event_response = requests.get(event_url)
    # event_data = event_response.json()

    url = "https://cricket.sportdevs.com/standings"

    payload={}
    headers = {
  'Accept': 'application/json'
}

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)



    return render(request, "Users/dashboard.html", context)

def Register(request):
     return render(request, 'Users/Auth.html')


def IPL(request):
    return render(request , "Users/IPL.html")

# def Rankings(request):
#     return render(request , "Users/Rankings.html")


from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib import messages
import random
import json

# Temporarily store OTPs (for demo purpose)
# email_otp_map = {}

# def register_view(request):
#     if request.method == "POST":
#         email = request.POST.get("email")
#         password = request.POST.get("password")
#         otp = request.POST.get("otp")

#         if email_otp_map.get(email) == otp:
#             if not User.objects.filter(username=email).exists():
#                 try:
#                     user = User.objects.create_user(
#                         username=email,
#                         email=email,
#                         password=password
#                     )
#                     user.save()
#                     print("✅ User created:", user.username)
#                     return redirect('login')
#                 except Exception as e:
#                     print("❌ Error creating user:", e)
#                     return JsonResponse({"error": str(e)})
#             else:
#                 return JsonResponse({"error": "User already exists"})
#         else:
#             return JsonResponse({"error": "Invalid OTP"})

#     return render(request, "Users/register.html")


# @csrf_exempt
# def send_email_otp(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             email = data.get("email")
#             otp = str(random.randint(100000, 999999))
#             email_otp_map[email] = otp

#             send_mail(
#                 subject="Your CrickPredict OTP",
#                 message=f"Your OTP for CrickPredict is: {otp}",
#                 from_email="your_email@example.com",
#                 recipient_list=[email],
#                 fail_silently=False,
#             )

#             return JsonResponse({"success": True})
#         except Exception as e:
#             return JsonResponse({"success": False, "error": str(e)})


# from django.contrib.auth import authenticate, login
# from django.shortcuts import render, redirect

# def login_view(request):
#     if request.method == "POST":
#         email = request.POST.get("email")
#         password = request.POST.get("password")
#         user = authenticate(request, username=email, password=password)

#         if user is not None:
#             login(request, user)
#             return render(request , 'Users/dashboard.html')  # or any dashboard view
#         else:
#             return render(request, "Users/login.html", {"error": "Invalid credentials"})
#     return render(request, "Users/login.html")


from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm

# Register View
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'Users/register.html', {'form': form})

# Login View
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('user_dashboard')
    else:
        form = LoginForm()
    return render(request, 'Users/login.html', {'form': form})

# Logout View
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from .models import Contest

def is_admin(user):
    return user.is_superuser or user.is_staff

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    if request.method == "POST":
        title = request.POST.get("title")
        desc = request.POST.get("desc")
        start = request.POST.get("start")
        end = request.POST.get("end")
        
        Contest.objects.create(
            title=title,
            description=desc,
            start_time=start,
            end_time=end,
            created_by=request.user
        )
        return redirect('admin_dashboard')

    contests = Contest.objects.all()
    return render(request, 'Users/admin_dashboard.html', {'contests': contests})


@login_required
def user_dashboard(request):
    contests = Contest.objects.all()
    return render(request, 'Users/user_dashboard.html', {'contests': contests})


from .models import UserAnswer

from .models import Contest, Question, UserAnswer

@login_required
def contest_detail(request, contest_id):
    contest = Contest.objects.get(id=contest_id)
    questions = Question.objects.filter(contest=contest)

    if request.method == "POST":
        for question in questions:
            selected_option = request.POST.get(f"question_{question.id}")
            if selected_option:
                is_correct = selected_option == question.correct_option
                UserAnswer.objects.create(
                    user=request.user,
                    question=question,
                    selected_option=selected_option,
                    is_correct=is_correct
                )
        return redirect('user_dashboard')

    return render(request, 'Users/contest_detail.html', {
        'contest': contest,
        'questions': questions
    })

@login_required
def profile_view(request):
    return render(request , 'Users/Profile.html')


def Rankings(request):
    return render(request, "Users/Rankings.html")