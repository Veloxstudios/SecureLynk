from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm 
from django.contrib.auth.decorators import login_required
from .forms import ContactForm, ProfileForm
from .models import Contact
import socket
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

def home(request):
    return render(request, 'Index.html')

def services(request):
    return render(request, 'services.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required(login_url='/login/')
def dashboard(request):
    contacts = Contact.objects.all().order_by('-created_at')
    return render(request, 'dashboard.html', {'contacts': contacts})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'contact.html', {
                'form': ContactForm(),
                'success': True
            })
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

@login_required(login_url='/login/')
def tools(request):
    return render(request, 'tools.html')

@require_POST
def port_scan(request):
    data = json.loads(request.body)
    host = data.get('host', '').strip()
    results = []

    common_ports = {
        21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP',
        53: 'DNS', 80: 'HTTP', 110: 'POP3', 143: 'IMAP',
        443: 'HTTPS', 3306: 'MySQL', 3389: 'RDP', 5432: 'PostgreSQL',
        6379: 'Redis', 8080: 'HTTP-Alt', 8443: 'HTTPS-Alt', 27017: 'MongoDB'
    }

    try:
        ip = socket.gethostbyname(host)
        for port, service in common_ports.items():
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((ip, port))
            sock.close()
            results.append({
                'port': port,
                'service': service,
                'open': result == 0
            })
        return JsonResponse({'success': True, 'ip': ip, 'results': results})
    except socket.gaierror:
        return JsonResponse({'success': False, 'error': 'Could not resolve host.'})

@login_required(login_url='/login/')
def profile(request):
    profile_form = ProfileForm(instance=request.user)
    password_form = PasswordChangeForm(user=request.user)
    profile_success = False
    password_success = False

    if request.method == 'POST':

        if 'update_profile' in request.POST:
            profile_form = ProfileForm(request.POST, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                profile_success = True

        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)
                password_success = True

    return render(request, 'profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
        'profile_success': profile_success,
        'password_success': password_success,
    })