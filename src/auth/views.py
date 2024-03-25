from django.contrib import messages
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from auth import services
from auth.errors import InvalidCredentials
from auth.forms import RegistrationForm, LoginForm
from users.services import user_create
from users.selectors import user_get


def register(request):
    if request.user.is_authenticated:
        return redirect(reverse('users:me'))
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        user = user_create(
            email=form.cleaned_data['email'],
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
        )
        messages.info(request, 'Account successfully created.')
        request.session['username'] = user.username
        return redirect('auth:two_factor')
    return render(request, 'auth/register.html', {'form': form})


def login(request):
    if request.user.is_authenticated:
        return redirect(reverse('users:me'))
    form = LoginForm(request.POST or None)
    if form.is_valid():
        try:
            user = services.login(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                token=form.cleaned_data['token'],
            )
        except InvalidCredentials as e:
            messages.error(request, str(e))
            return redirect('auth:login')
        django_login(request, user)
        next = request.GET.get('next', None)
        return redirect(next or reverse('users:me'))
    return render(request, 'auth/login.html', {'form': form})


@login_required
def logout(request):
    django_logout(request)
    return redirect(reverse('auth:login'))


def two_factor(request):
    if request.user.is_authenticated:
        return redirect(reverse('users:me'))
    if 'username' not in request.session:
        return redirect(reverse('auth:login'))
    user = user_get(username=request.session['username'])
    if user is None:
        return redirect(reverse('auth:login'))

    response = render(request, 'auth/two-factor-setup.html')
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


def qrcode(request):
    if 'username' not in request.session:
        raise Http404 
    user = user_get(username=request.session['username'])
    if user is None:
        raise Http404

    del request.session['username']

    qr = services.qrcode_create(user)

    response = HttpResponse(qr.getvalue(), content_type='image/svg+xml')
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response
