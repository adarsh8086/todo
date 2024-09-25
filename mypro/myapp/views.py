from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project, Todo
from .forms import ProjectForm, TodoForm
import requests

@login_required
def project_list(request):
    projects = Project.objects.filter(owner=request.user)
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'todos/project_list.html', {'projects': projects, 'form': form})

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    todos = project.todos.all()
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.project = project
            todo.save()
            return redirect('project_detail', project_id=project.id)
    else:
        form = TodoForm()
    return render(request, 'todos/project_details.html', {'project': project, 'todos': todos, 'form': form})

@login_required
def export_project_summary(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    todos = project.todos.all()
    completed_todos = todos.filter(status=True)
    pending_todos = todos.filter(status=False)

    # Prepare the content for the gist
    gist_content = f"# {project.title}\n\n"
    gist_content += f"*Summary*: {len(completed_todos)} / {len(todos)} completed.\n\n"

    gist_content += "## Pending Todos\n"
    for todo in pending_todos:
        gist_content += f"- [ ] {todo.description}\n"

    gist_content += "\n## Completed Todos\n"
    for todo in completed_todos:
        gist_content += f"- [x] {todo.description}\n"

    # Use GitHub API to create a secret gist
    github_token = "YOUR_GITHUB_TOKEN"
    headers = {"Authorization": f"token {github_token}"}
    data = {
        "files": {f"{project.title}.md": {"content": gist_content}},
        "description": f"{project.title} project summary",
        "public": False,
    }
    response = requests.post("https://api.github.com/gists", headers=headers, json=data)

    if response.status_code == 201:
        gist_url = response.json().get('html_url')
        return redirect(gist_url)
    else:
        return render(request, 'todos/export_failed.html')



def mark_as_completed(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    project.is_completed = True
    project.save()
    return redirect('project_detail', project_id=project.id)  # Redirect to the project detail page






@login_required
def mark_project_as_completed(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    project.is_completed = True  # Ensure you have this field in your Project model
    project.save()
    return redirect('project_list')