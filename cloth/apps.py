from django.apps import AppConfig


class ClothConfig(AppConfig):
    name = 'cloth'
    verbose_name = "Cloth Configure for Cloth Model"
    def ready(self):
        import cloth.signals