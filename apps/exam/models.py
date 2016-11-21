from __future__ import unicode_literals
from django.db import models
from ..logreg.models import User
from datetime import datetime, date

class WishManager(models.Manager):
    def validation(self, post):
        print post
        errors = []
        if len(post['wish']) == 0:
            errors.append("Wish cannot be empty!")
        elif len(post['wish']) < 3:
            errors.append("A wish must be at LEAST 3 characters!")

        if len(post['desc']) == 0:
            errors.append("Description cannot be empty!")
        elif len(post['desc']) < 10:
            errors.append("A wish must be at LEAST 10 characters!")
        return errors

class Wish(models.Model):
    wish = models.CharField(max_length=45)
    description = models.CharField(max_length=45)
    creator = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WishManager()

class Shared(models.Model):
    sharedwish = models.ForeignKey(Wish)
    adder = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
