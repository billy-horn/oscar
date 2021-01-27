from django.urls import path
from .views import (
	PostListView,
	PostDetailView,
	PostCreateView,
	PostUpdateView,
	PostDeleteView,
	UserPostListView,
	ClassifyCreateView,
	ClassifyDetailView,
)
from . import views

urlpatterns = [
	path('', PostListView.as_view(), name='blog-home'), # Leaving empty string bc it's a home page
	path('user/<str:username>', UserPostListView.as_view(), name='user-posts'), # Leaving empty string bc it's a home page
	path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
	path('post/new/', PostCreateView.as_view(), name='post-create'),
	path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
	path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
	path('about/', views.about, name='blog-about'),
	path('classify/create', ClassifyCreateView.as_view(), name='classify-create'),
	path('classify/<int:pk>/', ClassifyDetailView.as_view(), name='classify-detail'),
]

