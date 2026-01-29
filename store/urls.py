from django.urls import path
from django.contrib.auth import views as auth_views
from .views import store_home, create_checkout, register_view

urlpatterns = [
    path("", store_home, name="home"),
    path("checkout/", create_checkout, name="checkout"),

    path("login/", auth_views.LoginView.as_view(template_name="store/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", register_view, name="register"),
]
