from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import (
    Course, Lesson, LessonProgress, UserProfile,
    Enrollment, Achievement
)
from .forms import AchievementForm

# -----------------------
# Public / Auth Views
# -----------------------
def home(request):
    courses = Course.objects.all()[:8]
    return render(request, 'index.html', {"courses": courses})

def signup(request):
    if request.method == "POST":
        username = request.POST.get('email')
        password = request.POST.get('password')

        # create user
        user = User.objects.create_user(username=username, password=password)
        # ensure userprofile exists
        UserProfile.objects.get_or_create(user=user)
        login(request, user)
        return redirect('dashboard')

    return render(request, 'accounts/signup.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

# -----------------------
# Dashboard / Profile
# -----------------------
@login_required
def dashboard(request):
    enrollments = Enrollment.objects.filter(user=request.user)
    # message handling if passed from other views
    message = request.GET.get('message')
    return render(request, 'accounts/dashboard.html', {
        'enrollments': enrollments,
        'message': message
    })

@login_required
def profile(request):
    profile = request.user.userprofile
    enrollments = Enrollment.objects.filter(user=request.user)
    return render(request, "accounts/profile.html", {
        "profile": profile,
        "enrollments": enrollments,
    })

# -----------------------
# Credits / Simple actions
# -----------------------
@login_required
def earn_credits(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    profile.credits += 5
    profile.save()
    return redirect('dashboard')

@login_required
def spend_credits(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if profile.credits >= 3:
        profile.credits -= 3
        profile.save()
        msg = "Credits deducted."
    else:
        msg = "Not enough credits."
    return redirect(f"/dashboard/?message={msg}")

# -----------------------
# Courses / Search / Filter
# -----------------------
@login_required
def courses(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()

    qs = Course.objects.all()

    if query:
        qs = qs.filter(
            Q(title__icontains=query) |
            Q(instructor__username__icontains=query)
        )

    if category and category != "all":
        qs = qs.filter(category=category)

    return render(request, "accounts/courses.html", {
        "courses": qs,
        "query": query,
        "selected_category": category or "all",
    })

# -----------------------
# Enrollment
# -----------------------
@login_required
def enroll(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    # already enrolled?
    if Enrollment.objects.filter(user=request.user, course=course).exists():
        return redirect('dashboard')

    # check credits
    if profile.credits >= 3:
        profile.credits -= 3
        profile.save()
        Enrollment.objects.create(user=request.user, course=course)
        return redirect('dashboard')
    else:
        # redirect back to courses with message
        return redirect(f"/courses/?message=Not+enough+credits")

@login_required
def unenroll(request, course_id):
    Enrollment.objects.filter(user=request.user, course_id=course_id).delete()
    return redirect("dashboard")

# -----------------------
# Instructor actions
# -----------------------
@login_required
def become_instructor(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    profile.is_instructor = True
    profile.save()
    return redirect('dashboard')

@login_required
def add_course(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if not profile.is_instructor:
        return redirect('dashboard')  # block non-instructors (or show message)

    if request.method == "POST":
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        category = request.POST.get('category', 'other')

        Course.objects.create(
            title=title,
            description=description,
            instructor=request.user,
            category=category
        )

        return render(request, "accounts/add_course.html", {
            "message": "Course added successfully!"
        })

    return render(request, "accounts/add_course.html")

# -----------------------
# Lessons & Progress
# -----------------------
@login_required
def add_lesson(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    # only instructor of this course or global instructor allowed
    if request.user != course.instructor and not profile.is_instructor:
        return redirect('course_detail', course_id=course.id)

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()
        file = request.FILES.get("file")
        video_url = request.POST.get("video_url", "").strip()

        Lesson.objects.create(
            course=course,
            title=title,
            content=content,
            file=file,
            video_url=video_url
        )
        return redirect("course_detail", course_id=course.id)

    return render(request, "accounts/add_lesson.html", {"course": course})

@login_required
def mark_lesson_done(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    LessonProgress.objects.get_or_create(user=request.user, lesson=lesson, defaults={'completed': True})
    return redirect("course_detail", course_id=lesson.course.id)

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = Lesson.objects.filter(course=course).order_by('id')

    enrolled = Enrollment.objects.filter(user=request.user, course=course).exists()

    total_lessons = lessons.count()
    completed_lessons = LessonProgress.objects.filter(
        user=request.user,
        lesson__in=lessons,
        completed=True
    ).count()

    progress = 0
    if total_lessons > 0:
        progress = int((completed_lessons / total_lessons) * 100)

    return render(request, "accounts/course_detail.html", {
        "course": course,
        "lessons": lessons,
        "enrolled": enrolled,
        "progress": progress,
        "completed_lessons": completed_lessons,
        "total_lessons": total_lessons,
    })
    from .models import CourseReview

    if request.method == "POST":
        rating = int(request.POST.get("rating"))
        comment = request.POST.get("comment")        
        CourseReview.objects.update_or_create(
            course=course,
            user=request.user,
            defaults={'rating': rating, 'comment': comment}
        )
        return redirect("course_detail", course_id=course.id)

    return render(request, "accounts/course_detail.html", context)

@login_required
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    # check if student is enrolled
    enrolled = Enrollment.objects.filter(
        user=request.user,
        course=lesson.course
    ).exists()

    if not enrolled:
        return redirect('courses')

    # check lesson progress
    completed = LessonProgress.objects.filter(
        user=request.user, lesson=lesson, completed=True
    ).exists()

    return render(request, "accounts/lesson_detail.html", {
        "lesson": lesson,
        "completed": completed
    })

# -----------------------
# Achievements
# -----------------------
@login_required
def achievements(request):
    achievements = Achievement.objects.filter(user=request.user)

    if request.method == "POST":
        form = AchievementForm(request.POST, request.FILES)
        if form.is_valid():
            achievement = form.save(commit=False)
            achievement.user = request.user
            achievement.save()
            return redirect("achievements")
    else:
        form = AchievementForm()

    return render(request, "accounts/achievements.html", {
        "form": form,
        "achievements": achievements
    })

