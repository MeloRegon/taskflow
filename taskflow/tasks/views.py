
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializers import (
    TaskCreateSerializer,
    TaskSerializer,
    TaskUpdateSerializer
)
from .services import (
    create_task,
    get_project_tasks,
    get_task,
    update_task,
    delete_task,
)



class TaskListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):

        tasks = get_project_tasks(request.user, project_id)
        if tasks is None:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = TaskSerializer(tasks, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, project_id):
        serializer = TaskCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        task = create_task(
            user=request.user,
            project_id=project_id,
            title=serializer.validated_data['title'],
        )

        if task is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = TaskSerializer(task)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TaskDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, project_id, task_id):
        serializer = TaskUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        task = update_task(
            user=request.user,
            project_id=project_id,
            task_id=task_id,
            **serializer.validated_data
        )

        if task is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(TaskSerializer(task).data, status=status.HTTP_200_OK)


    def delete(self, request, project_id, task_id):
        result = delete_task(
            user=request.user,
            project_id=project_id,
            task_id=task_id,
        )

        if result is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)


    def get(self, request, project_id, task_id):
        task = get_task(request.user, project_id, task_id)

        if task is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)



def demo_page(request):
    project_id = 1

    if request.method == "POST":
        title = request.POST.get("title")

        if title:
            create_task(
                user=request.user,
                project_id=project_id,
                title=title,
            )

        return redirect("demo")

    tasks = get_project_tasks(request.user, project_id)

    if tasks is None:
        tasks = []

    return render(
        request,
        "index.html",
        {
            "tasks": tasks,
        }
    )

def demo_delete_task(request, task_id):
    if request.method == "POST":
        delete_task(
            user=request.user,
            project_id=1,
            task_id=task_id,
        )

    return redirect("demo")