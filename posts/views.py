from django.shortcuts import render
from rest_framework import generics,permissions,mixins,status
from rest_framework.exceptions import ValidationError
from .models import Post,Vote
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import PostSerializer,VoteSerializer


class PostList (generics.ListCreateAPIView):
    queryset = Post.objects.all();
    serializer_class = PostSerializer
    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(poster=self.request.user)

class PostRetrieveDestroy (generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all();
    serializer_class = PostSerializer
    
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, *args, **kwargs):
        Post.objects.filter(pk=kwargs['pk'],poster=self.request.user)
        if post.exists():
            return self.destroy(request,*args,**kwargs)
        else :
            raise ValidationError('This is not your post to delete ,  Hey!!')

class VoteCreate (generics.CreateAPIView,mixins.DestroyModelMixin):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk'])
        return Vote.objects.filter(voter=user, post=post)

    
    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError('You have already voted !!!')
        
        serializer.save(voter=self.request.user,post=Post.objects.get(pk=self.kwargs['pk']))
        

    def delete(self, request, *args, **kwargs):
        queryset = self.get_queryset()  # call the method!
        if queryset.exists():
            queryset.delete()            # delete the queryset
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('You have never voted Silly ..!!!')
