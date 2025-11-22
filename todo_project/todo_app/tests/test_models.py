from django.test import TestCase
from django.utils import timezone
from ..models import Task


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
