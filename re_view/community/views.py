from datetime import datetime
from django.shortcuts import render
from .models import Post, Answer
from .serializers import PostSerializer, AnswerSerializer
from rest_framework import viewsets, generics, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class PostViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    
    def create(self, request, *args, **kwargs):
        
        query_data = request.data
        
        pub_time = datetime.now().strftime('%Y%m%d%H%M%S')
        query_data["post_token"] = pub_time + request.data["userid"] #post_token: pub_time + userid
        
        serializer = PostSerializer(data=query_data)

        if not serializer.is_valid():
            return Response(serializer.errors)
        
        serializer.save()

        return Response(serializer.data)
            


    def list(self, request):
        
        queryset = Post.objects.all()
        order = self.request.query_params.get('order', None)

        if order == "popular":
            queryset = queryset.order_by("-view_count", "-pub_date")

        if order == "like":
            queryset = queryset.order_by("-like_count", "-pub_date")

        serializer = PostSerializer(queryset, many=True)

        return Response(serializer.data)
    


    def destroy(self, request, pk):
        pass


        
    @action(detail=True, methods=['patch'])
    def view(self, request):
        
        obj = Post.objects.filter(post_token=self.kwargs["pk"])

        data = {
            "post_token": obj["post_token"],
            "userid": obj["userid"],
            "title": obj["title"],
            "content": obj["content"],
            "pub_date": obj["pub_date"],
            "view_count": obj["view_count"] + 1,
            "like_count": obj["like_count"],
            "image": obj["image"]
        }
        serializer = PostSerializer(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors)

        serializer.save()

        return self.update(request, *args, **kwargs)


    @action(detail=True, methods=['patch'])
    def like(self, request):
        obj = Post.objects.filter(post_token=self.kwargs["pk"])

        data = {
            "post_token": obj["post_token"],
            "userid": obj["userid"],
            "title": obj["title"],
            "content": obj["content"],
            "pub_date": obj["pub_date"],
            "view_count": obj["view_count"],
            "like_count": obj["like_count"] + 1,
            "image": obj["image"]
        }
        serializer = PostSerializer(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors)

        serializer.save()

        return self.update(request, *args, **kwargs)


        def perform_destroy(self, instance):
            instance.delete()




class GetPostAPI(mixins.ListModelMixin, generics.GenericAPIView):

    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        
        queryset = Post.objects.all().filter(userid=self.kwargs["userid"])
        
        serializer = PostSerializer(data=queryset, many=True)
        
        return Response(serializer.data)



class AnswerViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    @action(detail=True)
    def show(self, request, pk):

        queryset = Answer.objects.all().filter(post_token=pk)

        serializer = AnswerSerializer(data=queryset, many=True)

        return Response(serializer.data)

    def create(self, request):
        
        query_data = request.data
        
        pub_time = datetime.now().strftime('%Y%m%d%H%M%S')

        #answer_token: pub_time + post_token + userid
        query_data["answer_token"] = pub_time + request.data['post_token'] + request.data["userid"] 
        
        serializer = AnswerSerializer(data=query_data)

        if not serializer.is_valid():
            return Response(serializer.errors)
        
        serializer.save()

        return Response(serializer.data)
        
    
    def destroy(self, request, pk):
        pass


    @action(detail=True, methods=['patch'])
    def like(self, request):
        obj = Answer.objects.filter(answer_token=self.kwargs["pk"])

        data = {
            "answer_token": obj["answer_token"],
            "post_token": obj["post_token"],
            "userid": obj["userid"],
            "content": obj["content"],
            "pub_date": obj["pub_date"],
            "like_count": obj["like_count"] + 1,
        }
        serializer = AnswerSerializer(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors)

        serializer.save()

        return self.update(request, *args, **kwargs)

        