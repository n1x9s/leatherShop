from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import SignUpForm, LoginForm


# def signup(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             user.refresh_from_db()
#             user.save()
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=user.username, password=raw_password)
#             login(request, user)
#             return redirect('shop:index')
#     else:
#         form = SignUpForm()
#     return render(request, 'personalAccount/register.html', {'form': form})
#

class SignUp(CreateView):
    form_class = SignUpForm
    template_name = 'personalAccount/register.html'
    success_url = reverse_lazy('shop:index')


class SignIn(LoginView):
    form_class = LoginForm
    template_name = 'personalAccount/login.html'


def signout(request):
    logout(request)
    return redirect('personalAccount:signin')
