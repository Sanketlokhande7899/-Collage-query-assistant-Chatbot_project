from django.contrib import admin
from .models import (  UserProfile,FAQ,Conversation,ChatMessage,Feedback,AdminLog,ModelPerformance)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user")
    search_fields = ("user__username",)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "answer")
    search_fields = ("question", "answer")


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("id", "student", "status", "started_at")
    list_filter = ("status",)
    search_fields = ("student__username",)


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "conversation", "confidence_score", "created_at")
    search_fields = ("user_message",)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("id", "rating", "created_at")


@admin.register(AdminLog)
class AdminLogAdmin(admin.ModelAdmin):
    list_display = ("id", "admin", "action", "created_at")


@admin.register(ModelPerformance)
class ModelPerformanceAdmin(admin.ModelAdmin):
    list_display = ("id", "model_name", "accuracy", "trained_at")