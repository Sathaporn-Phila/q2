from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.display, name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/result/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('<int:question_id>/result/sortResult/', views.sortResult, name='sortResult'),
    path('sortQuestion/', views.sortQuestion, name='sortQuestion'),
]