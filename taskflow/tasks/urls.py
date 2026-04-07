from django.urls import path
from .views import (
    TaskListView,
    TaskDetailView,
    demo_page,
    demo_delete_task
)


urlpatterns = [
    path(
        'projects/<int:project_id>/tasks/',
         TaskListView.as_view(),
         name='tasks'
         ),
    path(
        'projects/<int:project_id>/tasks/<int:task_id>/',
         TaskDetailView.as_view(),
         name='task_detail'
         ),
    path("demo/", demo_page, name="demo"),
    path("demo/delete/<int:task_id>/", demo_delete_task, name="demo_delete_task"),
]