from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("questions/", views.questions, name="questions"),
    path("questions/<str:question_id>/", views.question_detail, name="question_detail"),
    path("new/", views.new_question, name="new_question"),


    # API
    path("api/new/question", views.api_submit_question, name="api_submit_question"),
]