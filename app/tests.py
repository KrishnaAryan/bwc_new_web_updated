from django.test import TestCase, Client
from django.urls import reverse
from .models import ContactMessage, BookTestRode, BlogPost, Job
from django.utils import timezone
from datetime import timedelta

class ViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.blog_post = BlogPost.objects.create(
            title="Test Blog",
            content="Test Content",
            click_count=50,
            date=timezone.now(),
            slug="test-blog"
        )
        self.job = Job.objects.create(
            title="Test Job",
            description="Test Description",
            is_open=True
        )
        self.closed_job = Job.objects.create(
            title="Closed Job",
            description="Closed Description",
            is_open=False
        )

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_about_view(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about-us.html')

    def test_why_ecoyan_view(self):
        response = self.client.get(reverse('why_ecoyan'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'why-ecoyan.html')

    def test_certification_view(self):
        response = self.client.get(reverse('certification'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'certification.html')

    def test_customers_view(self):
        response = self.client.get(reverse('customers'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customers.html')

    def test_photos_view(self):
        response = self.client.get(reverse('photos'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'photos.html')

    def test_e_rickshaw_view(self):
        response = self.client.get(reverse('e_rickshaw'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'e-rickshaw.html')

    def test_e_cargo_view(self):
        response = self.client.get(reverse('e_cargo'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'e-cargo.html')

    def test_e_garbage_view(self):
        response = self.client.get(reverse('e_garbage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'e-garbage.html')

    def test_golf_cart_view(self):
        response = self.client.get(reverse('golf_cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'golf-cart.html')

    def test_car_view(self):
        response = self.client.get(reverse('car'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'car.html')

    def test_contact_view_get(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')

    def test_contact_view_post(self):
        response = self.client.post(reverse('contact'), {
            'Name': 'Test User',
            'Email': 'test@example.com',
            'phone': '1234567890',
            'message': 'Test Message'
        })
        self.assertEqual(response.status_code, 302)  # Check for redirect

    def test_dealer_view_get(self):
        response = self.client.get(reverse('dealer'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dealer.html')

    def test_dealer_view_post(self):
        response = self.client.post(reverse('dealer'), {
            'Name': 'Test User',
            'Email': 'test@example.com',
            'phone': '1234567890',
            'message': 'Test Message'
        })
        self.assertEqual(response.status_code, 302)  # Check for redirect

    def test_book_test_ride_view_get(self):
        response = self.client.get(reverse('book_test_ride'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_test_ride.html')

    def test_book_test_ride_view_post(self):
        response = self.client.post(reverse('book_test_ride'), {
            'Name': 'Test User',
            'Email': 'test@example.com',
            'Phone': '1234567890',
            'State': 'Test State',
            'City': 'Test City',
            'Purpose': 'Test Purpose',
            'Message': 'Test Message'
        })
        self.assertEqual(response.status_code, 302)  # Check for redirect

    def test_success_view(self):
        response = self.client.get(reverse('success_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'success.html')

    def test_custom_404_view(self):
        response = self.client.get('/non-existent-page/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_blogs_view(self):
        response = self.client.get(reverse('blogs'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs.html')

    def test_blog_details_view(self):
        response = self.client.get(reverse('blogs_details', args=[self.blog_post.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog_detalils.html')

    def test_job_list_view(self):
        response = self.client.get(reverse('job_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'careers.html')

    def test_job_detail_view(self):
        response = self.client.get(reverse('job_detail', args=[self.job.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'job_detail.html')

    def test_apply_for_job_view_get(self):
        response = self.client.get(reverse('apply_for_job', args=[self.job.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'apply_for_job.html')

    def test_apply_for_job_view_post(self):
        with open('test_resume.pdf', 'w') as file:
            file.write('Test resume content.')
        with open('test_resume.pdf', 'rb') as resume:
            response = self.client.post(reverse('apply_for_job', args=[self.job.pk]), {
                'name': 'Test User',
                'email': 'test@example.com',
                'phone': '1234567890',
                'resume': resume
            })
        self.assertEqual(response.status_code, 302)  # Check for redirect

    def test_apply_for_closed_job(self):
        response = self.client.get(reverse('apply_for_job', args=[self.closed_job.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'job_closed.html')

    def test_privacy_policy_view(self):
        response = self.client.get(reverse('PrivacyPolicy'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'PrivacyPolicy.html')

    def test_terms_conditions_view(self):
        response = self.client.get(reverse('TermsConditions'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Terms&Conditions.html')

    def test_product_view(self):
        response = self.client.get(reverse('Product'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product.html')
