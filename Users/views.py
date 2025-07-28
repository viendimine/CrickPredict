from django.shortcuts import render
import requests
import json
from django.http import JsonResponse
from django.conf import settings
import os
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


#     url = "https://Cricbuzz-Official-Cricket-API.proxy-production.allthingsdev.co/matches/recent"

#     payload = {}
#     headers = {
#    'x-apihub-key': 'QTljgrtqud7pAQA5XqGNZv6-GTwMg9b47tvuk4zrKmmzvx6kot',
#    'x-apihub-host': 'Cricbuzz-Official-Cricket-API.allthingsdev.co',
#    'x-apihub-endpoint': '8ff18bd6-7f60-45a1-bf9b-4f82b3e4c6ac'
#     }

    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent"
    payload = {}

    headers = {
	"x-rapidapi-key": "356fbb3facmsha25df2559e89a0dp14d3bbjsn03b52f07dc6b",
	"x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)


    response = requests.request("GET", url, headers=headers, data=payload)
    previous_matches_data = response.json()

    previous_matches = []

    for type_match in previous_matches_data.get('typeMatches', []):
        for series in type_match.get('seriesMatches', []):
            matches = series.get('seriesAdWrapper', {}).get('matches', [])
            for match in matches:
                match_info = match.get('matchInfo', {})
                if match_info.get('state') == 'Complete':
                    previous_matches.append({
                        'team1': match_info['team1']['teamName'],
                        'team2': match_info['team2']['teamName'],
                        'matchDesc': match_info['matchDesc'],
                        'status': match_info['status'],
                        'seriesName': match_info['seriesName'],
                        'venue': match_info['venueInfo']['ground'],
                        'city': match_info['venueInfo']['city'],
                        'score1': match.get('matchScore', {}).get('team1Score', {}),
                        'score2': match.get('matchScore', {}).get('team2Score', {}),
                        'team1_img': match_info['team1']['imageId'],
                        'team2_img': match_info['team2']['imageId'],
                    })

    # print(previous_matches)

    live_url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"

    headers = {
	    "x-rapidapi-key": "af63ff1472mshb469cc6f907f78dp19cb37jsnf28e7ad315ed",
	    "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
    }

    live_response = requests.get(live_url, headers=headers)
    
    data = live_response.json()
    live_matches = []

    for type_block in data.get("typeMatches", []):
        match_type = type_block.get("matchType", "Unknown")

        for series in type_block.get("seriesMatches", []):
            wrapper = series.get("seriesAdWrapper")
            if not wrapper:
                continue

            series_id = wrapper.get("seriesId")
            series_name = wrapper.get("seriesName")

            for match in wrapper.get("matches", []):
                match_info = match.get("matchInfo", {})
                match_score = match.get("matchScore", {})

                # Team 1 score details
                team1_inngs = match_score.get("team1Score", {}).get("inngs1", {})
                team1_runs = team1_inngs.get("runs")
                team1_wickets = team1_inngs.get("wickets")
                team1_overs = team1_inngs.get("overs")

                # Team 2 score details
                team2_inngs = match_score.get("team2Score", {}).get("inngs1", {})
                team2_runs = team2_inngs.get("runs")
                team2_wickets = team2_inngs.get("wickets")
                team2_overs = team2_inngs.get("overs")

                # Convert timestamp to readable date
                start_timestamp = match_info.get("startDate")
                if start_timestamp:
                    start_time = datetime.utcfromtimestamp(int(start_timestamp) / 1000).strftime('%d %b %Y %I:%M %p')
                else:
                    start_time = "Not Announced"

                live_matches.append({
                    "match_type": match_type,
                    "series_id": series_id,
                    "series_name": series_name,
                    "match_id": match_info.get("matchId"),
                    "match_desc": match_info.get("matchDesc"),
                    "match_format": match_info.get("matchFormat"),
                    "start_time": start_time,
                    "status": match_info.get("status"),
                    "state": match_info.get("state"),
                    "state_title": match_info.get("stateTitle"),

                    "team1": match_info.get("team1", {}).get("teamName"),
                    "team2": match_info.get("team2", {}).get("teamName"),
                    "team1_sname": match_info.get("team1", {}).get("teamSName"),
                    "team2_sname": match_info.get("team2", {}).get("teamSName"),
                    "team1_img": match_info.get("team1", {}).get("imageId"),
                    "team2_img": match_info.get("team2", {}).get("imageId"),

                    "venue": match_info.get("venueInfo", {}).get("ground"),
                    "city": match_info.get("venueInfo", {}).get("city"),

                    "team1_runs": team1_runs,
                    "team1_wickets": team1_wickets,
                    "team1_overs": team1_overs,

                    "team2_runs": team2_runs,
                    "team2_wickets": team2_wickets,
                    "team2_overs": team2_overs,
                })







    #rajvishap52@gmail.com
    # url = "https://Cricbuzz-Official-Cricket-API.proxy-production.allthingsdev.co/news"

    # payload = {}
    # headers = {
    # 'x-apihub-key': 'QTljgrtqud7pAQA5XqGNZv6-GTwMg9b47tvuk4zrKmmzvx6kot',
    # 'x-apihub-host': 'Cricbuzz-Official-Cricket-API.allthingsdev.co',
    # 'x-apihub-endpoint': 'b02fb028-fcca-4590-bf04-d0cd0c331af4'
    # }

    url = "https://Cricbuzz-Official-Cricket-API.proxy-production.allthingsdev.co/news"

    payload = {}
    headers = {
        'x-apihub-key': 'oeP1UQOfy7TfWS-r4Hbe5BaIG9CeMlIulJ4c9vtrMkN0SmfU3L',
        'x-apihub-host': 'Cricbuzz-Official-Cricket-API.allthingsdev.co',
        'x-apihub-endpoint': 'b02fb028-fcca-4590-bf04-d0cd0c331af4'
}

    response = requests.request("GET", url, headers=headers, data=payload)


    # print(response.text)
    data = response.json()
    stories = []
    for item in data.get("storyList", []):
        story = item.get("story", {})
        stories.append({
            "headline": story.get("hline"),
            "intro": story.get("intro"),
            "context": story.get("context"),
            "published": story.get("pubTime"),
            "image_id": story.get("imageId"),
            "caption": story.get("coverImage", {}).get("caption"),
            "seoHeadline": story.get("seoHeadline"),
            "source": story.get("source"),
            "news_id" :story.get("id")
            })
        
    print(stories)


# Then define context
    context = {
    "current_matches": current_matches,
    "upcoming_matches": upcoming_matches,
    "previous_matches": previous_matches,
    "all_leagues": all_leagues,
    "stories" : stories,
    "live_matches" : live_matches
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

    # print(response.text)



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


# def Rankings(request):
#     return render(request, "Users/Rankings.html")


def Rankings(request):

    # url = "https://cricket-live-line1.p.rapidapi.com/teamRanking/1"

    # headers = {
	# "x-rapidapi-key": "356fbb3facmsha25df2559e89a0dp14d3bbjsn03b52f07dc6b",
	# "x-rapidapi-host": "cricket-live-line1.p.rapidapi.com"
    # }
    # data = response.json()

    # response = requests.get(url, headers=headers)

    ### Test Rankings
    with open("Users/Data/test.json", "r") as f:
        data = json.load(f)

    with open("Users/Data/Flags.json", "r") as f:
        Flags = json.load(f)
    


    test_data = []
    for team in data[:10]:
        test_data.append({
            "rank": team["rank"],
            "rating": team["rating"],
            "points": team["points"],
            "team": team["team"],
            "image": Flags.get(team["team"], "")
    }) 
        
    ### ODIs Rankings

    with open("Users/Data/ODI.json", "r") as f:
        data = json.load(f)

    with open("Users/Data/Flags.json", "r") as f:
        Flags = json.load(f)
    


    ODI_data = []
    for team in data[:10]:
        ODI_data.append({
            "rank": team["rank"],
            "rating": team["rating"],
            "points": team["points"],
            "team": team["team"],
            "image": Flags.get(team["team"], "")
    }) 
        
    ### T20Is Ranking

    with open("Users/Data/T20Is.json", "r") as f:
        data = json.load(f)

    with open("Users/Data/Flags.json", "r") as f:
        Flags = json.load(f)
    


    T20Is_data = []
    for team in data[:10]:
        T20Is_data.append({
            "rank": team["rank"],
            "rating": team["rating"],
            "points": team["points"],
            "team": team["team"],
            "image": Flags.get(team["team"], "")
    }) 
    ## ODI Women Team Ranking

    with open("Users/Data/ODI_Women.json", "r") as f:
        data = json.load(f)

    with open("Users/Data/Flags.json", "r") as f:
        Flags = json.load(f)
    


    ODI_Women_data = []
    for team in data[:10]:
        cleaned_team = team["team"].replace(" Women", "")
        ODI_Women_data.append({
            "rank": team["rank"],
            "rating": team["rating"],
            "points": team["points"],
            "team": team["team"],
            "image": Flags.get(cleaned_team, "")
    }) 


    ##T20Is Women Team Ranking

    with open("Users/Data/T20Is_Women.json", "r") as f:
        data = json.load(f)

    with open("Users/Data/Flags.json", "r") as f:
        Flags = json.load(f)
    


    T20Is_Women_data = []
    for team in data[:10]:
        cleaned_team = team["team"].replace(" Women", "")
        T20Is_Women_data.append({
            "rank": team["rank"],
            "rating": team["rating"],
            "points": team["points"],
            "team": team["team"],
            "image": Flags.get(cleaned_team, "")
    }) 

    # print(test_data)



    # url = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/rankings/batsmen"

    # querystring = {"formatType":"test"}

    # headers = {
	# "x-rapidapi-key": "356fbb3facmsha25df2559e89a0dp14d3bbjsn03b52f07dc6b",
	# "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
    # }

    # response = requests.get(url, headers=headers, params=querystring)
    ### T20Is Batsmen Rankings

    with open("Users/Data/T20Is_batters.json", "r") as f:
        data = json.load(f)
    T20Is_players = []
    

    for player in data[:10]:
        T20Is_players.append({
        "rank": player.get("rank"),
        "name": player.get("player"),
        "country": player.get("team"),
        "points": player.get("points"),
        "image": f"T20Is_Player_Images/{player.get('player')}.jpg",
    })
        
    # print(T20Is_players)
    ### ODIS Batsmen Rankings

    with open("Users/Data/ODI_batters.json", "r") as f:
        data = json.load(f)
    ODI_players = []
    

    for player in data[:10]:
        ODI_players.append({
        "rank": player.get("rank"),
        "name": player.get("player"),
        "country": player.get("team"),
        "points": player.get("points"),
        "image": f"ODI_Player_Images/{player.get('player')}.jpg",
    })
        


    ### Test Batsmen Rankings
    with open("Users/Data/Test_batters.json", "r") as f:
        data = json.load(f)
    Test_players = []
    

    for player in data[:10]:
        Test_players.append({
        "rank": player.get("rank"),
        "name": player.get("player"),
        "country": player.get("team"),
        "points": player.get("points"),
        "image": f"Test_Player_Images/{player.get('player')}.jpg",
    })
        

    ## ODI Women Batting Rankings

    with open("Users/Data/ODI_Women_batters.json", "r") as f:
        data = json.load(f)
    ODI_Women_players = []
    

    for player in data[:10]:
        ODI_Women_players.append({
        "rank": player.get("rank"),
        "name": player.get("name"),
        "country": player.get("country"),
        "rating": player.get("rating"),
        "image": f"ODI_Women_Images/{player.get('name')}.jpg",
    })
        
    ## T20Is Women Batting Rankings

    with open("Users/Data/T20Is_Women_batters.json", "r") as f:
        data = json.load(f)
    T20Is_Women_players = []
    

    for player in data[:10]:
        T20Is_Women_players.append({
        "rank": player.get("rank"),
        "name": player.get("name"),
        "country": player.get("country"),
        "rating": player.get("rating"),
        "image": f"T20Is_Women_Images/{player.get('name')}.jpg",
    })
        
        
    # print(players)



    return render(request, "Users/Rankings.html", {
        "test_data": test_data,
        "ODI_data": ODI_data,
        "T20Is_data": T20Is_data,
        "Test_players": Test_players,
        "T20Is_players" : T20Is_players,
        "ODI_players" : ODI_players,
        "ODI_Women_data" : ODI_Women_data,
        "T20Is_Women_data" : T20Is_Women_data,
        "ODI_Women_players" : ODI_Women_players,
        "T20Is_Women_players" : T20Is_Women_players
        })



def News(request):
    
    url = "https://cricket-live-line1.p.rapidapi.com/news"

    headers = {
	    "x-rapidapi-key": "356fbb3facmsha25df2559e89a0dp14d3bbjsn03b52f07dc6b",
	    "x-rapidapi-host": "cricket-live-line1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    data = response.json()
    # print(data)
    stories = []
    for article in data['data']:
        title = article.get('title')
        image = article.get('image')
        desciption = article.get('description')
        content = article.get('content')
        news_id = article.get('news_id')
        stories.append(article)


    return render(request, "Users/News.html",{
    "stories": stories 
})

def news_detail(request, news_id):
    import requests

    url = "https://Cricbuzz-Official-Cricket-API.proxy-production.allthingsdev.co/news"

    payload = {}
    headers = {
        'x-apihub-key': 'oeP1UQOfy7TfWS-r4Hbe5BaIG9CeMlIulJ4c9vtrMkN0SmfU3L',
        'x-apihub-host': 'Cricbuzz-Official-Cricket-API.allthingsdev.co',
        'x-apihub-endpoint': 'b02fb028-fcca-4590-bf04-d0cd0c331af4'
}

    response = requests.get(url, headers=headers)
    data = response.json()
    print(data)

    selected_news = None

    for item in data.get("storyList", []):
        story = item.get("story", {})
        if story.get("id") == news_id:
            selected_news = {
                "headline": story.get("hline"),
                "intro": story.get("intro"),
                "context": story.get("context"),
                "published": story.get("pubTime"),
                "image_id": story.get("imageId"),
                "caption": story.get("coverImage", {}).get("caption"),
                "seoHeadline": story.get("seoHeadline"),
                "source": story.get("source"),
                "news_id": story.get("id")
            }
            break  # Stop after finding the first matching one

    if selected_news:
        return render(request, 'Users/news_detail.html', {'news': selected_news})
    else:
        return render(request, 'Users/news_detail.html', {'error': 'News article not found'})


def scorecard(request):
    live_url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"

    headers = {
	    "x-rapidapi-key": "af63ff1472mshb469cc6f907f78dp19cb37jsnf28e7ad315ed",
	    "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
    }

    live_response = requests.get(live_url, headers=headers)
    
    data = live_response.json()
    scorecard = []

    for type_block in data.get("typeMatches", []):
        match_type = type_block.get("matchType", "Unknown")

        for series in type_block.get("seriesMatches", []):
            wrapper = series.get("seriesAdWrapper")
            if not wrapper:
                continue

            series_id = wrapper.get("seriesId")
            series_name = wrapper.get("seriesName")

            for match in wrapper.get("matches", []):
                match_info = match.get("matchInfo", {})
                match_score = match.get("matchScore", {})

                team1_inngs = match_score.get("team1Score", {}).get("inngs1", {})
                team1_runs = team1_inngs.get("runs")
                team1_wickets = team1_inngs.get("wickets")
                team1_overs = team1_inngs.get("overs")

                team2_inngs = match_score.get("team2Score", {}).get("inngs1", {})
                team2_runs = team2_inngs.get("runs")
                team2_wickets = team2_inngs.get("wickets")
                team2_overs = team2_inngs.get("overs")

                # Convert timestamp to readable date
                start_timestamp = match_info.get("startDate")
                if start_timestamp:
                    start_time = datetime.utcfromtimestamp(int(start_timestamp) / 1000).strftime('%d %b %Y %I:%M %p')
                else:
                    start_time = "Not Announced"

                scorecard.append({
                    "series_id": series_id,
                    "series_name": series_name,
                    "match_id": match_info.get("matchId"),
                    "start_time": start_time,
                    "status": match_info.get("status"),
                    "state": match_info.get("state"),
                    "state_title": match_info.get("stateTitle"),

                    "team1": match_info.get("team1", {}).get("teamName"),
                    "team2": match_info.get("team2", {}).get("teamName"),
                    "team1_sname": match_info.get("team1", {}).get("teamSName"),
                    "team2_sname": match_info.get("team2", {}).get("teamSName"),
                    "team1_img": match_info.get("team1", {}).get("imageId"),
                    "team2_img": match_info.get("team2", {}).get("imageId"),

                    "venue": match_info.get("venueInfo", {}).get("ground"),
                    "city": match_info.get("venueInfo", {}).get("city"),

                    "team1_runs": team1_runs,
                    "team1_wickets": team1_wickets,
                    "team1_overs": team1_overs,

                    "team2_runs": team2_runs,
                    "team2_wickets": team2_wickets,
                    "team2_overs": team2_overs,
                })

    return render(request , "Users/scorecard.html",{'scorecard' : scorecard})

def team_details(request, team_name):
    import json

    with open("Users/Data/test.json", "r") as f:
        data = json.load(f)

    with open("Users/Data/Flags.json", "r") as f:
        Flags = json.load(f)

    test_data = []
    selected_team_data = None

    for team in data[:10]:
        team_info = {
            "rank": team["rank"],
            "rating": team["rating"],
            "points": team["points"],
            "team": team["team"],
            "image": Flags.get(team["team"], "")
        }

        test_data.append(team_info)

        if team["team"].lower() == team_name.lower():
            selected_team_data = team_info

<<<<<<< HEAD
=======
    # print(test_data)

    with open("Users/Data/Cricket_Players/India_Cricket_Players.json", "r") as f:
        data = json.load(f)

    with open("Users/Data/Country_CricketBoard.json", "r") as f:
        countries = json.load(f)

    
    country_info = next((c for c in countries if c["name"].lower() == team_name.lower()), None)
    if not country_info:
        return render(request, "Users/team_details.html", {"error": "Country not found."})

    country_name = country_info["name"]
    cricket_board = country_info.get("CB", "Unknown")
    file_path = f"Users/Data/Cricket_Players/{country_name}_Cricket_Players.json"

   
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return render(request, "Users/team_details.html", {"error": "Player data missing for this country."})

    try:
        with open(file_path, "r", encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return render(request, "Users/team_details.html", {"error": "Invalid JSON for this country."})

    
    def build_player_list(player_list):
        result = []
        for p in player_list:
            name = p["name"] if isinstance(p, dict) and "name" in p else p
            image = p["image"]
            result.append({
                "name": name,
                "image" : image,
            })
        return result

    All_players = build_player_list(data.get("All Players", []))
    Batting = build_player_list(data.get("Batsmen", []))
    Bowling = build_player_list(data.get("Bowlers", []))
    AllRounder = build_player_list(data.get("All Rounders", []))

    print(All_players)


>>>>>>> 41c0f55 (Added all Team Players Images)
    return render(
        request,
        "Users/team_details.html",
        {
            'test_data': test_data,
<<<<<<< HEAD
            'team': selected_team_data,       
            'team_name': team_name           
=======
            'team': selected_team_data,
            'team_name': team_name,
            'All_players': All_players,
            'Batting': Batting,
            'Bowling': Bowling,
            'AllRounder': AllRounder
>>>>>>> 41c0f55 (Added all Team Players Images)
        }
    )