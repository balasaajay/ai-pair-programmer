import os
from django.shortcuts import render, redirect
from django.contrib import messages
import openai
openai.api_key = os.environ.get('OPENAI_API_KEY')

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm

from .models  import Code

# Create your views here.
def home(request):

    languages_list = ['awk', 'bash', 'batch', 'c', 'clike', 'cmake', 'cpp', 'csharp', \
                      'css', 'css-extras', 'csv', 'diff', 'django', 'docker', 'git', 'go', \
                      'graphql', 'groovy', 'http', 'java', 'javascript', 'llvm', 'makefile', \
                      'markdown', 'markup', 'markup-templating', 'mongodb', 'nginx', 'powershell',\
                      'python', 'rust', 'sql', 'typescript', 'typoscript', 'verilog', 'vhdl', 'wasm', \
                      'yaml', 'zig']
    
    if request.method == 'POST':
        input_code = request.POST.get('input_code')
        lang = request.POST.get('lang')

        # Check to make sure language is picked.
        if lang == 'Select programming language':
            messages.success(request, 'Please select a programming language.')
            return render(request, 'home.html', {'input_code': input_code, 'response': input_code, 'languages_list': languages_list})
        else:
            # OPENAI
            
            prompt = f"Respond only with code. Do not repeat any part of the code. Fix this {lang} code: {input_code}"

            # Send a request
            try:
                response = openai.completions.create(
                    model="gpt-3.5-turbo-instruct",  # Specify the model
                    prompt=prompt,
                    max_tokens=1000,  # Adjust maximum token length as needed
                    temperature=0.2,  # Optional: Adjust creativity
                )
                response = response.choices[0].text.strip()
                # Save to DB
                record = Code(question=input_code, code_answer=response, language=lang, user=request.user)
                record.save()
                return render(request, 'home.html', {'languages_list': languages_list, 'response': response, 'lang': lang})
            except Exception as e:
                return render(request, 'home.html', {'languages_list': languages_list, 'response': e, 'lang': lang})
    return render(request, 'home.html', {'languages_list': languages_list})

def suggest(request):
    languages_list = ['awk', 'bash', 'batch', 'c', 'clike', 'cmake', 'cpp', 'csharp', \
                      'css', 'css-extras', 'csv', 'diff', 'django', 'docker', 'git', 'go', \
                      'graphql', 'groovy', 'http', 'java', 'javascript', 'llvm', 'makefile', \
                      'markdown', 'markup', 'markup-templating', 'mongodb', 'nginx', 'powershell',\
                      'python', 'rust', 'sql', 'typescript', 'typoscript', 'verilog', 'vhdl', 'wasm', \
                      'yaml', 'zig']
    
    if request.method == 'POST':
        input_code = request.POST.get('input_code')
        lang = request.POST.get('lang')

        # Check to make sure language is picked.
        if lang == 'Select programming language':
            messages.success(request, 'Please select a programming language.')
            print("Please select a programming language.")
            return render(request, 'suggest.html', {'input_code': input_code, 'response': input_code, 'languages_list': languages_list})
        else:
            # OPENAI
            prompt = f"Respond only with code. {input_code} in {lang}"
            # Send a request
            try:
                response = openai.completions.create(
                    model="gpt-3.5-turbo-instruct",  # Specify the model
                    prompt=prompt,
                    max_tokens=1000,  # Adjust maximum token length as needed
                    temperature=0.2,  # Optional: Adjust creativity
                )
                response = response.choices[0].text.strip()
                # Save to DB
                record = Code(question=input_code, code_answer=response, language=lang, user=request.user)
                record.save()
                return render(request, 'suggest.html', {'languages_list': languages_list, 'response': response, 'lang': lang})
            except Exception as e:
                return render(request, 'suggest.html', {'languages_list': languages_list, 'response': e, 'lang': lang})
    return render(request, 'suggest.html', {'languages_list': languages_list})

def login_user_fn(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password. Try again!")
            return redirect('home')
    else:
        return render(request, 'home.html', {})

def logout_user_fn(request):
    logout(request)
    messages.success(request, "You have been logged out!")
    return redirect('home')

def register_user_fn(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f"Account created for {username}!")
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

def history_user_fn(request):
    if request.user.is_authenticated:
        code = Code.objects.filter(user_id=request.user.id)
        return render(request, 'history.html', {'code': code})
    else:
      messages.success(request, "You must be logged in to view the history!")
      return redirect('home')
    

def delete_history_fn(request, History_id):
    history = Code.objects.get(pk=History_id)
    history.delete()
    messages.success(request, "Deleted successfully!")
    return redirect('history')
    