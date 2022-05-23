from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
)


# Create your models here.

class OtherUsers(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=150, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class ActiveManager(models.Manager):
    def active(self):
        return self.filter(active=True)


class EquipmentIssue(models.Model):
    name = models.CharField(max_length=48)
    department = models.CharField(max_length=48)
    equipment_category = models.CharField(max_length=48)
    serial_number = models.CharField(max_length=48)
    description = models.TextField(blank=True)
    date_of_issue = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=32)
    slug = models.SlugField(max_length=48)
    is_issued = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    objects = ActiveManager()
    CATEGORIES = ('name', 'department', 'equipment_category', 'status, slug')

    def __str__(self):
        return self.name

    def save(self):
        self.slug = slugify(self.name)
        super(EquipmentIssue, self).save()

    def get_absolute_url(self):
        return reverse('issues', args=[str(self.slug)])


class EquipmentIssueTag(models.Model):
    equipmentIssues = models.ManyToManyField(EquipmentIssue, blank=True)
    name = models.CharField(max_length=32)
    slug = models.SlugField(max_length=48)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
