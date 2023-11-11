from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from rest_framework.parsers import JSONParser

from .application import Application
from .models import (
    Gis,
    Profile,
    Task,
    TaskHistory,
)
from .serializers import (
    GisSerializer,
    ProfileSerializer,
    TaskHistorySerializer,
    TaskSerializer,
    UserSerializer,
)


def rights_check(func, role):
    """Инкапсуляция проверки прав"""
    return func()


def index(request):
    return HttpResponse('Главная страница')


def profile_data(request, pk):
    """Получить данные по пользователю"""
    try:
        profile = Profile.objects.select_related('user').get(pk=pk)
    except Profile.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ProfileSerializer(profile)
        data = serializer.data
        data['login'] = profile.user.login
        return JsonResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def auth(request, action):
    if action == 'logout':
        logout(request)
        return HttpResponse('Успешный выход из аккаунта')
    elif request.method == 'POST' and action == 'login':
        user = authenticate(username=request.POST['login'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse('Успешная авторизация')
            else:
                return HttpResponse('Аккаунт неактивен')
        else:
            return HttpResponse('Неверный логин или пароль')
    else:
        return HttpResponse('Не получены учётные данные')


@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def tasks(request):
    """Получить список задач"""
    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TaskSerializer(data=data)
        if serializer and serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def task_data(request, pk):
    """Получить данные по задаче"""
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return JsonResponse(serializer.data)


@csrf_exempt
def task_history(request, pk):
    """Получить историю задач"""
    if request.method == 'GET':
        task_history = TaskHistory.objects.filter(task=pk)
        serializer = TaskHistorySerializer(task_history, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def gis(request, pk):
    """Получить координаты"""
    if request.method == 'GET':
        gis_data = Gis.objects.filter(user=pk)
        serializer = GisSerializer(gis_data, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def count(request):
    """Расчёты"""
    app = Application()
    return JsonResponse(app.count_task())
