from django.db import models
import bcrypt
import re
PASS_REGEX = re.compile(r'[a-zA-Z]')
NAME_REGEX = re.compile(r'[a-zA-Z ]')
from datetime import datetime, date
# Create your models here.
class UserManager(models.Manager):
    def login(self, post):
        user_list = self.filter(username=post['username'])
        if user_list:
            user = user_list[0]
            if bcrypt.hashpw(post['password'].encode(), user.password.encode()) == user.password:
                return user
        return None


    def register(self, post):
        encrypted_password= bcrypt.hashpw(post['password'].encode(), bcrypt.gensalt())

        user = self.create(name=post['name'], username=post['username'], password= encrypted_password, hired=post['date_hired'])


    def validate_user_info(self, post):
        today = date.today()
        errors = []
        if len(post['name']) == 0:
            errors.append("Name is required")
        elif len(post['name']) < 3:
            errors.append("Name must be at least 3 characters")
        elif not NAME_REGEX.match(post['name']):
            errors.append("Name must consist of letters and spaces only")

        if len(post['username']) == 0:
                errors.append("Username is required")
        elif len(post['username']) < 3:
            errors.append("Username must be at least 3 characters")
        elif not post['username'].isalpha():
            errors.append("Username must consist of letters only")

        if len(post['password'])<8:
            errors.append("Error: Password cannot be empty OR less than 8 characters")
        elif not PASS_REGEX.match(post['password']):
            errors.append("Error: Password must contain a letter")
        elif post['password'] != post['passconf']:
            errors.append("Error: Password doesn't match!")

        if len(post['date_hired']) == 0:
            errors.append("Date Hired is required!")
        else:
            try:
                date_hired = datetime.strptime(post['date_hired'], '%Y-%m-%d')
                if date_hired.date() > today:
                    errors.append("Only employees that have been hired today or earlier may make a wishlist. Future employees must wait until their first day on the job.")
                print date_hired
            except:
                print post['date_hired']
                errors.append("Please enter a valid date for the hired date!")


        if len(self.filter(username=post['username'])) > 0:
            errors.append("Username unavailable!")
        return errors
