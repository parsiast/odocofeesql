from django.urls import path
from .views import CategoryView ,CategoryGets , ItemView , ItemGets

urlpatterns = [
    path('Category/<int:pk>',CategoryView.as_view(),name='category'),
    path('Category/',CategoryView.as_view(),name='category'),

    path('Item/<int:pk>',ItemView.as_view(),name='item'),
    path('Item/',ItemView.as_view(),name='item'),

    path('getcategory/<int:pk>',CategoryGets.as_view(),name='getcategory'),
    path('getcategory/',CategoryGets.as_view(),name='getcategory'),

    path('getitem/<int:pk>',ItemGets.as_view(),name='getitem'),
    path('getitem/',ItemGets.as_view(),name='getitem'),

]
