from django.db import models
from django.db.models.deletion import SET_NULL
from django.db.models.fields import BLANK_CHOICE_DASH
from mypage.models import CustomUser
from django.utils import timezone
# Create your models here.

class ClothType (models.Model) :
    type = models.CharField(max_length=20)

    def __str__ (self) :
        return self.type

class StandardFit_up (models.Model) :
    # 반팔 긴팔
    clothType = models.ForeignKey(ClothType, on_delete=models.SET_NULL, null=True)
    # S M L XL
    size = models.CharField(max_length=5)
    # 가슴 둘레
    chest = models.IntegerField()
    # 어깨 넓이
    shoulder = models.IntegerField()
    # 팔 길이, 반팔일 때는 null
    sleeve = models.IntegerField(blank=True, null=True)
    # 옷의 총장
    clothGeneral = models.IntegerField()
    
class StandardFit_down(models.Model) :
    # 반바지 긴바지
    clothType = models.ForeignKey(ClothType, on_delete=models.SET_NULL, null=True)
    # S M L XL
    size = models.CharField(max_length=5)
    # 허리
    waistWidth = models.IntegerField()
    # 총 길이
    totalHeight = models.IntegerField()


class Cloth(models.Model) :
    sleeveType = models.BooleanField(default=True)
    pantsType = models.BooleanField(default=False)
    name = models.CharField(max_length=20, unique=True)
    clothImage = models.ImageField(upload_to='cloth/', null=True, blank=True)
    price = models.FloatField(default=0, null=True, blank=True)
    multyFitTypePants = models.ManyToManyField(StandardFit_down, null=True, blank=True)
    multyFitTypeSleeve = models.ManyToManyField(StandardFit_up, null=True, blank=True)


class ViewOfUser(models.Model) : 
    look = models.IntegerField(default=0)
    resently = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Cloth, on_delete=models.CASCADE)