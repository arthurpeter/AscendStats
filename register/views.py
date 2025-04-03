from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_backends
from .forms import RegisterForm, LoginForm
from allauth.account.utils import send_email_confirmation
from allauth.account.views import ConfirmEmailView
from allauth.account.models import EmailConfirmationHMAC

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.save(commit=False)
            user.is_active = False  # Deactivate the account until email is confirmed
            user.save()

            # Send email confirmation
            send_email_confirmation(request, user)

            # Redirect to a confirmation sent page
            return redirect('email_confirmation_sent')
    else:
        form = RegisterForm()
    return render(request, 'register/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data.get('username_or_email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username_or_email, password=password)
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
                else:
                    return render(request, 'register/login.html', {
                        'form': form,
                        'error': 'Your email is not verified. Please check your inbox.'
                    })
            else:
                return render(request, 'register/login.html', {
                    'form': form,
                    'error': 'Invalid username or password.'
                })
    else:
        form = LoginForm()
    return render(request, 'register/login.html', {'form': form})


class CustomConfirmEmailView(ConfirmEmailView):
    def post(self, *args, **kwargs):
        response = super().post(*args, **kwargs)
        self.user.is_active = True
        self.user.save()
        return response

    def get(self, *args, **kwargs):
        confirmation = EmailConfirmationHMAC.from_key(kwargs['key'])
        if confirmation:
            user = confirmation.email_address.user
            user.is_active = True
            user.save()
            confirmation.confirm(self.request)
            login(self.request, user, backend='register.backends.EmailOrUsernameBackend')
            return render(self.request, 'account/email_confirmed.html')  # Render the confirmation page

        else:
            return redirect('/invalid-confirmation/')

