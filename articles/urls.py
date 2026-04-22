from django.urls import path
from articles.views import ArticleDetail, ArticleView, NotificationDetail, NotificationView ,   NotificationPostView ,ArticlePostView

urlpatterns = [
    path('', ArticleView.as_view()),
    path('<int:pk>/', ArticleDetail.as_view()),
    path('post/',ArticlePostView.as_view()),

    path('notifications/', NotificationView.as_view()),
    path('notifications/<int:pk>/', NotificationDetail.as_view()),
    path('notifications/post/', NotificationPostView.as_view()),

]
