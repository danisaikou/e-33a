from decimal import Decimal

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import UpdateView

from .forms import (AddTaskForm, ExpenseForm, NewProject, TimeForm,
                    UpdateTaskForm)
from .models import Expense, Project, ProjectTask, TimeModel, User


def index(request):
    # Render the home page
    return render(request, 'track/index.html')


def project_list(request):
    # Render the projects page with the users projects
    return render(request, 'track/projects.html', {
            'projects': request.user.project_list.all(),
        })


def create_task(request):
    # Handle form submission to create a new task
    if request.method == 'POST':
        form = AddTaskForm(request.POST)
        # Check that the form is valid before proceeding
        if form.is_valid():
            # Get user info so it's stored with the listing
            proj = form.save(commit=False)
            proj.projects = request.user
            proj.project_manager = request.user

            # Save it and generate a blank form
            proj.save()
            form = AddTaskForm()

    # If it's not POST, give the user the form to fill out
    else:
        form = AddTaskForm()

    # To the listing page with the form
    return render(request, 'track/create_task.html', {
        'form': form
    })


def create_project(request):
    # Generate form from model forms for creating a listing
    if request.method == 'POST':
        form = NewProject(request.POST)

        # Check that the form is valid before proceeding
        if form.is_valid():

            # Get user info to store with project
            proj = form.save(commit=False)
            proj.projects = request.user
            proj.project_manager = request.user

            # Save and generate blank form
            proj.save()
            form = NewProject()

    # If it's not POST, give the user the form to fill out
    else:
        form = NewProject()

    # To the listing page with the form
    return render(request, 'track/create_project.html', {
        'form': form

    })


class edit_project(UpdateView):
    # Define model and specify template to render
    model = Project
    template_name = 'track/edit_project.html'
    fields = ['name', 'budget_hours', 'budget_dollars', ]

    def get_success_url(self):
        return reverse('projects')


def project(request, id):
    projects = Project.objects.filter(id=id)
    project = Project.objects.get(id=id)
    time_models = project.time_models.all()
    form = AddTaskForm(initial={'project': project})
    timeform = TimeForm(initial={'project': project})
    tasks = ProjectTask.objects.filter(project=project)
    expenseform = ExpenseForm(initial={'project': project})
    expenses = Expense.objects.filter(project=project)

    # Calc total expenses by summing all expenses
    total_expenses = sum([expense.amount for expense in expenses])

    if request.method == 'POST':

        # Form to add new tasks
        form = AddTaskForm(request.POST)

        # Confirm that the form is valid
        if form.is_valid():
            form.save()

            return redirect('project', id=id)
        else:
            form = AddTaskForm()

        # Form to add expenses to the project
        expenseform = ExpenseForm(request.POST)

        # Confirm form is valid
        if expenseform.is_valid():
            # create an expense object and save it to the db
            expense = Expense(
                amount=expenseform.cleaned_data['amount'],
                description=expenseform.cleaned_data['description'],
                date=expenseform.cleaned_data['date'],
                project_id=id,
            )
            expense.save()

            return redirect('project', id=id)
        else:
            expenseform = ExpenseForm()

            # get all expenses for the project
            expenses = Expense.objects.filter(project=project)

            # Calculate sum of all expenses for project
            total_expenses = sum([expense.amount for expense in expenses])

        # Form to add time to the project
        timeform = TimeForm(request.POST)

        # confirm form is valid and clean the inputs
        if timeform.is_valid():
            time_model = TimeModel(
                start_time=timeform.cleaned_data['start_time'],
                end_time=timeform.cleaned_data['end_time'],
                project_id=id,
            )
            time_model.save()

            return redirect('project', id=id)

        else:
            # Print errors when it doesn't work
            print(timeform.errors)
            timeform = TimeForm()
            # display error message

    tasks_todo = ProjectTask.objects.filter(project=project, status=ProjectTask.TODO)
    tasks_complete = ProjectTask.objects.filter(project=project, status=ProjectTask.COMPLETE)
    tasks_canceled = ProjectTask.objects.filter(project=project, status=ProjectTask.CANCELED)
    elapsed_time = project.get_elapsed_time()
    elapsed_time = Decimal(elapsed_time)
    project_total = elapsed_time * 200 + total_expenses

    return render(request, 'track/project.html', {
        'projects': projects,
        'id': id,
        'tasks_todo': tasks_todo,
        'tasks_complete': tasks_complete,
        'tasks_canceled': tasks_canceled,
        'form': form,
        'timeform': timeform,
        'project': project,
        'time_models': time_models,
        'elapsed_time': elapsed_time,
        'tasks': tasks,
        'expenseform': expenseform,
        'expenses': expenses,
        'total_expenses': total_expenses,
        'project_total': project_total,
    })


def toggle_project_status(request, id):
    project = Project.objects.get(id=id)
    project.toggle_status()
    return redirect('project', id=id)


def view_tasks(request):
    tasks = ProjectTask.objects.all()
    return render(request, 'track/tasks.html', {'tasks': tasks})


def view_task(request, pk):
    task = ProjectTask.objects.get(pk=pk)
    return render(request, 'tasks/task.html', {'task': task})


def update_task(request, pk):
    task = ProjectTask.objects.get(pk=pk)

    if request.method == 'POST':
        form = UpdateTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('projects')
    else:
        form = UpdateTaskForm(instance=task)

    return render(request, 'track/update_task.html', {'form': form})


def update_time(request):
    # get instance to update
    time_model = TimeModel.objects.get(id=1)

    # update start and end fields
    time_model.start_time = request.POST['start_time']
    time_model.end_time = request.POST['end_time']

    # save
    time_model.save()
    return HttpResponseRedirect(reverse('projects'))


def invoice(request, project_id):
    projects = Project.objects.filter(id=project_id)
    project = Project.objects.get(id=project_id)
    elapsed_time = project.get_elapsed_time()
    expenses = Expense.objects.filter(project=project)
    total_expenses = sum([expense.amount for expense in expenses])
    elapsed_time = Decimal(elapsed_time)
    project_total = elapsed_time * 200 + total_expenses
    tasks_complete = ProjectTask.objects.filter(project=project, status=ProjectTask.COMPLETE)

    return render(request, 'track/invoice.html', {
        'projects': projects,
        'elapsed_time': elapsed_time,
        'expenses': expenses,
        'total_expenses': total_expenses,
        'project_total': project_total,
        'tasks_complete': tasks_complete,
        })


def invoices_list(request):
    projects = Project.objects.all()

    return render(request, 'track/invoices_list.html', {
        'projects': projects,
        })


# Everything below this adapted from previous assignments
def login_view(request):
    if request.method == 'POST':

        # Attempt sign in
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'track/login.html', {
                'message': 'Invalid username and/or password.'
            })
    else:
        return render(request, 'track/login.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']

        # Ensure password matches confirmation
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        if password != confirmation:
            return render(request, 'track/register.html', {
                'message': 'Passwords must match.'
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, 'track/register.html', {
                'message': 'Username already taken.'
            })
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'track/register.html')
