from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db.models.deletion import SET_NULL

from django.utils.translation import ugettext_lazy
# Create your models here.


class Manager(BaseUserManager):
    def create_user(self, email, username, password, first_name, last_name):

        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        if not password:
            raise ValueError('Users must have a password')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, first_name=None, last_name=None):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email', max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(
        verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    display_picture = models.ImageField(upload_to='uploads',)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name',]

    objects = Manager()

    def __str__(self):
        return self.email

        # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin


class Item(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    type = models.CharField(max_length=20)
    price = models.IntegerField()
    stock = models.IntegerField()

    def __str__(self):
        return self.name


class Architect(User):
    experience = models.TextField()
    education = models.CharField(max_length=30)

    def __str__(self):
        return self.email


class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date_placed = models.DateTimeField(auto_now_add=True)
    ship_date = models.DateTimeField()
    address = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    items = models.ManyToManyField(Item)

    def __str__(self):
        return str(self.id)


class Meeting(models.Model):
    time = models.DateTimeField()
    title = models.CharField(max_length=30)
    client_id = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL)
    client_name = models.CharField(max_length=20)
    status = models.BooleanField(default=False)
    fee = models.IntegerField(default=1000)

    def __str__(self):
        return self.title


class Cart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField(Item, blank=True)

    def __str__(self):
        return str(self.id)


class Project(models.Model):
    description = models.TextField()
    title = models.CharField(max_length=30)
    client_id = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL)
    client_name = models.CharField(max_length=20)
    percentage = models.IntegerField()
    cost = models.IntegerField()
    start_date = models.DateTimeField(auto_now_add=True)
    comp_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title


class Design(models.Model):
    client_id = models.ForeignKey(
        User, related_name="client", null=True, on_delete=models.SET_NULL)
    arch_id = models.ForeignKey(
        Architect, related_name="architect", null=True, on_delete=models.SET_NULL)
    client_name = models.CharField(max_length=20)
    cost = models.IntegerField(default=1000)
    img = models.CharField(max_length=100, blank=True)
    status = models.BooleanField(default=False)
    description = models.TextField()

    def __str__(self):
        return str(self.id)


method_choices = (
    ('Cash on delivery', 'cash on delivery'),
    ('Online', 'online'),
)


class OrderPayment(models.Model):

    order_id = models.ForeignKey(
        Order, on_delete=models.CASCADE)
    method = models.CharField(max_length=20, choices=method_choices)
    amount = models.IntegerField()
    status = models.BooleanField(default=False)
    date = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.id)


class DesignPayment(models.Model):

    design_id = models.ForeignKey(
        Design, on_delete=models.CASCADE)
    amount = models.IntegerField()
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class MeetingPayment(models.Model):

    meeting_id = models.ForeignKey(
        Meeting, on_delete=models.CASCADE)
    amount = models.IntegerField()
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
