from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate ,login, logout
from django.http import HttpResponseRedirect
from .forms import SudokuImageForm
from .solver.new import solve
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request,'index.html')

@login_required(login_url="/login")
def upload_sudoku(request):
    # if request.method == 'POST':
    #     form = SudokuImageForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         sudoku_image = form.save()
    #         solved_sudoku = main(sudoku_image.image.path)
    #         return render(request, 'solved.html', {'solved_sudoku': solved_sudoku})
    # else:
    #     form = SudokuImageForm()
    # return render(request, 'upload.html', {'form': form})
    if request.method == 'POST':
        sudoku = []
        for i in range(9):
            row = []
            for j in range(9):
                value = request.POST.get(f'cell-{i}-{j}')
                row.append(int(value) if value.isdigit() else 0)
            sudoku.append(row)

        if solve(sudoku):  # Solve the Sudoku
            solved_sudoku = sudoku
        else:
            solved_sudoku = None  # In case the puzzle is not solvable
        
        return render(request, 'solved.html', {'solved_sudoku': solved_sudoku})
    return render(request, 'upload.html')

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username = username).exists():
            messages.info(request, "Invalid Username")
            return redirect('/login')
        
        user = authenticate(username = username, password = password)

        if user is None:    
            messages.info(request, "Invalid Password")
            return redirect('/login')
        
        else:
            login(request,user)        
            return redirect('/upload')
        
    return render(request, 'login.html')

def register(request):

    if request.method != "POST":
        return render(request, 'register.html')

    first_name = request.POST.get('firstname')
    last_name = request.POST.get('lastname')
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')

    user = User.objects.filter(username=username)


    if user.exists():
        messages.info(request, "Username Already Exists")
        return redirect('/register')

    elif User.objects.filter(email=email).exists():
        messages.info(request, "Email Already Taken")
        return redirect('/register')

    user = User.objects.create(
        first_name= first_name, 
        last_name= last_name,
        username=username,
        email=email,
        )

    user.set_password(password)    # this method is already thier in django
    user.save()
    messages.info(request, "Account created successfully")

    return redirect('/login')

def logout_page(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))

