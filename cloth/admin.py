from django.contrib import admin
from .models import Cloth, StandardFit_down, StandardFit_up, ClothType, ViewOfUser
# Register your models here.

admin.site.register(Cloth)
admin.site.register(StandardFit_down)
admin.site.register(StandardFit_up)
admin.site.register(ClothType)
admin.site.register(ViewOfUser)