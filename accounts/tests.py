from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class LandingPageAuthFlowTests(TestCase):
    def test_anonymous_user_is_sent_to_login_from_root(self):
        response = self.client.get(reverse("home"), follow=False)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

    def test_authenticated_user_is_sent_to_dashboard_from_root(self):
        user = get_user_model().objects.create_user(
            username="testuser",
            email="test@example.com",
            password="StrongPass123!",
        )
        self.client.force_login(user)

        response = self.client.get(reverse("home"), follow=False)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("dashboard"))

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard"), follow=False)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('dashboard')}")
