from django.shortcuts import render, redirect
from .models import Todo
from datetime import datetime
# Create your views here.
def home(request):
    todos = Todo.objects.all()
    sorted_todo = []
    done_todo = []
    now = datetime.now()
    for todo in todos:
        if todo.done != True:
            todo.d_day = todo.deadline.date() - now.date()
            if todo.d_day.days < 0:
                todo.outdated = True
            else:
                todo.outdated = False
            todo.d_day = todo.d_day.days
            sorted_todo.append(todo)
        else:
            done_todo.append(todo)
        sorted_todo.sort(key=lambda x: x.d_day)
    return render(request, 'home.html', {'todos': sorted_todo, 'done_todo': done_todo})

def new(request):
    if request.method == 'POST':
        deadline = request.POST['deadline']
        # '2023-04-04T12:34' => 2023-04-04 12:34:00
        parsed_deadline = datetime.fromisoformat(deadline)
        
        new_todo = Todo.objects.create(
            title = request.POST['title'],
            content = request.POST['content'],
            deadline = parsed_deadline,
        )
        return redirect('home')

    return render(request, 'new.html')

def detail(request, todo_id):
    todo = Todo.objects.get(id = todo_id)
    return render(request, 'detail.html', {'todo': todo})

def update(request,	todo_id):
    todo = Todo.objects.get(pk=todo_id)
    todo_deadline = datetime.isoformat(todo.deadline)

    if request.method == 'POST':
        deadline = request.POST['deadline']
        
        Todo.objects.filter(pk=todo_id).update(
            title = request.POST['title'],
            content = request.POST['content'],
            deadline = datetime.fromisoformat(deadline),
        )
        return redirect('detail', todo_id)
    
    return render(request, 'update.html', {'todo': todo, 'todo_deadline': todo_deadline })

def delete(request, todo_id):
    todo = Todo.objects.get(pk=todo_id)
    todo.delete()
    return redirect('home')

def done(request, todo_id):
    Todo.objects.filter(pk=todo_id).update(
        done = True,
    )
    return redirect('home')