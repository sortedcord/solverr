from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Question, Source

def index(request):
    return render(request, "solverrapp/index.html")

def questions(request):
    questions = Question.objects.all()
    return render(request, "solverrapp/questions.html", context={'questions':questions})

def question_detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    return render(request, "solverrapp/question_detail.html", context={'question':question})

def new_question(request):
    question_types = Question.QUESTION_TYPES.values()
    sources = Source.objects.all()
    return render(request, "solverrapp/question_new.html", context={'question_types':question_types, 'sources':sources})

# API
def api_submit_question(request):
    
    pass