from django.apps import AppConfig


# class JobConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'job'


class MemberConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Members'

    def ready(self):
        import Members.signals