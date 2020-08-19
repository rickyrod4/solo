from django.db import models
import bcrypt
import re

#Email Regex101
EMAIL_MATCH = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    #Validating the User Registration Information
    def validations(self, form_data):
        errors = {}
        if len(form_data['first_name']) < 1:
            errors['first_name'] = 'Must enter a first name' 

        if len(form_data['last_name']) < 1:
            errors['last_name'] = 'Must enter a last name' 
        
        if len(form_data['email']) < 1:
            errors['email'] = 'Must enter an email'
        
        if len(form_data['password']) < 1:
            errors['password'] = 'Must enter an password'
        
        if len(form_data['confirm']) < 1:
            errors['confirm'] = 'Must confirm your password'
        
        if form_data['password'] != form_data['confirm']:
            errors['confirm'] = 'Passwords do not match'   
        
        if not EMAIL_MATCH.match(form_data['email']):
            errors['email'] = 'Invalid Email'
        
        users_with_email = self.filter(email=form_data['email'])
        if users_with_email:
            errors['email'] = 'Email Is Already Registered'                 
        return errors
    #Registering A User
    def register(self, form_data):
        hash1 = bcrypt.hashpw(form_data['password'].encode(),bcrypt.gensalt()).decode()
        self.create(
            first_name = form_data['first_name'],
            last_name = form_data['last_name'],
            email = form_data['email'],
            password = hash1
        )
    #Authenticating Login Information
    def authenticate(self, email, password):
        users_with_emails = self.filter(email = email)
        if not users_with_emails:
            return False
        user = users_with_emails[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())

    #For Updating User Account Information
    def update(self, form_data, id):
        user = self.get(id = id)
        errors = {}
        if len(form_data['first_name'])>1:
            if len(form_data['first_name'])>3:
                user.first_name = form_data['first_name']
            else:
                errors['first_name'] = 'First Name Must Contain At Least 3 Characters'

        if len(form_data['last_name'])>1:
            if len(form_data['last_name'])>3:
                user.last_name = form_data['last_name']
            else:
                errors['last_name'] = 'Last Name Must Contain At Least 3 Characters'

        users_with_email = self.filter(email=form_data['email'])
        if len(form_data['email'])>1:
            if not EMAIL_MATCH.match(form_data['email']):
                errors['email'] = 'Invalid Email'
            elif users_with_email:
                errors['email'] = 'Email Is Already Registered'
            else:
                user.email = form_data['email']

        if len(form_data['password'])>1:
            if form_data['password'] == form_data['confirm']:
                hash2 = bcrypt.hashpw(form_data['password'].encode(),bcrypt.gensalt()).decode()
                user.password = hash2
            else:
                errors['password'] = 'Passwords Do Not Match'

        if len(form_data['confirm'])>1:
            if form_data['confirm'] != form_data['password']:
                errors['password'] = 'Passwords Do Not Match'


        if errors:
            return errors
        else:
            user.save()
            errors['success'] = 'Account Successfully Updated'
            return errors


# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    #tacos_ordered
    #favorite_taco
    #taco_History
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Taco(models.Model):
    taco_type = models.CharField(max_length=255)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    tacos_for = models.ManyToManyField(User, related_name='taco_history')
    favorite = models.ManyToManyField(User, related_name='favorite_taco')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Order(models.Model):
    quantity_ordered = models.IntegerField()
    total_price = models.DecimalField(decimal_places=2, max_digits=5)
    ordered_by = models.ForeignKey(User, related_name='tacos_ordered', on_delete=models.CASCADE, default = None)
    

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 