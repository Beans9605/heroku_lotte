# from django.db import connection
# from django.core.signals import request_finished
# from django.dispatch import receiver
# from .models import Cloth

# @receiver (pre_save, sender=Cloth)
# def cloth_pre_save(sender, **kwargs) :
#     image = kwargs['instance'].clothImage
#     sleeveType = kwargs['instance'].sleeveType
#     pantsType = kwargs['instance'].pantsType
#     print(sender.clothImage)

#     if (sleeveType and not pantsType) :
#         for field in sender.meta.fields :
#             if field.name == 'clothImage' :
#                 field.upload_to = 'cloth/sleeve'
#         super(Cloth, sender)
#         print(image.upload_to)
#     elif (pantsType and not sleeveType) :
#         for field in sender.meta.fields :
#             if field.name == 'clothImage' :
#                 field.upload_to = 'cloth/pants'
#         super(Cloth, sender)

#     else :
#         raise InterruptedError



from django.core.signals import request_finished, request_started
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from .models import ViewOfUser, Cloth
from mypage.models import CustomUser
from .views import selectCloth, clothHome, clothDone, CallbackCloth

# 사용자 정의 백단
@receiver(clothDone)
def callback_to_selectCloth(sender, **kwargs) :
    if sender == selectCloth :
        print(kwargs['clothData'])
        try :
            view = ViewOfUser.objects.get(product = kwargs['clothData'])
            view.look += 1
            print('success look now')
            view.save()
        except ViewOfUser.DoesNotExist :
            view = ViewOfUser(
                look=1,
                product = Cloth.objects.get(pk=kwargs['clothData'])
            )
            print('success look')
            view.save()

    else :
        pass


# 사용자 정의 백단 신호보내기
@receiver(clothDone)
def callback_to_clothHome(sender, **kwargs) :
    if sender == clothHome :
        print("Success for acception!")