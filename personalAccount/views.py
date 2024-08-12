from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

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

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)


class SignIn(LoginView):
    form_class = LoginForm
    template_name = 'personalAccount/login.html'


class SignOut(LogoutView):
    next_page = reverse_lazy('personalAccount:signin')


class Profile(TemplateView):
    template_name = 'personalAccount/profile.html'
