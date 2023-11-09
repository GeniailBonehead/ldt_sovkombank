# Слой бизнес-логики приложения
from ldt_app.models import Profile, Task


class Application:
    tasks = []
    users = []

    def __init__(self):
        self._get_tasks()
        self._get_users()

    def _get_tasks(self):
        self.tasks = [task for task in Task.objects.filter().values()]

    def _get_users(self):
        self.users = [profile for profile in Profile.objects.filter(
            active='Active',
        )]

    def count_task(self):
        """Обращение к ML"""
        return count_mock(self.tasks, self.users)


def count_mock(tasks, users):
    """Заглушка расчётов"""
    return {}
