from django.db import models
from django.conf import settings

ROLE_OWNER = 'OWNER'
ROLE_MEMBER = 'MEMBER'
ROLE_CHOICES = (
    (ROLE_OWNER, 'Owner'),
    (ROLE_MEMBER, 'Member'),
)


class Workspace(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class WorkspaceMembership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'workspace'],
                name='unique_workspace_membership'
            )
        ]

    def __str__(self):
        return f"{self.user} → {self.workspace} ({self.role})"

