"""
URL configuration for Dongstagram project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import Sub
from content.views import Main, UploadFeed
from .settings import MEDIA_ROOT, MEDIA_URL
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', Main.as_view()),
    path('content/', include('content.urls')),
    path('user/', include('user.urls')),
]

# 이미지 데이터는 media 파일에 저장되고 데이터베이스에는 주소값만 저장되는데 아래 셋팅을 해놓아야 media에서 이미지를 조회할 수 있다.
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
