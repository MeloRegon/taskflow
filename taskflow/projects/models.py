from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=200)
    workspace = models.ForeignKey(
        'workspaces.Workspace',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name