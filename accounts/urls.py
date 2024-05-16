from django.urls import path

from accounts import views

app_name = "accounts"

urlpatterns = [
    # ログイン
    path("login/", views.LoginView.as_view(), name="login"),
    # ログアウト
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # アカウント登録
    path('signup/', views.SignupView.as_view(), name='signup'),
]
