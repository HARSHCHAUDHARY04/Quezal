from django.db import models

class User(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    password_hash = models.CharField(max_length=255)
    user_type = models.CharField(max_length=50, default='student')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'

class Quiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    result_filename = models.CharField(max_length=255)
    original_filename = models.CharField(max_length=255, null=True, blank=True)
    num_questions = models.IntegerField()
    difficulty = models.CharField(max_length=50)
    mode = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'quizzes'
