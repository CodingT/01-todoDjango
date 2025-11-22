from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Task


class TaskModelTests(TestCase):
	def test_mark_complete_and_incomplete(self):
		t = Task.objects.create(title="Test")
		self.assertFalse(t.completed)
		self.assertIsNone(t.completed_at)

		t.mark_complete()
		t.refresh_from_db()
		self.assertTrue(t.completed)
		self.assertIsNotNone(t.completed_at)

		t.mark_incomplete()
		t.refresh_from_db()
		self.assertFalse(t.completed)
		self.assertIsNone(t.completed_at)

	def test_is_overdue(self):
		past = timezone.now() - timezone.timedelta(days=1)
		future = timezone.now() + timezone.timedelta(days=1)

		t1 = Task.objects.create(title="Past due", due_date=past)
		t2 = Task.objects.create(title="Future", due_date=future)
		t3 = Task.objects.create(title="Completed", due_date=past, completed=True)

		self.assertTrue(t1.is_overdue())
		self.assertFalse(t2.is_overdue())
		self.assertFalse(t3.is_overdue())


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
		# prefer asserting side-effects (object created) rather than exact redirect behavior
		self.assertTrue(Task.objects.filter(title="Created via view").exists())

	def test_update_view_updates_task(self):
		url = reverse("task_update", args=[self.t.pk])
		resp = self.client.post(url, {"title": "Updated", "description": "x", "priority": "2", "completed": ""})
		# assert update persisted
		self.t.refresh_from_db()
		self.assertEqual(self.t.title, "Updated")

	def test_delete_view_deletes_task(self):
		url = reverse("task_delete", args=[self.t.pk])
		resp = self.client.post(url)
		self.assertEqual(resp.status_code, 302)
		self.assertFalse(Task.objects.filter(pk=self.t.pk).exists())


