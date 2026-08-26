from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15)
    department = models.CharField(max_length=100, blank=True)
    year = models.CharField(max_length=20, blank=True)
    roll_number = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

class FAQ(models.Model):
    CATEGORY_CHOICES = [
        ('admission', 'Admission'),
        ('fees', 'Fees'),
        ('courses', 'Courses'),
        ('hostel', 'Hostel'),
        ('placements', 'Placements'),
        ('library', 'Library'),
        ('general', 'General'),
    ]

    question = models.TextField()
    answer = models.TextField()
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    keywords = models.TextField(blank=True)
    intent = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

class Conversation(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('closed', 'Closed'),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="New Conversation")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.username} - {self.title}"

class ChatMessage(models.Model):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    user_message = models.TextField()
    bot_response = models.TextField(blank=True)

    detected_intent = models.CharField(max_length=100, blank=True)
    confidence_score = models.FloatField(default=0.0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.id} - {self.conversation.student.username}"

class Feedback(models.Model):
    chat_message = models.OneToOneField(
        ChatMessage,
        on_delete=models.CASCADE,
        related_name='feedback'
    )

    rating = models.IntegerField()
    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback - {self.chat_message.id}"

class AdminLog(models.Model):
    ACTION_CHOICES = [
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
    ]

    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100)
    object_id = models.IntegerField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.admin.username} - {self.action}"

class ModelPerformance(models.Model):
    model_name = models.CharField(max_length=100)
    accuracy = models.FloatField(default=0.0)
    precision = models.FloatField(default=0.0)
    recall = models.FloatField(default=0.0)
    f1_score = models.FloatField(default=0.0)
    trained_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.model_name
        