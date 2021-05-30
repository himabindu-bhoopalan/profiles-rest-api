from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

#abstract base user and persmissionmixin is the standard models 
#used when overriding the default classes 
class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self,email,name,password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError("Users must have an email address")

        #normalize the email address-make 2nd half in lower case 
        email=self.normalize_email(email)
        #creates a new user 
        user=self.model(email=email,name=name)
        #by default django encrypts it 
        user.set_password(password)

        #specified such in django doc 
        user.save(using=self._db)
        return user 

    def create_superuser(self,email,name,password):
        """Create a super user profile and save it with given details"""
        user=self.create_user(email,name,password)
        #is_superuser is automatically created by PermissionMixin even if we didnt specify it 
        user.is_superuser=True
        user.is_staff=True
        user.save(using=self._db)

        return user 


class UserProfile(AbstractBaseUser,PermissionsMixin):
    '''Database model for users in the system'''
    email=models.EmailField(max_length=255,unique=True)
    name=models.CharField(max_length=255)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)

    objects=UserProfileManager()

    #usually called user_name , we are overiding it to email 
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['name']

    #because we specify function in the class, self id default arg
    def get_full_name(self):
        """Retrive full name of the user"""
        return self.name

    def get_short_name(self):
        """Retrieve shot name"""
        return self.name
    
    #this is function specifies the string representation of our model
    #this is recommended for all django models 
    #because when we convert it to a string , it wont be a meaningful output , so we specify the data here
    #we use this when we want to print it later 
    def __str__(self):
        """Return string representation of our user"""
        return self.email

