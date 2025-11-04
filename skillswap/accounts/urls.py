from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout_view'),
    path('signup/', views.signup, name='signup'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('earn-credits/', views.earn_credits, name='earn_credits'),
    path('spend-credits/', views.spend_credits, name='spend_credits'),
    path('courses/', views.courses, name='courses'),
    path('enroll/<int:course_id>/', views.enroll, name='enroll'),
    path('unenroll/<int:course_id>/', views.unenroll, name='unenroll'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('add-course/', views.add_course, name='add_course'),
    path('become-instructor/', views.become_instructor, name='become_instructor'),
    path('course/<int:course_id>/add-lesson/', views.add_lesson, name='add_lesson'),
    path('profile/', views.profile, name='profile'),
]
