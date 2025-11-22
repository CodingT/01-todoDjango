from django.db import models
from django.conf import settings
from django.utils import timezone
class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, related_name='tags')

    class Meta:
        unique_together = (('name', 'owner'),)
        ordering = ['name']

    def __str__(self):
        return self.name

class Task(models.Model):
    PRIORITY_LOW = 1
    PRIORITY_MEDIUM = 2
    PRIORITY_HIGH = 3
    PRIORITY_CHOICES = (
        (PRIORITY_LOW, 'Low'),
        (PRIORITY_MEDIUM, 'Medium'),
        (PRIORITY_HIGH, 'High'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='tasks')
    project = models.ForeignKey(Project, null=True, blank=True, on_delete=models.SET_NULL, related_name='tasks')
    tags = models.ManyToManyField(Tag, blank=True, related_name='tasks')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(null=True, blank=True)

    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    priority = models.PositiveSmallIntegerField(choices=PRIORITY_CHOICES, default=PRIORITY_MEDIUM)
    order = models.PositiveIntegerField(null=True, blank=True, help_text="Optional manual ordering index")

    class Meta:
        ordering = ['completed', 'due_date', '-priority', 'created_at']
        indexes = [
            models.Index(fields=['owner', 'completed']),
            models.Index(fields=['owner', 'due_date']),
        ]

    def __str__(self):
        return self.title

    def mark_complete(self):
        if not self.completed:
            self.completed = True
            self.completed_at = timezone.now()
            self.save(update_fields=['completed', 'completed_at'])

    def mark_incomplete(self):
        if self.completed:
            self.completed = False
            self.completed_at = None
            self.save(update_fields=['completed', 'completed_at'])

    def is_overdue(self):
        if self.due_date and not self.completed:
            return timezone.now() > self.due_date
        return False
        return False
