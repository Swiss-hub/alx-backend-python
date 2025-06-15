from django.apps import AppConfig

class ChatConfig(AppConfig):
    name = 'Django-Chat'

    def ready(self):
        import Django-Chat.signals