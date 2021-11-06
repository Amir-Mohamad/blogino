from random import randint
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, FormView
from django.contrib.auth import views
from django.contrib.auth import login, logout
from django.contrib.messages.views import SuccessMessageMixin as message
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from accounts.models import User
from accounts.forms import RegisterForm, ProfileForm, VerifyForm


# Dashboard (Profile). for changing some data.(name, lastname and ...)
class Profile(LoginRequiredMixin, message, UpdateView):
	model = User
	template_name = 'accounts/profile.html'
	form_class = ProfileForm
	success_url = reverse_lazy('core:home')
	success_message = 'پروفایل شما با موفقیت اپدیت شد'

	def get_object(self):
		return User.objects.get(pk=self.request.user.pk)

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		file = self.request.FILES.get('avatar')
		kwargs.update({'file': file})
		return kwargs


# Registering user
def UserRegister(request):
	form = RegisterForm(request.POST or None)
	if form.is_valid():
		global cd, code
		cd = form.cleaned_data
		code = randint(10100, 30100)
		subject = f'code: {code} for email: {cd["email"]}'
		send_mail(subject, 'code', settings.EMAIL_HOST_USER, (cd['email'],))
		return redirect('accounts:verify')
	return render(request, 'accounts/register.html', {'form':form})


# 2 step authentication with verify code
def VerifyCode(request):
	form = VerifyForm(request.POST or None)
	if form.is_valid():
		verifier = form.cleaned_data.get('verifier')
		if code == verifier:
			user = User.objects.create_user(email=cd['email'], password=cd['password1'])
			user.save()
			login(request, user)
			messages.success(request, 'You registerd successfully')
			return redirect('blog:home')
		else:
			messages.error(request, 'Your code is wrong')
			return redirect('accounts:verify')
	return render(request, 'accounts/verify.html', {'form':form})


# Login user
class UserLogin(message, views.LoginView):
	template_name = 'accounts/login.html'
	success_message = 'You successfully login'


# Logouting user
class UserLogout(views.LogoutView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "You successfully logout")
        return super().dispatch(request, *args, **kwargs)


# Changing password
class PasswordChange(message, views.PasswordChangeView):
	template_name = 'accounts/password_change_form.html'
	success_url = reverse_lazy('blog:home')
	success_message = 'Your password changed successfully'
