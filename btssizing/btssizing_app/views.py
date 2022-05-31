from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

# Vue index
def index(request): 
    return redirect('home/')

@login_required
def dashboard(request):
    return render(request, 'btssizing_app/index.html')

@login_required
def users(request):
    return redirect("btssizing_app:home") ; 
    # users = UserModel.objects.all()
    # return render(request, 'btssizing_app/users.html', {'users':users})