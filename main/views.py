from datetime import datetime, timedelta, timezone as dt_timezone
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Climb
from .forms import ClimbForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from .predictor import generate_suggestion
from django.contrib.auth import logout
from django.utils import timezone

@login_required
def climbs(request):
    if request.user is None:
        return redirect('login')
    
    user = request.user
    if request.method == "POST":
        form = ClimbForm(request.POST)

        if form.is_valid():
            grade = form.cleaned_data["grade"]
            success = form.cleaned_data["success"]
            attempts = form.cleaned_data["attempts"]
            style = form.cleaned_data["style"]
            notes = form.cleaned_data["notes"]

            climb = Climb(user=user, grade=grade, success=success, attempts=attempts, style=style, notes=notes)
            climb.save()

            user.calculate_flash_grade()
            user.calculate_max_grade()
            user.calculate_level()

            return redirect('climbs')
    else:
        form = ClimbForm()
    return render(request, 'main/climbs.html', {"form": form, "user": user})

@login_required
def delete_climb(request, climb_id):
    if request.user is None:
        return redirect('login')
    
    user = request.user
    climb = get_object_or_404(Climb, id=climb_id)

    if climb.user == user:
        climb.delete()

    user.calculate_flash_grade()
    user.calculate_max_grade()
    user.calculate_level()
    
    return redirect('climbs')

@login_required
def edit_climb(request, climb_id):
    if request.user is None:
        return redirect('climbs')
    
    user = request.user
    climb = get_object_or_404(Climb, id=climb_id)
    
    if climb.user != request.user:
        return redirect('climbs')

    if request.method == 'POST':
        form = ClimbForm(request.POST)
        if form.is_valid():
            grade = form.cleaned_data["grade"]
            success = form.cleaned_data["success"]
            attempts = form.cleaned_data["attempts"]
            style = form.cleaned_data["style"]
            notes = form.cleaned_data["notes"]

            grade_changed = grade != climb.grade
            success_changed = success != climb.success
            attempts_changed = attempts != climb.attempts

            climb.grade = grade
            climb.success = success
            climb.attempts = attempts
            climb.style = style
            climb.notes = notes
            climb.save()

            if grade_changed or success_changed or attempts_changed:
                user.calculate_flash_grade()
                user.calculate_max_grade()
                user.calculate_level()

            return redirect('climbs')
    else:
        form = ClimbForm(instance=climb)

    return render(request, 'main/climbs.html', {
        'form': form,
        'user': user,
        'editing': True
    })


def home(request):
    if request.user is None or not request.user.is_authenticated:	
        return render(request, 'main/home.html')
    
    user = request.user
    preferred_style = user.calculate_preferred_style()
    recent_climbs = Climb.objects.filter(user=request.user).order_by('-date')[:4]
    chart_data= user.get_max_grades_last_six_months()
    return render(request, 'main/home.html', {
        'preferred_style': preferred_style,
        'recent_climbs': recent_climbs,
        'chart_data': chart_data,
    })

@login_required
def style_distribution_data(request):
    user = request.user
    styles = user.get_style_distribution()
    suggestion = generate_suggestion(styles=styles)
    return JsonResponse({'styles': styles, 'suggestion': suggestion})

def about(request):
    return render(request, 'main/about.html')

def comming_soon(request):
    return render(request, 'main/soon.html')

@login_required
def profile(request):
    user = request.user
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()

            return redirect('profile')
    else:
        form = UserProfileForm(instance=user)

    return render(request, 'main/profile.html', {
        'form': form,
        'user': user
    })

@login_required
def delete_account(request):
    if request.method == "POST":
        request.user.delete()
        logout(request)
        return redirect('/')
    return redirect('profile')

def advanced(request):
    return render(request, 'main/advanced.html', {
        'average_grade_data': average_grade_data(request, as_dict=True),
        'grade_distribution_data': grade_distribution_data(request, as_dict=True),
        'success_rate_data': success_rate_data(request, as_dict=True),
        'session_analysis_data': request.user.get_session_analysis()
    })

@login_required
def grade_distribution_data(request, as_dict=False):
    user = request.user
    start_date = get_time_range(request)
    
    # Get climbs within time range using timezone-aware datetime
    climbs = user.climb_set.filter(date__gte=start_date)
    
    # Create grade distribution from V0 to V17
    grades = [f'V{i}' for i in range(18)]
    grade_counts = {grade: 0 for grade in grades}
    
    # Count climbs per grade
    for climb in climbs:
        grade_key = f'V{int(climb.grade)}'
        if grade_key in grade_counts:
            grade_counts[grade_key] += 1

    # Generate colors only for grades with counts > 0
    present_grades = [grade for grade in grades if grade_counts[grade] > 0]
    counts = [grade_counts[grade] for grade in present_grades]
    
    # Predefined vibrant color palette with 18 distinct colors
    color_palette = [
        '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEEAD',   # V0-V4
        '#D4A5A5', '#FF9AA2', '#FFB7B2', '#FFDAC1', '#E2F0CB',   # V5-V9
        '#B5EAD7', '#C7CEEA', '#FFB347', '#FF6961', '#CFCFC4',   # V10-V14
        '#77DD77', '#FDFD96', '#84B082', '#ECA1A6'               # V15-V17
    ]
    
    # Cycle through the palette for present grades
    colors = [color_palette[int(grade[1:]) % len(color_palette)] 
              for grade in present_grades]

    data = {
        'labels': present_grades,
        'datasets': [{
            'label': 'Number of Climbs',
            'data': counts,
            'backgroundColor': colors,
            'borderWidth': 1
        }]
    }
    
    return data if as_dict else JsonResponse(data)

@login_required
def success_rate_data(request, as_dict=False):
    user = request.user
    grades_data = user.get_success_rate(start_date=get_time_range(request))
    labels = list(grades_data.keys())
    success_rates = list(grades_data.values())
    data = {
        'labels': labels,
        'datasets': [{
            'label': 'Success Rate',
            'data': success_rates,
            'backgroundColor': '#1e3c72'
        }]
    }
    return data if as_dict else JsonResponse(data)

@login_required
def average_grade_data(request, as_dict=False):
    user = request.user
    average_grade_data = user.get_average_grade()
    labels = list(average_grade_data.keys())
    average_grades = list(average_grade_data.values())
    data = {
        'labels': labels,
        'datasets': [{
            'label': 'Average Grade',
            'data': average_grades,
            'borderColor': '#2a5298'
        }]
    }
    return data if as_dict else JsonResponse(data)

def get_time_range(request):
    """
    Helper function to calculate date range based on request parameters
    """
    time_range = request.GET.get('time_range', '1')  # Default to 1 months
    now = timezone.now()
    
    # Map time range choices to date calculations
    time_map = {
        '1': now - timedelta(days=30),   # 1 month
        '3': now - timedelta(days=90),   # 3 months
        '6': now - timedelta(days=180),  # 6 months
        '12': now - timedelta(days=365), # 1 year
        '0': timezone.make_aware(datetime.min, dt_timezone.utc) # All time
    }
    
    return time_map.get(time_range, time_map['1'])