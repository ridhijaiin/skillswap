from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Course, Enrollment, UserProfile


class AccountsSmokeTests(TestCase):
	def setUp(self):
		self.client = Client()

	def test_signup_and_dashboard_access(self):
		resp = self.client.post(reverse('signup'), {'email': 'tuser@example.com', 'password': 'pass1234'}, follow=True)
		self.assertEqual(resp.status_code, 200)
		# dashboard should be accessible
		resp = self.client.get(reverse('dashboard'))
		self.assertEqual(resp.status_code, 200)

	def test_instructor_can_add_course(self):
		# create and login user
		self.client.post(reverse('signup'), {'email': 'inst@example.com', 'password': 'pass1234'}, follow=True)
		# become instructor
		self.client.get(reverse('become_instructor'))
		# add course
		resp = self.client.post(reverse('add_course'), {'title': 'TestCourse', 'description': 'desc', 'category': 'other'}, follow=True)
		self.assertEqual(resp.status_code, 200)
		self.assertTrue(Course.objects.filter(title='TestCourse').exists())

	def test_enrollment_requires_credits_and_then_works(self):
		# create instructor and course
		self.client.post(reverse('signup'), {'email': 'inst2@example.com', 'password': 'pass1234'}, follow=True)
		self.client.get(reverse('become_instructor'))
		self.client.post(reverse('add_course'), {'title': 'CreditCourse', 'description': 'desc', 'category': 'other'}, follow=True)
		course = Course.objects.get(title='CreditCourse')
		# create student
		self.client.logout()
		self.client.post(reverse('signup'), {'email': 'student2@example.com', 'password': 'pass1234'}, follow=True)
		# enroll should fail due to insufficient credits
		resp = self.client.get(reverse('enroll', args=[course.id]), follow=True)
		self.assertEqual(resp.status_code, 200)
		self.assertFalse(Enrollment.objects.filter(user__username='student2@example.com', course=course).exists())
		# give credits and try again
		profile = UserProfile.objects.get(user__username='student2@example.com')
		profile.credits = 5
		profile.save()
		resp = self.client.get(reverse('enroll', args=[course.id]), follow=True)
		self.assertEqual(resp.status_code, 200)
		self.assertTrue(Enrollment.objects.filter(user__username='student2@example.com', course=course).exists())
