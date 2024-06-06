from uuid import uuid4

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Feed, Reply, Like, Bookmark
from user.models import User
import os
from Dongstagram.settings import MEDIA_ROOT

# Create your views here.
class Main(APIView):
    def get(self, request):
        email = request.session.get('email', None)

        if email is None:  # 로그인을 안한 상태로 접속했을 때
            return render(request, "user/login.html")

        user = User.objects.filter(email=email).first()

        if user is None:  # 이메일 주소는 있는데 우리 회원이 아닐 때
            return render(request, "user/login.html")  # 그러면 로그인 다시해
        feed_object_list = Feed.objects.all().order_by('-id')
        feed_list = []

        for feed in feed_object_list:
            user = User.objects.filter(email=feed.email).first()
            reply_object_list = Reply.objects.filter(feed_id=feed.id) # 그 피드 하나에 적힌 댓글 목록을 불러올 수 있다.
            reply_list = []
            for reply in reply_object_list:
                user = User.objects.filter(email=reply.email).first()
                reply_list.append(dict(
                    reply_content=reply.reply_content,
                    nickname=user.nickname,
                ))
            like_count = Like.objects.filter(feed_id=feed.id, is_like=True).count()
            is_liked = Like.objects.filter(feed_id=feed.id, email=email, is_like=True).exists() # 나 아직 왜 feed_id가 필요한지 모르겠음
            is_marked = Bookmark.objects.filter(feed_id=feed.id, email=email, is_marked=True).exists()
            feed_list.append(dict(
                                  id=feed.id,
                                  image=feed.image,
                                  content=feed.content,
                                  like_count=like_count,
                                  profile_image=user.profile_image,
                                  nickname=user.nickname, # 실시간 데이터 반영
                                  reply_list=reply_list,
                                  is_liked=is_liked,
                                  is_marked=is_marked, # main으로 데이터를 보내는거니까 템플릿에서 is_marked를 쓸려면  이 데이터가 필요한 건 당연하다.
                                  ))

#        print('로그인한 사용자:', request.session['email'])


        return render(request,"Dongstagram/main.html",{"feed_list":feed_list, "user" : user})


class UploadFeed(APIView):
    def post(self, request):

        # 파일을 불러오는 거
        file = request.FILES['file']

        uuid_name = uuid4().hex # 이미지 파일의 경우 특수문자 한글 막 뒤죽박죽하게 섞여있다 그것을 영어와 숫자로만 적힌 고유id값으로 만들어준다
        save_path = os.path.join(MEDIA_ROOT, uuid_name)# 경로지정 경로를 join 미디어루트 경로에 uuid_name을 추가 즉 media/uuid_name 이렇게 지정을 하겠다는 뜻 미디어 폴더에 uuid_name으로 고유값이 만들어진 애까지 지정

        with open(save_path, 'wb+') as destination: # 실제로 파일을 저장하는 부분
            for chunk in file.chunks():
                destination.write(chunk)

        image = uuid_name
        content = request.data.get('content')
        email = request.session.get('email', None) # 세션이 있다는거는 로그인한 증거니까 세션에서 가져오고

        Feed.objects.create(image=image,content=content,email=email,)
        return Response(status=200)


class Profile(APIView):
    def get(self, request):
        email = request.session.get('email', None)

        if email is None: # 로그인을 안한 상태로 접속했을 때
            return render(request, "user/login.html")

        user = User.objects.filter(email=email).first()

        if user is None:# 이메일 주소는 있는데 우리 회원이 아닐 때
            return render(request, "user/login.html") # 그러면 로그인 다시해

        #내가 쓴 피드 리스트들을 보여주어야함
        feed_list = Feed.objects.filter(email=email)
        like_list = list(Like.objects.filter(email=email, is_like=True).values_list('feed_id', flat=True)) # feed_id 정보를 list로 받고 싶으면 flat을 True로 설정하면 된다. 내가 좋아요를 누른 피드리스트가 나온다
        print(like_list) # 쿼리셋으로 나오는데 list로 나오게 할려면 list()를 해야한다. 위에 줄 말하는거임 list()안하니까 쿼리셋으로 나옴
        like_feed_list = Feed.objects.filter(id__in=like_list) # 피드에 있는 id중에 좋아요 한 애만 걸림
        bookmark_list = list(Bookmark.objects.filter(email=email, is_marked=True).values_list('feed_id', flat=True))
        bookmark_feed_list = Feed.objects.filter(id__in=bookmark_list)
        return render(request, "content/profile.html", {"user":user, "feed_list":feed_list, "like_feed_list":like_feed_list, "bookmark_feed_list":bookmark_feed_list})


class UploadReply(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        reply_content = request.data.get('reply_content', None)
        email = request.session.get('email', None)

        Reply.objects.create(feed_id=feed_id,reply_content=reply_content, email=email)

        return Response(status=200)


class ToggleLike(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        favorite_text = request.data.get('favorite_text', True) # 안 올라오면 True

        if favorite_text == 'favorite_border': # jquery로 boolean이 안넘어감
            is_like = True
        else:
            is_like = False
        email = request.session.get('email', None)

        like = Like.objects.filter(feed_id=feed_id, email=email).first() # 이미 좋아요를 누른게 있는 지 판별

        if like:
            like.is_like = is_like
            like.save()
        else:
            Like.objects.create(feed_id=feed_id, is_like=is_like, email=email)


        return Response(status=200)


class ToggleBookmark(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        bookmark_text = request.data.get('bookmark_text', True)  # 안 올라오면 True

        if bookmark_text == 'bookmark_border':  # jquery로 boolean이 안넘어감
            is_marked = True
        else:
            is_marked = False
        email = request.session.get('email', None)

        bookmark = Bookmark.objects.filter(feed_id=feed_id, email=email).first()  # 이미 좋아요를 누른게 있는 지 판별

        if bookmark:
            bookmark.is_marked = is_marked
            bookmark.save()
        else:
            Bookmark.objects.create(feed_id=feed_id, is_marked=is_marked, email=email)

        return Response(status=200)