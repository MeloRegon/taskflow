from django.db import transaction
from .models import Workspace, WorkspaceMembership, ROLE_OWNER


def create_workspace(user, name):

    with transaction.atomic():


        workspace = Workspace.objects.create(
            name=name
        )

        WorkspaceMembership.objects.create(
            user=user,
            workspace=workspace,
            role=ROLE_OWNER,
        )

    return workspace


def user_is_owner(user, workspace):

    membership = WorkspaceMembership.objects.filter(
        user=user, workspace=workspace
    ).first()

    if membership and  membership.role == ROLE_OWNER:
        return True
    return False


