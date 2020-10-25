from django.shortcuts import redirect, render, get_object_or_404
from .models import Cloth, ViewOfUser, StandardFit_up, StandardFit_down
# 옷 조회 관리용 시그널
from django.dispatch import Signal
# 시간대 별 추천 라인 반환용 모듈
import datetime, time
from datetime import timedelta
from django.db.models import Max

# qr 코드 인식용 모듈
import pyzbar.pyzbar as pyzbar
import cv2
import matplotlib.pyplot as plt
import numpy as np

# ----------------------------------------------- 옷 종류 검색 ---------
import sys
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
API_URL = 'https://dapi.kakao.com/v2/vision/product/detect'
MYAPP_KEY = 'c3b6b008909cc21e1ec48f7afae2122a'

def detect_product(image):
    # headers = {'Authorization': 'KakaoAK {}'.format(MYAPP_KEY), "Content-Type" : "multipart/form-data"}
    headers = {'Authorization': 'KakaoAK {}'.format(MYAPP_KEY), "Content-Type" : "multipart/form-data"}

    try:
        
        resp = requests.post(API_URL, headers=headers, data=image)
        print(resp)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(str(e))
        sys.exit(0)
# ----------------------------------------------------------------------


# -------------------- 시그널 보내기 : 옷 조회 기록 ----------------------
clothDone = Signal()


# 콜백함수
class CallbackCloth :

    def send_done(self, clothData) :
        clothDone.send(sender=self, clothData=clothData)


# 추천 알고리즘

class Recommend() :
    def recommend_of_resently(self) :
        now_date = datetime.datetime.now()
        resently_days = now_date + timedelta(days=-7)
        resently_view = ViewOfUser.objects.filter(resently__range =[resently_days, now_date])

        reslook = 0

        respk = resently_view

        for res in resently_view :
            if res.look >= reslook :
                reslook = res.look
                respk = res
        
        
        
            
        
        # view = {'resently_view' : resently_view}

        if respk :
            return respk
        else :
            return None
    
    def recommend_of_best(self) :
        best_view = ViewOfUser.objects.all()
        # view = {'best_view' : best_view}

        reslook = 0

        respk = best_view

        for res in best_view :
            if res.look >= reslook :
                reslook = res.look
                respk = res

        
        if respk :
            return respk
        else :
            return None
        

# Create your views here.


# 홈 화면에서는 모든 옷들을 보여주고, 하단에 추천 옷을 골라준다.
def clothHome(request) :
    cloths = Cloth.objects.all()
    clothRecommend = Recommend()

    # if request.user :
    #     print(request.user.id)
    #     user_views = ViewOfUser.objects.filter(users=request.user)
    #     resently_views = clothRecommend.recommend_of_resently()
    #     best_views = clothRecommend.recommend_of_best()
    #     context = {'cloths' : cloths, 'user_views' : user_views, 'resently_views' : resently_views, 'best_views' : best_views}
    # else :
    try :
        resently_views = clothRecommend.recommend_of_resently()
        print(resently_views.product.clothImage.url)
        best_views = clothRecommend.recommend_of_best()
        context = {'cloths' : cloths, 'resently_views' : resently_views, 'best_views' : best_views}
        return render(request, "cloth/clothHome.html", context)
    except :
        context = {'cloths' : cloths}
        return render(request, "cloth/clothHome.html", context)

# def clothSearch(request) :
#     if request.method == "POST" :

# 셀렉하게 되면 자동적으로 뷰를 생성해주고, 디테일한 화면을 띄워준다.
def selectCloth(request, pk) :
    try :
        clothData = Cloth.objects.get(pk=pk)
        if clothData.sleeveType :
            StandardFit = StandardFit_up.objects.all()
        elif clothData.pantsType :
            StandardFit = StandardFit_down.objects.all()
        else :
            redirect('clothHome')

        context = {'cloth' : clothData, 'standardfit' : StandardFit }
        # signal을 이용한 신호를 받아서 데이터 조회 이후에 조회수 및 정보 저장 별도
        CallbackCloth.send_done(selectCloth, clothData=pk)
        return render(request, "cloth/clothSelect.html", context)
    except Cloth.DoesNotExist :
        return redirect('clothHome')

def select(request):
    if request.method == 'POST':
        name = request.POST['name']
        cloth = Cloth.objects.filter(name=name)
        context = {'select': cloth}
        return render(request, 'cloth/clothHome.html', context)


# def shoppingPage (self, request) :
#     if request.method == 'POST' :
#         cloths = request.POST['cloths']

# def test_image(request) :
#     print(request.FILES['img'])
#     file = {'image' : request.FILES['img']}

#     cloth = Cloth.objects.get(name='black_pants')

#     file2 = {'image' : open(cloth.clothImage.path, 'rb')}
#     print(detect_product(file2))
    
#     return redirect('clothHome')

# qr코드 확인
def qr_code_authenticate(request) :
    img2 = request.FILES['qr-code']

    byte_img = bytes(0)

    for img3 in img2 :
        byte_img += img3
    
    encoded_img = np.fromstring(byte_img, dtype = np.uint8)
    img = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)
    # qr_code = cv2.imread(img, 1)

    # plt.imshow(img)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    decoded = pyzbar.decode(gray)

    cloths = []

    for d in decoded :
        print(d.data.decode('utf-8'))
        print(d.type)
    
        d.data.decode('utf-8')
        try :
            cloths.append(Cloth.objects.get(pk = d.data.decode('utf-8')))
        except Cloth.DoesNotExist :
            return redirect('clothHome')

    print(cloths)
    for cloth in cloths :
        return redirect('selectCloth', pk=cloth.pk)
