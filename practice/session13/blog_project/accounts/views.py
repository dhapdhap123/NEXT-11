from django.shortcuts import render, redirect

# Create your views here.
from django.contrib import auth
from .models import Profile
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

class CreateUserForm(UserCreationForm):
    class Meta:
        model=Profile
        fields=['username',	'email', 'bio', 'password1', 'password2']

def signup(request):
    form = CreateUserForm
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:home')
        else:
            error = '입력정보가 valid하지 않습니다.'
            return render(request, 'accounts/signup.html', {'form': form, 'error': error})
    return render(request, 'accounts/signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user, backend ="django.contrib.auth.backends.ModelBackend")
            if 'next' in request.GET:
                return redirect(request.GET.get('next', '/'))
            else:
                return redirect('blog:home')
            
        else:
            error = '아이디 또는 비밀번호가 틀립니다'
            return render(request, 'accounts/login.html', {'error': error})
    return render(request, 'accounts/login.html')

def logout(request):
   auth.logout(request)
   return redirect('blog:home')