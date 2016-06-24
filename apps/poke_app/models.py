from __future__ import unicode_literals
import re, bcrypt

from django.db import models

# Create your models here.

NAME_REGEX = re.compile(r'^[\w\s]*$')
EMAIL_REGEX = re.compile(r'^[\w\.\+-]+@[\w\.-]+\.[a-zA-Z]*$')
ALIAS_REGEX = re.compile(r'^[^"`()\[\]{};]+$')


class UserManager(models.Manager):
    def login(self, email, password):
        errors = {}
        user = User.objects.filter(email__iexact=email)
        if user:
            if bcrypt.hashpw(password.encode('utf-8'), user[0].password.encode('utf-8')) == user[0].password:
                return (True, user[0])
            else:
                errors['login-password'] = "Password incorrect"
        else:
            errors['login-email'] = "Email not in database"

        return (False, errors)

    def register(self, **kwargs):
        name = kwargs['name'][0]
        alias = kwargs['alias'][0]
        email = kwargs['email'][0]
        password = kwargs['password'][0]
        confirm_pw = kwargs['confirm_pw'][0]
        birthdate = kwargs['birthdate'][0]

        errors = {}
        if len(name) > 1:
            if not NAME_REGEX.match(name):
                errors['name'] = "Name must be letters and spaces only"
        else:
            errors['name'] = "Name must be at least 2 characters"

        if len(alias) > 1:
            if not ALIAS_REGEX.match(alias):
                errors['alias'] = "Alias must not contain quotes, brackets, or semicolons"
        else:
            errors['alias'] = "Alias must be at least 2 characters"

        if len(email) > 0:
            if not EMAIL_REGEX.match(email):
                errors['email'] = "Email is not valid"
        else:
            errors['email'] = "Email must not be empty"

        if password == confirm_pw:
            if len(password) < 8:
                errors['password'] = "Password must be at least 8 characters"
        else:
            errors['password'] = "Password confirmation does not match"

        # date validations

        if errors:
            return (False, errors)

        encrypted_pass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        user = {
            'name': name,
            'alias': alias,
            'email': email,
            'birthdate': birthdate,
            'password': encrypted_pass,
        }

        return (True, user)

class User(models.Model):
    name = models.CharField(max_length=200)
    alias = models.CharField(max_length=200)
    email = models.EmailField()
    password = models.CharField(max_length=200)
    birthdate = models.DateField()
    userManager = UserManager()
    objects = models.Manager()


class Poke(models.Model):
    poker = models.ForeignKey(User, related_name='poke_set')
    poked = models.ForeignKey(User, related_name='poked_set')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
