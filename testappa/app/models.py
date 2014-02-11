from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.core import validators
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices

# Create your models here.
import re
STATUS = Choices(('active','Active'), ('inactive', 'Inactive'))
# ROLE = roles()
ACCESS_LEVEL = Choices((0, '---'), (1, 'One'),(2, 'Two'), (3, 'Three'),(4, 'Four'),(5, 'Five'))

TRUE_FALSE = Choices(('true', 'True'), ('false', 'False'))

class TeaUser(AbstractBaseUser):

    username = models.CharField(_('username'), max_length=30, unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, numbers and '
                    '@/./+/-/_ characters'),
        validators=[
            validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Enter a valid username.'), 'invalid')
        ])
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    common_name = models.CharField(max_length=255, blank=True, default='')
    date_of_birth = models.DateField(null=True)
    email = models.EmailField(_('email address'), blank=True)
    organization = models.CharField(max_length=40, blank=True)
    school = models.CharField(max_length=40, blank=True)
    state_id = models.CharField(max_length=40, blank=True)
    sis_id = models.CharField(max_length=40, blank=True)
    grade = models.CharField(max_length=5, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default=STATUS.active)
    role = models.CharField(max_length=40, default='student')
    manager = models.CharField(max_length=10, choices=TRUE_FALSE, default=TRUE_FALSE.false)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


    class Meta:
        swappable = 'AUTH_USER_MODEL'

    @property
    def is_staff(self):
        return True


    @property
    def is_active(self):
        if self.status == STATUS.active:
            return True
        else:
            return False

    @is_active.setter
    def is_active(self, value):
        # Todo : add other roles
        if value == True:
            self.status = STATUS.active

    @property
    def is_superuser(self):
        try:
            if self.manager.lower() == 'true':
                return True
        except Exception:
            pass
        return False

    @is_superuser.setter
    def is_superuser(self, value):
        if value:
            self.manager = TRUE_FALSE.true

    def get_username(self):
        "Return the identifying username for this User"
        return getattr(self, self.USERNAME_FIELD)

    def __str__(self):
        return self.get_username()

    def natural_key(self):
        return (self.get_username(),)

    def is_anonymous(self):
        """
        Always returns False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True
    def get_all_permissions(self, obj=None):

        if not hasattr(self, '_perm_cache'):
            r = Role.objects.get_by_natural_key(self.role)
            self._perm_cache = set(["%s.%s" % (p.content_type.app_label, p.codename) for p in r.permissions.all()])
        return self._perm_cache

    def has_perm(self, perm, obj=None):

        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True
        if perm in self.get_all_permissions():
            return True
        return False

    def has_perms(self, perm_list, obj=None):

        for perm in perm_list:
            if not self.has_perm(perm, obj):
                return False
        return True

    def has_module_perms(self, app_label):
        """
        Returns True if the user has any permissions in the given app label.
        Uses pretty much the same logic as has_perm, above.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        for perm in self.get_all_permissions(set):
            if perm[:perm.index('.')] == app_label:
                return True
        return False

    def get_full_name(self):
        """
        Returns the email.
        """
        return self.email

    def get_short_name(self):
        """
        Returns the email.
        """
        return self.email

    def validate(self, user=None, force_clean=False):

        return
