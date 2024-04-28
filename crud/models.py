from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    CATEGORY_CHOICES = [
        ('Education', 'Education'),
        ('Health', 'Health'),
        ('Food', 'Food'),
        ('Work', 'Work'),
        # Add more categories as needed
    ]

    name = models.CharField(max_length=100, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    STATUS_CHOICES = [
        ('To Do', 'To Do'),
        ('In Progress', 'In Progress'),
        ('Done', 'Done'),
    ]
    
    title = models.CharField(max_length=100)
    description = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Low')
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='To Do')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, default=1)  # Default to the first category

    def __str__(self):
        return self.title

class UniqueLink(models.Model):
    PERMISSION_CHOICES = [
        ('view', 'View Only'),
        ('edit', 'Edit'),
        ('admin', 'Admin'),
    ]

    url = models.CharField(max_length=100, unique=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    permission = models.CharField(max_length=10, choices=PERMISSION_CHOICES)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_links')