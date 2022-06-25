from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from .forms import SetForm, QuestionForm
from .models import Set, Question


def parse_data_from_post(post):
    data = {}
    for i in post.lists():
        key, value = i
        # print(key, value)
        if key == 'set_name' or key == 'set_description':
            data[key] = value[0]
        else:
            data[key] = value
            if key == 'name':
                data['no_questions'] = len(value)

    return data


def create_set_new(request):
    if request.method == "POST":
        for i in request.POST.lists():
            key, values = i
            if key == 'name':
                names = values
                no_questions = len(values)
            if key == 'def':
                definitions = values

        print(no_questions)
        set_name = request.POST.get('set_name')
        set_description = request.POST.get('set_description')

        new_set = Set.objects.create(user=request.user, name=set_name, description=set_description)
    
        print(set_name, set_description)

        for name, definition in zip(names, definitions):
            print(name, definition)
            if not name == definition == None or name == definition == "":
                Question.objects.create(question_set=new_set, name=name, definition=definition)
        return redirect('view_set', pk=new_set.id)

    return render(request, 'learningSets/create_set_try.html')


def edit_set_new(request, pk):
    q_set = Set.objects.get(id=pk)
    response = {
        'changed': False
    }

    if request.method == "POST":
        data = parse_data_from_post(request.POST)
        print(data)

        q_set.name = data["set_name"]
        q_set.description = data["set_description"]

        if q_set.tracker.changed():
            q_set.save()
            response["changed"] = True

        questions = q_set.question_set.all()

        for index, (name, definition) in enumerate(zip(data['name'], data['def'])):
            
            # print(name, definition)
            if not name == definition == None or name == definition == "":
                if index < questions.count():
                    question = questions[index]
                    question.name = name
                    question.definition = definition

                    if question.tracker.changed():
                        question.save()
                        response["changed"] = True

                else:
                    data = {
                        'name': name,
                        'definition': definition,
                        'question_set': q_set
                    }
                    question = QuestionForm(data)

                    if question.is_valid():
                        question = question.save()
                        response["changed"] = True
                    else:
                        break
                
                response[question.id] = index+1

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse(response)
        return redirect('edit_set', pk=q_set.id)

    return render(request, 'learningSets/edit_set_try.html', {'set': q_set})



@login_required(login_url='login')
def create_set(request):
    if request.method == "POST":
        get_question_indexes(request.POST)
        set_name = request.POST.get('set_name')
        set_description = request.POST.get('set_description')

        new_set = Set.objects.create(user=request.user, name=set_name, description=set_description)
        

        no_questions = int(request.POST.get('no_questions'))
        print(set_name, set_description)

        for i in range(1, no_questions + 1):
            q_name = request.POST.get(f'name-{i}')
            q_definition = request.POST.get(f'def-{i}')
            print(q_name, q_definition)
            if not q_name == q_definition == None or q_name == q_definition == "":
                Question.objects.create(question_set=new_set, name=q_name, definition=q_definition)
            print(q_name, q_definition)
        return redirect('view_set', pk=new_set.id)

    return render(request, 'learningSets/create_set.html')


def edit_set(request, pk):
    q_set = Set.objects.get(id=pk)
    response = {
        'changed': False
    }

    if request.method == "POST":
        set_name = request.POST.get('set_name')
        set_description = request.POST.get('set_description')

        q_set.name = set_name
        q_set.description = set_description

        if q_set.tracker.changed():
            q_set.save()
            response["changed"] = True

        no_questions = int(request.POST.get('no_questions'))
        questions = q_set.question_set.all()

        for i in range(no_questions):
            q_name = request.POST.get(f'name-{i+1}')
            q_definition = request.POST.get(f'def-{i+1}')
            
            # print(q_name, q_definition)
            if not q_name == q_definition == None or q_name == q_definition == "":
                if i < questions.count():
                    question = questions[i]
                    question.name = q_name
                    question.definition = q_definition

                    if question.tracker.changed():
                        question.save()
                        response["changed"] = True

                else:
                    data = {
                        'name': q_name,
                        'definition': q_definition,
                        'question_set': q_set
                    }
                    question = QuestionForm(data)

                    if question.is_valid():
                        question = question.save()
                        response["changed"] = True
                    else:
                        break
                
                response[question.id] = i+1

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse(response)
        return redirect('edit_set', pk=q_set.id)

    return render(request, 'learningSets/edit_set.html', {'set': q_set})


def delete_set(request, pk):
    q_set = Set.objects.get(id=pk)
    q_set.delete()
    return redirect('home')

    # if request.method == "POST":
    #     q_set.delete()
    #     return redirect('home')

    # return render(request, 'learningSets/delete.html', {'obj': q_set})


def delete_term(request, pk):
    term = Question.objects.get(id=pk)
    term.delete()
    return HttpResponse('Success')

    

def view_set(request, pk):
    q_set = Set.objects.get(id=pk)

    return render(request, 'learningSets/view_set.html', {'set': q_set})