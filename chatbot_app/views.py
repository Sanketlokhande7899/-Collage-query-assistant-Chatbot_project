from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required
from .forms import FAQForm
from chatbot_app.ai.predict import predict_intent
from chatbot_app.models import FAQ, Conversation, ChatMessage
from chatbot_app.ai.predict import predict_intent
from chatbot_app.ai.ollama_api import ask_ollama
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def home(request):
    return render(request, "home.html")

@login_required
def dashboard(request):

    total_chats = ChatMessage.objects.filter(
        conversation__student=request.user
    ).count()

    
    today = timezone.now().date()

    today_chats = ChatMessage.objects.filter(
        conversation__student=request.user,
        created_at__date=today
    ).count()

   
    total_faqs = FAQ.objects.count()

    context = {

        "total_chats": total_chats,

        "today_chats": today_chats,

        "total_faqs": total_faqs,

    }

    return render(
        request,
        "dashboard.html",
        context
    )
@login_required(login_url='login')
def chat(request):

    response = ""
    conversation = None
    highest_score = 0

    if request.user.is_authenticated:

        conversation = Conversation.objects.filter(
            student=request.user,
            status="active"
        ).first()

        if not conversation:

            conversation = Conversation.objects.create(
                student=request.user,
                title="My Chat"
            )

    if request.method == "POST":

        question = request.POST.get("question")

        print("Question:", question)

        # Predict Intent
        intent = predict_intent(question)

        print("Predicted Intent:", intent)

        # Get all FAQs of predicted intent
        faqs = FAQ.objects.filter(intent=intent)

        best_match = None
        highest_score = 0

        for faq in faqs:

            score = calculate_similarity(
                question,
                faq.question
            )

            print(f"{faq.question} -> {score}")

            if score > highest_score:
                highest_score = score
                best_match = faq

        # FAQ Answer OR Ollama AI Answer

        if best_match and highest_score >= 0.50:

            response = best_match.answer

            print("Best Match:", best_match.question)
            print("Similarity:", highest_score)

            if conversation:

                ChatMessage.objects.create(
                    conversation=conversation,
                    user_message=question,
                    bot_response=response,
                    confidence_score=highest_score
                )

        else:

            print("No FAQ found. Calling Ollama AI...")

            response = ask_ollama(question)

            if conversation:

                ChatMessage.objects.create(
                    conversation=conversation,
                    user_message=question,
                    bot_response=response,
                    confidence_score=0
                )

    return render(
        request,
        "chat.html",
        {
            "response": response,
            "confidence": round(highest_score * 100, 2)
            if request.method == "POST" else None,
        }
    )
def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Registration Successful."
            )

            return redirect("login")

        else:

            messages.error(
                request,
                "Please correct the errors below."
            )

    else:

        form = RegisterForm()

    return render(
        request,
        "register.html",
        {
            "form": form
        }
    )
def login_view(request):

    if request.method == "POST":

        form = LoginForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(
                username=username,
                password=password
            )

            print(user)  

            if user:

                auth_login(request, user)

                return redirect("dashboard")

            else:
                print("Login Failed")

    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})

def logout_view(request):

    logout(request)

    return redirect("login")

@login_required
def chat_history(request):

    chats = ChatMessage.objects.filter(
        conversation__student=request.user
    ).order_by("-created_at")

    return render(
        request,
        "chat_history.html",
        {
            "chats": chats
        }
    )
@login_required
def profile(request):
    return render(request, "profile.html")


@login_required
def faq_form(request):
    if request.method == "POST":
        form = FAQForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("faq_form")  
    else:
        form = FAQForm()

    return render(request, "faq_form.html", {"form": form})

@login_required
def admin_faq(request):
    faqs = FAQ.objects.all()
    return render(request, "admin_faq.html", {"faqs": faqs})

def page_not_found(request, exception):

    return render(request, "404.html", status=404)

@login_required
def faq_management(request):

    faqs = FAQ.objects.all().order_by("-id")

    return render(
        request,
        "faq_management.html",
        {
            "faqs": faqs
        }
    )
@login_required
def users_list(request):

    users = User.objects.all()

    return render(
        request,
        "users_list.html",
        {
            "users": users
        }
    )
@login_required
def today_chats(request):

    today = timezone.now().date()

    chats = ChatMessage.objects.filter(
        created_at__date=today
    )

    return render(
        request,
        "today_chats.html",
        {
            "chats": chats
        }
    )

@staff_member_required
def admin_chat_history(request):

    chats = ChatMessage.objects.all().order_by("-created_at")

    return render(
        request,
        "admin_chat_history.html",
        {
            "chats": chats
        }
    )
def admin_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            username=username,
            password=password
        )

        if user is not None and user.is_superuser:

            login(request, user)

            return redirect("admin_dashboard")

    return render(request, "admin_login.html")


@login_required
def admin_dashboard(request):

    if not request.user.is_superuser:
        return redirect("login")

    context = {
        "total_users": User.objects.count(),
        "total_chats": ChatMessage.objects.count(),
        "total_faqs": FAQ.objects.count(),
        "today_chats": ChatMessage.objects.filter(
            created_at__date=timezone.now().date()
        ).count(),
    }

    return render(request, "admin_dashboard.html", context)