from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Create your views here.
def register(resp):
    if resp.method == "POST":
        form = UserCreationForm(resp.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
        else:
            messages.error(resp, "Invalid password or username")
    else:
        form = UserCreationForm()
    return render(resp, "register/register.html", {"form": form})