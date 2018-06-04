from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group


# TODO : Add to Practitioner Group
class Practitioner(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


# TODO : Add to Patient Group
class Patient(models.Model):
    # Set who is taking care of the doctor
    practitioner = models.ForeignKey(Practitioner, on_delete=models.CASCADE)

    # Store Patient Specific Information
    name = models.CharField(max_length=255, null=True)
    gravida = models.IntegerField()
    para = models.IntegerField()
    date_of_admission = models.DateField(auto_now_add=True)  # Auto-Add when Created
    time_of_admission = models.TimeField(auto_now_add=True)  # Auto-Add when Created
    ruptured_membrane_time = models.TimeField(null=True)
    vaginal_births = models.IntegerField()  # Vaginal births past 20 week period
    age = models.PositiveIntegerField()
    height = models.PositiveIntegerField()  # Height in Inches
    weight = models.PositiveIntegerField()  # Weight in Pounds

    def __str__(self):
        return self.name or ''

    '''
    BMI Takes the height in inches and the weight in pounds and converts it to a BMI using:
    http://extoxnet.orst.edu/faqs/dietcancer/web2/twohowto.html
    '''

    @property
    def bmi(self):
        return round((self.weight * 0.45) / ((self.height * 0.025) ** 2), 2)


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, username, password=None, is_active=True, is_staff=False,
                    is_superuser=False):
        if not username:
            raise ValueError("Username is Required")
        if not password:
            raise ValueError("Password is Required")

        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)  # Set/Change user Password
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.is_active = is_active
        user.first_name = first_name
        user.last_name = last_name
        user.username = username

        user.save(using=self._db)

        return user

    def create_staffuser(self, username, first_name, last_name, email, password=None):
        user = self.create_user(email, first_name, last_name, username, password=password, is_staff=True)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name, email, password=None):
        user = self.create_user(email, first_name, last_name, username, password=password, is_staff=True,
                                is_superuser=True)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    practitioner = models.OneToOneField(Practitioner, null=True, on_delete=models.CASCADE)
    patient = models.OneToOneField(Patient, null=True, on_delete=models.CASCADE)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def get_email(self):
        return self.email

    def get_username(self):
        return self.username
