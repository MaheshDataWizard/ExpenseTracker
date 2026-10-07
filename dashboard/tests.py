from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class DashboardMonthYearSelectorTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="dashboard-user",
            email="dashboard@example.com",
            password="StrongPass123!",
        )

    def test_dashboard_page_has_month_and_year_selectors(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn('id="monthSelector"', content)
        self.assertIn('id="yearSelector"', content)
