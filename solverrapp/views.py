import json
import re

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
    solutions = Solution.objects.filter(question=question)


    _solutions = []
    print(len(solutions))
    for solution in solutions:
        if solution.solution_type == 'VID' and solution.solution_media_url.startswith('https://vimeo.com'):
            video_id = solution.solution_media_url.split("/")[-1].split('?')[0]
            body = f"""
<div style="padding:56.25% 0 0 0;position:relative;">
    <iframe src="https://player.vimeo.com/video/{video_id}?badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479" frameborder="0" allow="autoplay; fullscreen; picture-in-picture; clipboard-write" style="position:absolute;top:0;left:0;width:100%;height:100%;border-radius:0.6rem;" title="11"></iframe></div><script src="https://player.vimeo.com/api/player.js"></script>
            """
        elif solution.solution_type == 'IMG':
            body = f"<img src='{ solution.solution_media_url }'>"
        else:
            body = solution.solution_body
        _solutions.append({
            'body': body,
            'solution_source':solution.solution_source
        })


    return render(request, "solverrapp/questions/question_detail.html", context={'question':question, 'options':options, 'solutions':_solutions})

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

    if len(_questions) > 4:
        _questions = _questions[:4]

    return JsonResponse({
        'payload':{'data':_questions}
    })


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
    