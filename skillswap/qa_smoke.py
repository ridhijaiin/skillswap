"""
Quick QA smoke script to exercise signup, dashboard, become-instructor, add-course and enrollment flows.
Run this from the inner project folder with the project's venv activated.
Prints step results and any exception tracebacks.
"""
import os,sys,traceback
sys.path.insert(0, r'C:\Users\Lenovo\Desktop\skillswap\skillswap')
os.environ.setdefault('DJANGO_SETTINGS_MODULE','skillswap.settings')
import django
django.setup()
from django.test import Client
from django.contrib.auth.models import User
from accounts.models import Course, Enrollment

c = Client()

def safe(action_name, fn, *args, **kwargs):
    try:
        res = fn(*args, **kwargs)
        print(f"{action_name}: OK -> {getattr(res,'status_code',res)}")
        return res
    except Exception as e:
        print(f"{action_name}: EXCEPTION: {e}")
        traceback.print_exc()
        return None

# 1) Signup instructor user
resp = safe('signup_instructor_post', lambda: c.post('/signup/', {'email':'instructor@example.com','password':'pass1234'}, follow=True))
# 1b) fetch dashboard
resp = safe('dashboard_after_signup_get', lambda: c.get('/dashboard/'))

# 2) Become instructor
resp = safe('become_instructor_get', lambda: c.get('/become-instructor/', follow=True))

# 3) Add course
resp = safe('add_course_post', lambda: c.post('/add-course/', {'title':'QA Test Course','description':'A test','category':'programming'}, follow=True))
# verify course created
try:
    created = Course.objects.filter(title='QA Test Course').count()
    print(f'courses_created: {created}')
except Exception as e:
    print('courses_created: EXCEPTION')
    traceback.print_exc()

# 4) Create student user and enroll
safe('logout', lambda: c.logout())
resp = safe('signup_student_post', lambda: c.post('/signup/', {'email':'student@example.com','password':'pass1234'}, follow=True))
try:
    course = Course.objects.filter(title='QA Test Course').first()
    if course:
        enroll_path = f'/enroll/{course.id}/'
        resp = safe('student_enroll_get', lambda: c.get(enroll_path, follow=True))
        try:
            student = User.objects.get(username='student@example.com')
            enrolled = Enrollment.objects.filter(user=student, course=course).exists()
            print(f'enrolled_exists: {enrolled}')
        except Exception as e:
            print('check_enrolled: EXCEPTION')
            traceback.print_exc()
    else:
        print('student_enroll_get: SKIPPED (no course)')
except Exception as e:
    print('enroll flow: EXCEPTION')
    traceback.print_exc()

print('QA script complete')
