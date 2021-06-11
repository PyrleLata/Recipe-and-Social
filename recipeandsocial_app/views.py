from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
import re, bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
    return render(request, 'index.html')

def sign_up(request):
    return render(request, 'register.html') 

def register(request):
    if request.method == "POST":
        errors = User.objects.registration_val(request.POST)
        if len(errors) > 0:
            for key, val in errors.items():
                messages.error(request, val)
            return redirect("/signup")
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        hash_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        User.objects.create(first_name=first_name, last_name=last_name, email=email, password=hash_pw)
    return HttpResponse("<h1>Success! You can now <a href = '/login'>Log In</a></h1>")

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        if not User.objects.authenticate(email, password):
            messages.error(request, 'Email and Password do not match')
            return redirect("/")
        user = User.objects.get(email=email)
        request.session['user_id'] = user.id
        return redirect("/recipes")
    return redirect('/')

def logout(request):
    del request.session['user_id']
    return redirect('/')

def add_recipe(request):
    recipe_name = request.POST['recipe_name']
    ingredients = request.POST['ingredients']
    duration = request.POST['duration']
    desc = request.POST['desc']
    instruction = request.POST['steps']
    errors = Recipe.objects.basic_validation(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect('/recipes')
    
    user = User.objects.get(id=request.session['user_id'])
    Recipe.objects.create(recipe_name = recipe_name, ingredients = ingredients, cooking_instruction = instruction, desc = desc, duration = duration, user = user)
    return redirect('/recipes')

def recipes(request):
    if 'user_id' not in request.session:
        return HttpResponse("<h1>You must be <a href = '/login'>logged in</a> to get to your account</h1>")
    user = User.objects.get(id=request.session['user_id'])
    recipes = Recipe.objects.all()
    context = {
        "user": user,
        "recipes": recipes,
    }
    return render(request, 'list.html', context)



def recipe_info(request, recipe_id):
    recipe_info = Recipe.objects.get(id=recipe_id)
    context = {
        "recipe": recipe_info,
    }
    return render(request, 'recipe_info.html', context)

def edit_recipe(request, recipe_id):
    if request.method == "GET":
        recipe_to_update = Recipe.objects.get(id=recipe_id)
        context = {
            "recipe": recipe_to_update,
        }
        
    return render(request, 'edit-recipe.html', context)

def update_recipe(request, recipe_id):
    if request.method == "POST":
        recipe_to_update = Recipe.objects.get(id=recipe_id)
        errors = Recipe.objects.basic_validation(request.POST)
        if len(errors) > 0:
            for key, val in errors.items():
                messages.error(request, val)
            return redirect(f"/recipes/{recipe_to_update.id}/edit")
            
        recipe_to_update.recipe_name = request.POST['recipe_name']
        recipe_to_update.ingredients = request.POST['ingredients']
        recipe_to_update.cooking_instruction = request.POST['steps']
        recipe_to_update.desc = request.POST['desc']
        recipe_to_update.duration = request.POST['duration']
        recipe_to_update.save()
        context = {
            "recipe": recipe_to_update,
        }
    
    return redirect(f"/recipes/{recipe_to_update.id}")

def destroy_recipe(request, recipe_id):
    recipe_to_delete = Recipe.objects.get(id=recipe_id)
    recipe_to_delete.delete()
    return redirect("/recipes")

def recipe_wall(request):
    user = User.objects.get(id=request.session['user_id'])
    recipes = Recipe.objects.all()
    context = {
        "user": user,
        "recipes": recipes,
    }
    return render(request, 'recipe_feed.html', context)

def add_like(request, recipe_id):
  recipe = Recipe.objects.get(id=recipe_id)
  user = User.objects.get(id=request.session['user_id'])
  recipe.likes.add(user)
  return redirect('/recipes/wall')

def add_comment(request):
  comment_text = request.POST['comment_text']
  recipe_id = request.POST['recipe_id']
  user = User.objects.get(id=request.session['user_id'])
  recipe = Recipe.objects.get(id=recipe_id)
  Comment.objects.create(text=comment_text, user=user, recipe=recipe)
  return redirect('/recipes/wall')

def delete_comment(request, comment_id):
  comment_to_delete = Comment.objects.get(id=comment_id) 
  comment_to_delete.delete()
  return redirect('/recipes/wall')