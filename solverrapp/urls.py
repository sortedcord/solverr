from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("questions/", views.questions, name="questions"),
    path("questions/<str:question_id>/", views.question_detail, name="question_detail"),
    path('questions/<str:question_id>/solve', views.question_solve, name='question_solve'),
    path("new/", views.question_new, name="question_new"),

    # API
    path("api/new/question", views.api_question_submit, name="api_question_submit"),
]