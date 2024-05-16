from allauth.account import views
from django.shortcuts import redirect

from accounts.forms import SignupUserForm


# ログイン
class LoginView(views.LoginView):
    template_name = "accounts/login.html"


# ログアウト
class LogoutView(views.LogoutView):
    template_name = "accounts/logout.html"

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            self.logout()
        return redirect("/")


# アカウント登録
class SignupView(views.SignupView):
    template_name = "accounts/signup.html"
    form_class = SignupUserForm
