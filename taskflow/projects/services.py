
from .models import Project
from taskflow.workspaces.models import WorkspaceMembership, ROLE_OWNER


def create_project(user, workspace, name):

    membership = WorkspaceMembership.objects.filter(
        user=user,
        workspace=workspace
    ).first()

    if not membership:
        return None

    if membership.role != ROLE_OWNER:
        return None


    return Project.objects.create(
                name=name,
                workspace=workspace
    )


