from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib import auth # para ver se o usuario existe no banco de dados

def cadastro(request):
    if request.method =="GET":
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if senha != confirmar_senha:
            messages.add_message(request, constants.ERROR, 'As senhas não coincidem')
            return redirect('/usuarios/cadastro')
        
        if len(senha) < 6:
            messages.add_message(request, constants.ERROR, 'A senha deve conter pelo menos 6 caracteres' )
            return redirect('/usuarios/cadastro')
        
        users = User.objects.filter(username=username)
        if user.exists():
            messages.add_message(request, constants.ERROR,'Já existe um usuário com esse username' )
            return redirect('/usuarios/cadastro')
        
        user = User.objects.create_user(
            username=username,
            password=senha
        )


        return redirect('/usuarios/logar') 
    
def logar(request):
    if request.method == "GET":
        return render(request, 'logar.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = auth.authenticate(request, username= username, password=senha)  # o authenticate só busca quando o usuario existe no banco de dados
        if user:
            auth.login(request, user)  # atrelar ao ip do usuario ao usuario que de fato esta logado para que quando ele acessar a pagina ele consiga acessar com aquele usuario
            return redirect('/empresarios/cadastrar_empresa')
        messages.add_message(request, constants.ERROR, 'Usuario ou senha inválidos')
        return redirect('/usuarios/logar')
