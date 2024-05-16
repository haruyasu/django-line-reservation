from django.urls import path

from app import views

app_name = "app"

urlpatterns = [
    # トップページ
    path("", views.IndexView.as_view(), name="index"),
    # 店舗詳細
    path("store/<int:store_id>/", views.StoreDetailView.as_view(), name="store_detail"),
    path(
        "store/<int:store_id>/<int:service_id>/",
        views.StoreDetailView.as_view(),
        name="store_detail",
    ),
    # 店舗登録
    path("store_register/", views.StoreRegisterView.as_view(), name="store_register"),
    # サービス登録
    path(
        "service_register/",
        views.ServiceRegisterView.as_view(),
        name="service_register",
    ),
    # 店舗特別休日
    path("store_holiday/", views.StoreHolidayView.as_view(), name="store_holiday"),
    # プロフィール
    path("profile/", views.ProfileView.as_view(), name="profile"),
    # 予約
    path("reservation/", views.ReservationView.as_view(), name="reservation"),
    # スタッフ休日
    path("staff_holiday/", views.StaffHolidayView.as_view(), name="staff_holiday"),
]
