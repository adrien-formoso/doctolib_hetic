from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

class LoginView(View):
    template_name = 'login.html'
    
    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  # Django utilise username pour le champ d'identification
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Rediriger vers la page d'accueil
            else:
                messages.error(request, 'Email ou mot de passe invalide.')
        return render(request, self.template_name, {'form': form})
