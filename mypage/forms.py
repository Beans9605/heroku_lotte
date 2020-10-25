from django import forms
from .models import Image, CustomUser

class ImageForm(forms.ModelForm):
    '''이미지 모델을 위한 폼'''
    class Meta:
        model = Image
        fields = ('title', 'image')

class ProfileForm(forms.ModelForm):
    '''유저 프로필 폼'''
    class Meta:
        model = CustomUser
        fields = [
            #"username",
            "first_name",
            "last_name",
            "email",
            "face_img",
            "weight",
            "height",
            "fit",
            "faceLength",
        ]