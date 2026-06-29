from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout 
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'dashboard.html')
    else:
        return redirect('ulogin')
    

def usignup(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    elif request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password == confirm_password:

            try:
                User.objects.get(username=username)
                return render(request, "usignup.html", {"msg": "Username already exists"})

            except User.DoesNotExist:

                if User.objects.filter(email=email).exists():
                    return render(request, "usignup.html", {"msg": "Email already exists"})

                try:
                    validate_password(password)
                except ValidationError as e:
                    return render(request, "usignup.html", {"msg": e.messages})

                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )

                user.save()

                return redirect("ulogin")

        else:
            return render(request, "usignup.html", {"msg": "Passwords do not match"})

    else:
        return render(request, "usignup.html")

def ulogin(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "ulogin.html", {"msg": "Invalid credentials"})
    else:
        return render(request, "ulogin.html")
    
def ulogout(request):
    logout(request)
    return redirect("ulogin")

def change_password(request):
    if not request.user.is_authenticated:
        return redirect("ulogin")
    elif request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_new_password = request.POST.get("confirm_new_password")
        if new_password == confirm_new_password:
            user = User.objects.get(username=request.user.username)
            user.set_password(new_password)
            user.save()
            return redirect("ulogin")
        else:
            return render(request, "change_password.html", {"msg": "Passwords do not match"})
    else:   
        return render(request, "change_password.html")
