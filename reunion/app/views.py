from requests import delete
import requests
from rest_framework import viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.serializers import *


class CreateUser(APIView):

    permission_classes = []

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200,data={"code": 100, "result": [{"success": 'Data Created'}]})
        return Response({"code": 101, "result": [{"error": serializer.errors}]})


class ProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profiles = Profile.objects.get(id=request.user.id)
            serializer = ProfileSerializer(profiles)
            return Response(status=200,data={"code": 100, "result": [serializer.data]})
        except Exception as e:
            return Response({"code": 101, "result": [{"error": "Error Fetching Profile"}]})

class PostsView(viewsets.ModelViewSet):
    
    permission_classes = [IsAuthenticated]
    serializer_class = PostsSerializer
    queryset = Post.objects.all()
    
    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.queryset.filter(profile_id=self.request.user.id).order_by('-pk'), many=True)
        return Response(status=200,data={"code":100,"result":[serializer.data]})
    
    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        instance = self.queryset.filter(pk=pk,profile_id=self.request.user.id).first()
        if instance:
            serializer = self.get_serializer(instance)
            return Response(status=200,data={"code":100,"result":[serializer.data]})
        else:
            return Response(status=400,data={"code":101,"result":[{"error":"No Post Found with the given id"}]})
    
    def create(self,request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer) 
            return Response(status=200,data={"code":100,"result":[serializer.data]})
        else:
            return Response(status=400,data={"code":101,"result":[serializer.errors]})

    def destroy(self,request,*args, **kwargs):
        pk = kwargs.get('pk')
        instance = self.queryset.filter(pk=pk,profile_id=self.request.user.id).first()
        if instance:
            self.perform_destroy(instance)
            return Response(status=200,data={"code":100,"result":[{"Success":"Post Deleted Successfully"}]})
        else:
            return Response(status=400,data={"code":101,"result":[{"error":"No Post Found with the given id"}]})
            
class LikesView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self,request,*args, **kwargs):
        pk = kwargs.get('pk')
        instance = self.queryset.filter(pk=pk).first()
        if instance:
            like_list = instance.likes
            if like_list is None:
                instance.likes = [request.user.id]
                instance.save()
                return Response(status=200,data={"code":100,"result":[{"Success":"Post Liked Successfully"}]})
            elif request.user.id in like_list:
                return Response(status=200,data={"code":100,"result":[{"Success":"Post Already Liked"}]})
            else:
                instance.likes.append(request.user.id)
                instance.save()
                return Response(status=200,data={"code":100,"result":[{"Success":"Post Liked Successfully"}]})
            
        return Response(status=400,data={"code":101,"result":[{"error":"No Post Found with the given id"}]})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unlike(self,request,*args, **kwargs):
        pk = kwargs.get('pk')
        instance = self.queryset.filter(pk=pk).first()
        if instance:
            like_list = instance.likes
            if like_list is None:
                return Response(status=200,data={"code":100,"result":[{"Success":"Post Not Liked"}]})
            
            elif request.user.id in like_list:
                instance.likes.remove(request.user.id)
                instance.save()
                return Response(status=200,data={"code":100,"result":[{"Success":"Post UnLiked Successfully"}]})
            
            else:
                return Response(status=200,data={"code":100,"result":[{"Success":"Post Not Liked"}]})
            
        return Response(status=400,data={"code":101,"result":[{"error":"No Post Found with the given id"}]})

class CommentsView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    
    def update(self,request,*args,**kwargs):
        instance = self.get_object()
        if len(request.data['comment'])<200:
            if instance.comment is None:
                instance.comment = [request.data['comment']]
                instance.save()
            else:
                instance.comment.append(request.data['comment'])
                instance.save()
            return Response(status=200,data={"code":100,"result":[{"comment_id":len(instance.comment)}]})
        else:
            return Response(status=400,data={"code":101,"result":[{"error":"Comment More than 200 characters"}]})

class FollowersView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def follow(self,request,*args, **kwargs):
        pk = kwargs.get('pk')
        instance = self.queryset.filter(pk=pk).first()
        self_instance = request.user
        if instance:
            following_list = self_instance.following
            if following_list is None:
                self_instance.following = [pk]
                self_instance.save()
                self.save_followers(request, instance)
                return Response(status=200,data={"code":100,"result":[{"Success":"Followed Successfully"}]})
            elif pk in following_list:
                return Response(status=200,data={"code":100,"result":[{"Success":"Already Followed"}]})
            else:
                self_instance.following.append(pk)
                self_instance.save()
                self.save_followers(request, instance)
                return Response(status=200,data={"code":100,"result":[{"Success":"Followed Successfully"}]})
            
        return Response(status=400,data={"code":101,"result":[{"error":"No Profile Found with the given id"}]})

    def save_followers(self, request, instance):
        if instance.followers is None:
            instance.followers = [request.user.id]
            instance.save()
        else:
            instance.followers.append(request.user.id)
            instance.save()
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unfollow(self,request,*args, **kwargs):
        pk = int(kwargs.get('pk'))
        instance = self.queryset.filter(pk=pk).first()
        self_instance = request.user
        if instance:
            following_list = self_instance.following
            if following_list is None:
                return Response(status=200,data={"code":100,"result":[{"Success":"Not Following"}]})
            elif pk in following_list:
                self_instance.following.remove(pk)
                self_instance.save()
                instance.followers.remove(request.user.id)
                instance.save()
                return Response(status=200,data={"code":100,"result":[{"Success":"UnFollowed"}]})
            else:
                return Response(status=400,data={"code":101,"result":[{"Success":"Not Following"}]})
            
        return Response(status=400,data={"code":101,"result":[{"error":"No Profile Found with the given id"}]})
    