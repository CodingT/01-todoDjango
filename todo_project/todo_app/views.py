from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Task


def home(request):
    """Render the simple home page."""
    return render(request, "home.html")


class TaskListView(ListView):
    model = Task
    paginate_by = 25
    template_name = "task_list.html"
    context_object_name = "tasks"


class TaskDetailView(DetailView):
    model = Task
    template_name = "task_detail.html"
    context_object_name = "task"

def mark_complete(request, pk):
    """Mark a task as completed via POST and redirect back to the detail page."""
    # Only allow POST to perform the action; GET redirects to the detail page.
    if request.method != "POST":
        return redirect("task_detail", pk=pk)

    task = get_object_or_404(Task, pk=pk)
    task.mark_complete()
    return redirect("task_detail", pk=pk)


class TaskCreateView(CreateView):
    model = Task
    # simple default form fields; replace with ModelForm via forms.py for custom validation
    fields = [
        "title",
        "description",
        "due_date",
        "priority",
        "completed",
        "project",
    ]
    template_name = "task_form.html"
    success_url = reverse_lazy("task_list")


class TaskUpdateView(UpdateView):
    model = Task
    fields = [
        "title",
        "description",
        "due_date",
        "priority",
        "completed",
        "project",
    ]
    template_name = "task_form.html"
    success_url = reverse_lazy("task_list")


class TaskDeleteView(DeleteView):
    model = Task
    template_name = "task_confirm_delete.html"
    success_url = reverse_lazy("task_list")
