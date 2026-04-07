from django.apps import apps
from .models import Task
from workspaces.services import user_is_owner
from projects.models import Project
from workspaces.models import WorkspaceMembership


def get_project_for_user(user, project_id):

    print('USER:', user)
    print('PROJECT:', project_id)

    project = Project.objects.filter(
        id = project_id,
    ).first()

    print('PROJECT:', project)

    if not project:
        return None

    membership = WorkspaceMembership.objects.filter(
        user = user,
        workspace = project.workspace,
    ).first()

    print('MEMBER:', membership)

    if not membership:
        return None

    return project


def create_task(user, project_id, title):

    project = get_project_for_user(user, project_id)

    if not project:
        return None

    return Task.objects.create(title=title, project=project)


def get_project_tasks(user, project_id):
    pass
    # Нужно проверить находиться ли пользователь в проекте , легче всего проверить membership польователя данного проекта
    # Если membership пользователя не найден вообще, значит его нет в данном проекте , значит он не может получить из него Данне
    # Если у пользователя есть membership (OWNER или MEMBER не важно), значит можно вывести task данного проекта

    project = get_project_for_user(user, project_id)

    if not project:
        return None

    return Task.objects.filter(project=project)


def get_task(user, project_id, task_id):
    Task = apps.get_model('tasks', 'Task')

    task = Task.objects.filter(
        id = task_id,
        project_id = project_id,
        project__workspace__workspacemembership__user=user,
    ).first()

    if task is None:
        return None

    return task


def update_task(user, project_id, task_id, **data):
    Task = apps.get_model('tasks', 'Task')

    task = Task.objects.filter(
        id = task_id,
        project_id = project_id,
        project__workspace__workspacemembership__user=user,
    ).first()

    if not task:
        return None

    if 'title' in data:
        task.title = data['title']
    if 'status' in data:
        task.status = data['status']

    task.save()

    return task


def delete_task(user, project_id, task_id):
    Task = apps.get_model('tasks', 'Task')

    task = Task.objects.select_related('project__workspace').filter(
        id = task_id,
        project_id = project_id,
    ).first()

    if not task:
        return None

    if not user_is_owner(user, task.project.workspace):
        return None

    task.delete()

    return True

