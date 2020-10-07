from django.db import models

# Create your models here.
class Post(models.Model):
    post_token = models.CharField(("post_token"), max_length=50, primary_key=True)
    user= models.ForeignKey("account.Account", on_delete=models.CASCADE)
    title = models.CharField(("Post Title"), max_length=50)
    content = models.TextField(("Post Content"))
    publish_date = models.DateTimeField(("Post pusblied Date"),auto_now_add=True)
    view_count = models.IntegerField(("view count"), default=0)
    like_count = models.IntegerField(("like count"), default=0)
    image = models.CharField(("Sample image link"), max_length=150, blank=True)

    class Meta:
        ordering = ('publish_date',)

class Answer(models.Model):
    answer_token = models.CharField(("answer_token"), max_length=50, primary_key=True)
    post_token = models.ForeignKey("Post", on_delete=models.CASCADE)
    user = models.ForeignKey("account.Account", on_delete=models.CASCADE)
    content = models.TextField(("Answer content"))
    publish_date = models.DateTimeField(("Post pusblied Date"), auto_now_add=True)
    like_count = models.IntegerField(("like count"), default=0)

    class Meta:
        ordering = ('publish_date',)