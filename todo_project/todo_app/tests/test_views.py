from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from ..models import Task


class TaskViewsTests(TestCase):
    def setUp(self):
        # create a sample task
        self.t = Task.objects.create(title="View Task", description="desc")

    def test_list_view_shows_task(self):
        resp = self.client.get(reverse("task_list"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "View Task")

    def test_detail_view(self):
        resp = self.client.get(reverse("task_detail", args=[self.t.pk]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.t.title)

    def test_create_view_creates_task(self):
        data = {
            "title": "Created via view",
            "description": "from test",
            "priority": "2",
            "completed": "",
        }
        resp = self.client.post(reverse("task_create"), data)
        # may redirect (302) or re-render form (200) on validation; ensure object created
        self.assertTrue(Task.objects.filter(title="Created via view").exists())

    def test_update_view_updates_task(self):
        url = reverse("task_update", args=[self.t.pk])
        resp = self.client.post(url, {"title": "Updated", "description": "x", "priority": "2", "completed": ""})
        # either redirect or re-render; ensure update persisted
        self.t.refresh_from_db()
        self.assertEqual(self.t.title, "Updated")

    def test_delete_view_deletes_task(self):
        url = reverse("task_delete", args=[self.t.pk])
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=self.t.pk).exists())
