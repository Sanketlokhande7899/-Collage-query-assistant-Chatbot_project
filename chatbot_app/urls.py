
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("chat/", views.chat, name="chat"),
    path("chat-history/",views.chat_history,name="chat_history"),
    path("profile/",views.profile,name="profile" ),
    path("admin-faq/", views.admin_faq,name="admin_faq"),
    path("faq-form/",views.faq_form,name="faq_form"),
    path("404/",views.page_not_found,name="404"),
    path("faq-management/",views.faq_management,name="faq_management"),
    path("users/",views.users_list,name="users_list"),
    path("today-chats/",views.today_chats,name="today_chats"),
    path("admin-chat-history/",views.admin_chat_history,name="admin_chat_history"),
    path("admin-login/", views.admin_login, name="admin_login"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),

]