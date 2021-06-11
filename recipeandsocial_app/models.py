from django.db import models
import bcrypt, re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
  def registration_val(self, post_data):
    errors = {}
    if len(post_data['first_name']) < 2:
      errors['first_name'] = 'First name should be at least 2 characters'
    if len(post_data['last_name']) < 2:
      errors['last_name'] = 'Last name should be at least 2 characters'
    if not EMAIL_REGEX.match(post_data['email']):
      errors['email'] = 'Email is not valid'
    if len(post_data['password']) < 8:
      errors['password'] = "Password must be 8 characters long"
    if post_data['password'] != post_data['confirm_password']:
      errors['password'] = 'Your password do not match'
    print('gets inside registration val function')
    emailCheck = self.filter(email=post_data['email'])
    if emailCheck:
      errors['email'] = "That email is already in use"
    return errors
  def authenticate(self, email, password):
    users = self.filter(email=email)
    if not users:
      return False
    user = users[0]
    return bcrypt.checkpw(password.encode(), user.password.encode())

class User(models.Model):
  first_name = models.CharField(max_length=45)
  last_name = models.CharField(max_length=45)
  email = models.EmailField(unique=True)
  password = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add=True, null=True)
  updated_at = models.DateTimeField(auto_now=True, null=True)

  objects = UserManager()

  def __str__(self):
    return f"{self.first_name} {self.last_name} {self.email}"

class RecipeManager(models.Manager):
  def basic_validation(self, post_data):
    errors = {}
    if len(post_data['recipe_name']) < 2:
        errors['recipe_name'] = 'Name must be at least 2 characters!'
    if len(post_data['ingredients']) < 5:
        errors['ingredients'] = 'Ingredients must be at least 5 characters!'
    return errors

class Recipe(models.Model):
  recipe_name = models.CharField(max_length=255)
  ingredients = models.CharField(max_length=255)
  cooking_instruction = models.TextField(max_length=2000)
  desc = models.TextField()
  duration = models.IntegerField()
  user = models.ForeignKey(User, related_name="recipes", on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True, null=True)
  updated_at = models.DateTimeField(auto_now=True, null=True)
  likes = models.ManyToManyField(User, related_name="likes")
  
  objects = RecipeManager()

class Comment(models.Model):
  text = models.CharField(max_length=280)
  user = models.ForeignKey(User, related_name="comment", on_delete=models.CASCADE)
  recipe = models.ForeignKey(Recipe, related_name="comments", on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True, null=True)
  updated_at = models.DateTimeField(auto_now=True, null=True)