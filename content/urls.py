from django.urls import path
from .views import UploadFeed, Profile, Main, UploadReply, ToggleLike, ToggleBookmark

urlpatterns = [
    path('upload', UploadFeed.as_view(), name='upload'),
    path('reply', UploadReply.as_view(), name='reply'),
    path('profile', Profile.as_view(), name='profile'),
    path('main', Main.as_view(), name='main'),
    path('like',ToggleLike.as_view(), name='like'),
    path('bookmark',ToggleBookmark.as_view(), name='bookmark'),
]



