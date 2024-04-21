import json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Question, Solution, Source
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, "solverrapp/index.html")

def questions(request):
    questions = Question.objects.all()
    return render(request, "solverrapp/questions/questions.html", context={'questions':questions})

def question_detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    options = eval(question.question_options)
    return render(request, "solverrapp/questions/question_detail.html", context={'question':question, 'options':options})

def question_new(request):
    question_types = Question.QUESTION_TYPES.items()
    sources = Source.objects.all()
    return render(request, "solverrapp/questions/question_new.html", context={'question_types':question_types, 'sources':sources})

def question_solve(request, question_id):
    solution_types = Solution.SOLUTION_TYPES.items()
    question = get_object_or_404(Question, pk=question_id)
    options = eval(question.question_options)

    context = {
        'question': question,
        'solution_types': solution_types,
        'options': options
    }
    return render(request, "solverrapp/questions/question_solve.html", context = context)


# API
@csrf_exempt
def api_question_submit(request):
    if request.method == 'POST':
        # Check Content-Type header to determine how to parse the data
        content_type = request.headers.get('Content-Type', '')
        if 'application/json' in content_type:
            try:
                # Parse JSON data
                post_data_dict = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        elif 'multipart/form-data' in content_type:
            # Parse form data
            post_data_dict = request.POST.dict()
        else:
            return JsonResponse({'error': 'Unsupported Content-Type'}, status=415)
        
        qmodobj = Question(
            question_body=post_data_dict['body'],
            question_type=post_data_dict['type'],
            question_options=str(post_data_dict['options']),
        )
        qmodobj.save()
        sources = post_data_dict['sources']
        for source_str in sources:
            source = Source.objects.get(name=source_str)
            source.question_set.add(qmodobj)
        qmodobj.save()

        return JsonResponse({'payload': post_data_dict, 'index': qmodobj.id})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    