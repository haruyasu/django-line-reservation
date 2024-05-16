from django.urls import path

from line import views

app_name = "line"

urlpatterns = [
    # 店舗一覧
    path("", views.IndexView.as_view(), name="index"),
    # LINEコールバック
    path("callback/", views.CallbackView.as_view(), name="callback"),
    # サービス一覧
    path("service/<int:store_id>/", views.ServiceView.as_view(), name="service"),
    # スタッフ一覧
    path("staff/<int:service_id>/", views.StaffView.as_view(), name="staff"),
    # 予約カレンダー
    path(
        "calendar/<int:service_id>/<int:staff_id>/",
        views.CalendarView.as_view(),
        name="calendar",
    ),
    path(
        "calendar/<int:service_id>/<int:staff_id>/<int:year>/<int:week>/",
        views.CalendarView.as_view(),
        name="calendar",
    ),
    # お客様情報入力
    path(
        "reserve/<int:service_id>/<int:staff_id>/<int:year>/<int:month>/<int:day>/<int:hour>/<int:minute>/",
        views.ReserveView.as_view(),
        name="reserve",
    ),
    # 予約内容確認
    path(
        "confirm/<int:service_id>/<int:staff_id>/<int:year>/<int:month>/<int:day>/<int:hour>/<int:minute>/",
        views.ConfirmView.as_view(),
        name="confirm",
    ),
    # 予約完了
    path("done/", views.DoneView.as_view(), name="done"),
]
