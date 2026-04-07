from django.db import models

STATUS_TODO = "TODO"
STATUS_DONE = "DONE"
STATUS_IN_PROGRESS = "IN_PROGRESS"
STATUS_CHOICES = (
    (STATUS_TODO, 'Todo'),
    (STATUS_DONE, 'Done'),
    (STATUS_IN_PROGRESS, 'In Progress'),
)


class Task(models.Model):
    title = models.CharField(max_length=100)
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_TODO
    )
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title