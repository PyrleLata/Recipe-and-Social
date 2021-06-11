from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('signup', views.sign_up),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('recipes', views.recipes),
    path('add-recipe', views.add_recipe),
    path('recipes/<int:recipe_id>', views.recipe_info),
    path('recipes/<int:recipe_id>/edit', views.edit_recipe),
    path('recipes/<int:recipe_id>/update', views.update_recipe),
    path('recipes/<int:recipe_id>/destroy', views.destroy_recipe),
    path('recipes/wall', views.recipe_wall),
    path('add-like/<int:recipe_id>', views.add_like),
    path('add-comment', views.add_comment),
    path('delete-comment/<int:comment_id>', views.delete_comment),

]