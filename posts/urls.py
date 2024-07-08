from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewset, CommentViewSet, LikeViewSet

router = DefaultRouter()
router.register(r'posts', PostViewset, basename='post')
router.register(r'posts/(?P<post_pk>\d+)/comments', CommentViewSet, basename='comment')
router.register(r'posts/(?P<post_pk>\d+)/likes', LikeViewSet, basename='like')



urlpatterns = [
    path('', include(router.urls)),
]