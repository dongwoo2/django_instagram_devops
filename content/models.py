from django.db import models

# Create your models here.
class Feed(models.Model):
    content = models.TextField() # 글 내용
    image = models.TextField() # 피드 이미지
    email = models.EmailField(default='') # 이메일(실제는 글쓴이) - 이메일로 사람을 판별하니까

class Like(models.Model):
    feed_id = models.IntegerField(default=0) # 내가 어떤 게시물에 좋아유 눌렀는지를 판별
    email = models.EmailField(default='')
    is_like = models.BooleanField(default=True)


class Reply(models.Model):
    feed_id = models.IntegerField(default=0)
    email = models.EmailField(default='')
    reply_content = models.TextField()


class Bookmark(models.Model):
    feed_id = models.IntegerField(default=0)
    email = models.EmailField(default='')
    is_marked = models.BooleanField(default=True) # 북마크