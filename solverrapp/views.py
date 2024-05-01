import json
import re

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Question, Solution, Source
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

from .utils import sanitize_question

from .scrape import search_connectors


def index(request):
    return render(request, "solverrapp/index.html")

def questions(request):
    questions = Question.objects.all()
    return render(request, "solverrapp/questions/questions.html", context={'questions':questions})


def question_detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    options = eval(question.question_options)
    solutions = Solution.objects.filter(question=question)
    print(sanitize_question(question.display_text))

    return render(request, "solverrapp/questions/question_detail.html", context={'question':question, 'options':options, 'solutions':solutions})

def question_new(request):
    question_types = Question.QUESTION_TYPES.items()
    sources = Source.objects.all()
    source_types = Source.SOURCE_TYPES
    return render(request, "solverrapp/questions/question_new.html", context={'question_types':question_types, 'sources':sources,
                                                                              'source_types':source_types})

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
def api_question_search(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)
    query = re.sub('%20','', request.GET.get('q').lower())
    _questions = []
    q_objs = Question.objects.all()

    s_query = re.sub(r'[ ,_^:{}()\[\]/]', '', query)


    for question in q_objs:
        contains = False
        if (question.search_text is not None) and (s_query in question.search_text):
            contains = True

        if (query in question.display_text):
            contains = True

        if not contains:
            continue

        _questions.append({
            'text': question.display_text,
            'image': question.display_image,
            'index': question.id,
        })

    # search_connectors(query)
    if len(_questions) > 4:
        _questions = _questions[:4]

    return JsonResponse({
        'payload':{'data':_questions}
    })


def api_sources_list(request):
    sources = Source.objects.all()

    sources_dict = []
    for source in sources:
        sources_dict.append({
            'name': source.name,
            'type': source.source_type
        })

    return JsonResponse({'data':sources_dict}, status=200)


@csrf_exempt
def api_new_source(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

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

    source_dict = post_data_dict

    new_source = Source(name=source_dict['name'], source_type=source_dict['type'])
    new_source.save()

    return JsonResponse({'payload': post_data_dict})


@csrf_exempt
def api_solution_submit(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

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

    question = Question.objects.get(id=post_data_dict['question_id'])

    if -1 in post_data_dict['sel_answers']:
        answer = post_data_dict['answer']
    else:
        # CONTINUE THIS
        answer = ""
        for option in eval(question.question_options):
            if option['option_index'] in post_data_dict['sel_answers']:
                answer += f' ({option["option_index"]+1}) {option["option_body"]} '

    new_soln = Solution(
        solution_type=post_data_dict['type'],
        answer=answer,
        solution_body='$PROCESS'+post_data_dict['body'],
        question=question,
        solution_source=post_data_dict['source']
    )
    new_soln.save()
    return JsonResponse({'payload': post_data_dict})


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

        if qmodobj.question_type not in ('MCQ', 'SCQ'):
            qmodobj.question_options = post_data_dict['answer']

        qmodobj.save()
        sources = post_data_dict['sources']
        for source_str in sources:
            source = Source.objects.get(name=source_str)
            source.question_set.add(qmodobj)
        qmodobj.save()

        return JsonResponse({'payload': post_data_dict, 'index': qmodobj.id})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    