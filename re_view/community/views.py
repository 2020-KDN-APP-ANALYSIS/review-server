import json
from datetime import datetime
from django.shortcuts import render
from .models import Post, Answer
from .serializers import PostSerializer, AnswerSerializer
from rest_framework import viewsets, generics, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.core.serializers.json import DjangoJSONEncoder
from .authentication import JSONTokenAuthentication
from rest_framework import status

# Create your views here.


class PostViewSet(viewsets.ModelViewSet):

    def create(self, request, *args, **kwargs):
        if JSONTokenAuthentication.authenticate(request):
            query_data = request.data

            pub_time = datetime.now().strftime('%Y%m%d%H%M%S')
            query_data["post_token"] = pub_time + \
                request.data["userid"]  # post_token: pub_time + userid

            serializer = PostSerializer(data=query_data)

            if not serializer.is_valid():
                return Response(serializer.errors)

            serializer.save()

            return Response(serializer.data)
        else:
            return Response("Action denied: Not logged in ", status=status.HTTP_401_UNAUTHORIZED)

    def list(self, request):

        queryset = Post.objects.all()
        order = self.request.query_params.get('order', None)

        if order == "popular":
            queryset = queryset.order_by("-view_count", "-publish_date")

        if order == "like":
            queryset = queryset.order_by("-like_count", "-publish_date")

        serializer = PostSerializer(queryset, many=True)

        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def view(self, request, pk=None):

        obj = Post.objects.get(post_token=pk)
        #obj = json.dumps(list(obj)[0], cls=DjangoJSONEncoder)

        obj.view_count += 1
        obj.save()

        return Response("update success", status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def like(self, request, pk=None):

        if JSONTokenAuthentication.authenticate(request):

            obj = Post.objects.get(post_token=pk)

            obj.like_count += 1
            obj.save()

            return Response("update success", status=status.HTTP_200_OK)
        else:
            return Response("Action denied: Not logged in ", status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, pk):
        try:
            answer_queryset = Answer.objects.get(post_token=pk)
            answer_queryset.delete()
            post_queryset = Post.objects.get(post_token=pk)
            post_queryset.delete()

        except Exception as err:
            raise "Error: {}".format(err)

        return Response("delete succuess")


class GetPostAPI(mixins.ListModelMixin, generics.GenericAPIView):

    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        
        queryset = Post.objects.filter(user=self.kwargs["user_id"])
        
        serializer = PostSerializer(queryset, many=True)

        return Response(serializer.data)


class AnswerViewSet(viewsets.ModelViewSet):

    @action(detail=True, methods=['get'])
    def show(self, request, pk=None):

        queryset = Answer.objects.filter(post_token=pk).all()
        serializer = AnswerSerializer(queryset, many=True)

        return Response(serializer.data)

    def create(self, request):

        if JSONTokenAuthentication.authenticate(request):
            query_data = request.data

            pub_time = datetime.now().strftime('%Y%m%d%H%M%S')

            # answer_token: pub_time + post_token + userid
            query_data["answer_token"] = pub_time + \
                request.data['post_token'] + request.data["userid"]

            serializer = AnswerSerializer(data=query_data)

            if not serializer.is_valid():
                return Response(serializer.errors)

            serializer.save()

            return Response(serializer.data)
        else:
            return Response("Action denied: Not logged in ", status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, pk):
        try:

            queryset = Answer.objects.get(answer_token=pk)
            queryset.delete()
        except Exception as err:
            raise "Error: {}".format(err)
        return Response("delete succuess")

    @action(detail=True, methods=['patch'])
    def like(self, request, pk=None):

        if JSONTokenAuthentication.authenticate(request):

            obj = Answer.objects.get(answer_token=pk)
            obj.like_count += 1
            obj.save()
            return Response("update success")
        else:
            return Response("Action denied: Not logged in ", status=status.HTTP_401_UNAUTHORIZED)
