from django.urls import path
from .views import (
	PostsList, PostDetail, SearchResults, PostCreate, PostUpdate, PostDelete, ResponseCreate, ResponseList,
	ResponseDelete
)


urlpatterns = [
	path('', PostsList.as_view(), name='posts'),
	path('<int:pk>', PostDetail.as_view(), name='post_detail'),
	path('search/', SearchResults.as_view(), name='search'),
	path('create/', PostCreate.as_view(), name='post_create'),
	path('<int:pk>/edit', PostUpdate.as_view(), name='post_edit'),
	path('<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
	path('<int:pk>/response', ResponseCreate.as_view(), name='add_response'),
	path('responses', ResponseList.as_view(), name='responses'),
	path('responses/<int:pk>/delete', ResponseDelete.as_view(), name='response_delete'),
]
