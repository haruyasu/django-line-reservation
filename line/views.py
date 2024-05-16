from datetime import datetime, timedelta

from django.conf import settings
from django.http.response import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseServerError,
)
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    FollowEvent,
    MessageEvent,
    PostbackEvent,
    TextMessage,
    UnfollowEvent,
)

from app.models import (
    Customer,
    Reservation,
    Service,
    Staff,
    StaffHoliday,
    Store,
    StoreHoliday,
)
from line.forms import CustomerForm
from line.line_messages import (
    send_reservation_confirm_message,
    send_menu_message,
    send_new_menu_message,
    send_check_reservation_message,
    send_check_reservation_detail_message,
    send_change_reservation_message,
    send_cancel_reservation_message,
)

line_bot_api = LineBotApi(settings.CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.CHANNEL_SECRET)


# テキストメッセージ送信
def send_text_message(line_id, message):
    liff_json = {"type": "text", "text": message}
    result = TextMessage.new_from_json_dict(liff_json)
    try:
        line_bot_api.push_message(line_id, messages=result)
    except Exception:
        print("テキストメッセージを送信できませんでした")


# LINEコールバック
class CallbackView(View):
    def get(self, request):
        return HttpResponse("OK")

    def post(self, request):
        signature = request.META["HTTP_X_LINE_SIGNATURE"]
        body = request.body.decode("utf-8")

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            return HttpResponseBadRequest()
        except LineBotApiError as e:
            print(e)
            return HttpResponseServerError()

        return HttpResponse("OK")

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CallbackView, self).dispatch(*args, **kwargs)

    # 友達追加
    @handler.add(FollowEvent)
    def handle_follow(event):
        line_id = event.source.user_id

        # 既存のユーザーをチェック
        if not Customer.objects.filter(line_id=line_id).exists():
            try:
                # LINEユーザー情報を取得
                profile = line_bot_api.get_profile(line_id)
                # LINEユーザー名
                name = profile.display_name

                # 顧客登録
                Customer.objects.create(name=name, line_id=line_id)
                print("新しい友達追加: ", name)
            except LineBotApiError as e:
                print("新しい友達追加エラー: ", e)
        else:
            print("ユーザーはすでに登録されています。")

    # 友達解除
    @handler.add(UnfollowEvent)
    def handle_unfollow(event):
        line_id = event.source.user_id
        # 対応する顧客を見つけて削除
        try:
            user = Customer.objects.get(line_id=line_id)
            user.delete()
            print("友達解除されたユーザーを削除しました: ", line_id)
        except Customer.DoesNotExist:
            print("削除するユーザーが見つかりませんでした。", line_id)

    # テキストメッセージ
    @handler.add(MessageEvent, message=TextMessage)
    def text_message(event):
        try:
            # LINE ID取得
            line_id = event.source.user_id
            # 顧客情報取得
            customer = Customer.objects.get(line_id=line_id)
            # 予約情報取得
            reservations = Reservation.objects.filter(
                customer=customer, reservation_date__gt=timezone.now()
            )

            # メッセージ判定
            if event.message.text == "予約メニュー":
                if reservations.exists():
                    # 予約メニュー送信(予約あり)
                    send_menu_message(line_id)
                else:
                    # 予約メニュー送信(新規)
                    send_new_menu_message(line_id)
            elif event.message.text == "予約確認":
                if not reservations.exists():
                    send_text_message(line_id, "予約がありません")
                    return

                # 予約確認メッセージ送信
                send_check_reservation_message(line_id, reservations)

            elif event.message.text == "予約変更":
                if not reservations.exists():
                    send_text_message(line_id, "予約がありません")
                    return

                # 予約変更メッセージ送信
                send_change_reservation_message(line_id, reservations)

            elif event.message.text == "予約キャンセル":
                if not reservations.exists():
                    send_text_message(line_id, "予約がありません")
                    return

                # 予約キャンセルメッセージ送信
                send_cancel_reservation_message(line_id, reservations)

        except Exception as e:
            print(e)

    # ポストバック
    @handler.add(PostbackEvent)
    def on_postback(event):
        line_id = event.source.user_id
        data = dict(x.split("=") for x in event.postback.data.split("&"))
        # アクション取得
        action = data["action"]
        # 予約ID取得
        reservation_id = data["reservation_id"]
        reservation = Reservation.objects.get(id=reservation_id)

        if action == "予約確認":
            # 予約詳細メッセージ送信
            send_check_reservation_detail_message(line_id, reservation)

        elif action == "予約キャンセル":
            reservation.delete()
            send_text_message(line_id, "予約をキャンセルしました")


# 店舗一覧
class IndexView(View):
    def get(self, request):
        stores = (
            Store.objects.filter(services__staff__isnull=False)
            .distinct()
            .order_by("-created_at")
        )
        reservation_id = request.GET.get("reservation_id", None)

        return render(
            request,
            "line/index.html",
            {
                "stores": stores,
                "reservation_id": reservation_id,
                "liff_id": settings.LIFF_ID,
            },
        )


# LINE IDチェック
def check_line_id(request):
    line_id = request.GET.get("line_id")

    if line_id:
        return line_id
    else:
        redirect("line:index")


# サービス一覧
class ServiceView(View):
    def get(self, request, store_id):
        store = Store.objects.get(id=store_id)
        services = Service.objects.filter(store=store).order_by("-created_at")
        reservation_id = request.GET.get("reservation_id", None)
        line_id = check_line_id(request)

        return render(
            request,
            "line/service.html",
            {
                "services": services,
                "reservation_id": reservation_id,
                "line_id": line_id,
            },
        )


# スタッフ一覧
class StaffView(View):
    def get(self, request, service_id):
        staffs = Staff.objects.filter(services__id=service_id)
        reservation_id = request.GET.get("reservation_id", None)
        line_id = check_line_id(request)

        return render(
            request,
            "line/staff.html",
            {
                "staffs": staffs,
                "service_id": service_id,
                "reservation_id": reservation_id,
                "line_id": line_id,
            },
        )


# 予約不可日を取得
def get_disabled_dates(year, store, staff_id, week_dates):
    # 店舗の特別休日を取得
    store_holidays = StoreHoliday.objects.filter(holiday__year=year).values_list(
        "holiday", flat=True
    )

    store_holidays = [h.strftime("%Y-%m-%d") for h in store_holidays]

    # スタッフの休暇を取得
    staff_holidays = StaffHoliday.objects.filter(
        holiday__year=year, staff_id=staff_id
    ).values_list("holiday", flat=True)

    staff_holidays = [h.strftime("%Y-%m-%d") for h in staff_holidays]

    # 休日を取得
    day_mapping = {
        0: "closed_monday",
        1: "closed_tuesday",
        2: "closed_wednesday",
        3: "closed_thursday",
        4: "closed_friday",
        5: "closed_saturday",
        6: "closed_sunday",
    }

    weekday_holidays = set()
    for week_date in week_dates:
        day_of_week = week_date.weekday()
        if getattr(store, day_mapping[day_of_week]):
            weekday_holidays.add(week_date.strftime("%Y-%m-%d"))

    # 過去は予約不可
    today = datetime.now().date()
    past_dates = {
        week_date.strftime("%Y-%m-%d") for week_date in week_dates if week_date <= today
    }

    # 結合して、重複を削除
    disabled_dates = set(store_holidays).union(
        staff_holidays, weekday_holidays, past_dates
    )
    return disabled_dates


def get_week_dates(date):
    start_of_week = date - timedelta(days=date.weekday())
    return [start_of_week.date() + timedelta(days=i) for i in range(7)]


# 予約カレンダー
class CalendarView(View):
    def get(self, request, service_id, staff_id, year=None, week=None):
        reservation_id = request.GET.get("reservation_id", None)
        line_id = check_line_id(request)

        today = datetime.today()

        # 年と週を取得
        if year is None:
            year = today.year
        if week is None:
            week = today.isocalendar()[1]

        # サービス取得
        service = Service.objects.get(id=service_id)
        # スタッフ取得
        staff = Staff.objects.get(id=staff_id)

        first_day_of_year = datetime(year, 1, 1)
        if first_day_of_year.weekday() > 0:
            first_day_of_year -= timedelta(days=first_day_of_year.weekday())

        # 週の日付を取得
        current_date = first_day_of_year + timedelta(weeks=week - 1)
        week_dates = get_week_dates(current_date)

        # 営業時間を取得
        opening_time = service.store.open_time.hour
        closing_time = service.store.close_time.hour
        # 予約間隔
        interval = 30

        # 時間スロットを取得
        time_slots = [
            datetime(year, 1, 1, hour=h, minute=m).time()
            for h in range(opening_time, closing_time)
            for m in (0, interval)
        ]

        # 予約不可日を取得
        disabled_dates = get_disabled_dates(year, service.store, staff_id, week_dates)

        # 予約状況を取得
        availability = {}
        for week_date in week_dates:
            date_key = week_date.strftime("%Y-%m-%d")
            availability[date_key] = {}
            for time_slot in time_slots:
                time_key = time_slot.strftime("%H:%M")
                if str(week_date) in disabled_dates:
                    # 予約不可
                    availability[date_key][time_key] = True
                else:
                    # 予約可能
                    is_reserved = Reservation.objects.filter(
                        staff=staff,
                        reservation_date__date=week_date,
                        reservation_date__time=time_slot,
                    ).exists()
                    # 同じ時間帯ですでに予約済みの場合は予約不可
                    availability[date_key][time_key] = is_reserved

        return render(
            request,
            "line/calendar.html",
            {
                "service_id": service_id,
                "staff": staff,
                "week_dates": week_dates,
                "time_slots": time_slots,
                "current_year": year,
                "current_week": week,
                "current_month": current_date.month,
                "availability": availability,
                "reservation_id": reservation_id,
                "line_id": line_id,
            },
        )


# お客様情報入力
@method_decorator(csrf_exempt, name="dispatch")
class ReserveView(View):
    def get(self, request, service_id, staff_id, year, month, day, hour, minute):
        line_id = check_line_id(request)

        customer = Customer.objects.get(line_id=line_id)

        form = CustomerForm(instance=customer)

        return render(request, "line/reserve.html", {"form": form})

    def post(self, request, service_id, staff_id, year, month, day, hour, minute):
        reservation_id = request.GET.get("reservation_id", None)
        line_id = check_line_id(request)

        customer, created = Customer.objects.get_or_create(line_id=line_id)
        form = CustomerForm(request.POST, instance=customer)

        if form.is_valid():
            form.save()

            url = reverse(
                "line:confirm",
                args=[service_id, staff_id, year, month, day, hour, minute],
            )
            url += f"?line_id={line_id}"

            if reservation_id:
                url += f"&reservation_id={reservation_id}"

            return redirect(url)

        return render(request, "line/reserve.html", {"form": form})


# 予約内容確認
@method_decorator(csrf_exempt, name="dispatch")
class ConfirmView(View):
    def get(self, request, service_id, staff_id, year, month, day, hour, minute):
        check_line_id(request)

        service = Service.objects.get(id=service_id)
        staff = Staff.objects.get(id=staff_id)
        reservation_date = datetime(
            year=int(year),
            month=int(month),
            day=int(day),
            hour=int(hour),
            minute=int(minute),
        )

        return render(
            request,
            "line/confirm.html",
            {"service": service, "staff": staff, "reservation_date": reservation_date},
        )

    def post(self, request, service_id, staff_id, year, month, day, hour, minute):
        reservation_id = request.GET.get("reservation_id", None)
        line_id = check_line_id(request)

        service = Service.objects.get(id=service_id)
        store = service.store
        staff = Staff.objects.get(id=staff_id)
        customer = Customer.objects.get(line_id=line_id)

        reservation_date = datetime(
            year=int(year),
            month=int(month),
            day=int(day),
            hour=int(hour),
            minute=int(minute),
        )

        if reservation_id:
            reservation = Reservation.objects.get(id=reservation_id)
            reservation.service = service
            reservation.staff = staff
            reservation.customer = customer
            reservation.reservation_date = timezone.make_aware(reservation_date)
            reservation.save()
        else:
            Reservation.objects.create(
                service=service,
                staff=staff,
                customer=customer,
                reservation_date=timezone.make_aware(reservation_date),
            )

        # 予約確定メッセージ送信
        send_reservation_confirm_message(
            line_id, reservation_id, reservation_date, store, service, staff
        )

        return redirect("line:done")


class DoneView(View):
    def get(self, request):
        return render(request, "line/done.html")
