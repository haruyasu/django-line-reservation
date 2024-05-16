from django.conf import settings
from django.utils import timezone

from linebot import LineBotApi
from linebot.models import (
    FlexSendMessage,
)

line_bot_api = LineBotApi(settings.CHANNEL_ACCESS_TOKEN)


# 予約確定
def send_reservation_confirm_message(
    line_id, reservation_id, reservation_date, store, service, staff
):
    content_json = {
        "type": "flex",
        "altText": "予約変更しました" if reservation_id else "予約完了しました",
        "contents": {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "flex": 0,
                "contents": [
                    {
                        "type": "text",
                        "text": "予約変更" if reservation_id else "予約完了",
                        "weight": "bold",
                        "align": "center",
                        "contents": [],
                    }
                ],
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "日付",
                                    },
                                    {
                                        "type": "text",
                                        "text": reservation_date.strftime(
                                            "%Y年%m月%d日"
                                        ),
                                        "align": "end",
                                    },
                                ],
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "時間",
                                    },
                                    {
                                        "type": "text",
                                        "text": reservation_date.strftime("%H:%M"),
                                        "align": "end",
                                    },
                                ],
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "店舗",
                                    },
                                    {
                                        "type": "text",
                                        "text": store.name,
                                        "align": "end",
                                    },
                                ],
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "住所",
                                    },
                                    {
                                        "type": "text",
                                        "text": store.address,
                                        "align": "end",
                                    },
                                ],
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "電話番号",
                                    },
                                    {
                                        "type": "text",
                                        "text": store.tel,
                                        "align": "end",
                                    },
                                ],
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "サービス",
                                    },
                                    {
                                        "type": "text",
                                        "text": service.name,
                                        "align": "end",
                                    },
                                ],
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "スタッフ",
                                    },
                                    {
                                        "type": "text",
                                        "text": staff.user.name,
                                        "align": "end",
                                    },
                                ],
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "お支払金額",
                                    },
                                    {
                                        "type": "text",
                                        "text": (
                                            f"{service.price + staff.nomination_fee}円"
                                        ),
                                        "align": "end",
                                    },
                                ],
                            },
                        ],
                    }
                ],
            },
        },
    }

    result = FlexSendMessage.new_from_json_dict(content_json)

    line_bot_api.push_message(line_id, messages=result)


# 予約がある場合
def send_menu_message(line_id):
    content_json = {
        "type": "flex",
        "altText": "メニューを選択してください",
        "contents": {
            "type": "bubble",
            "direction": "ltr",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "メニューを選択してください",
                        "align": "center",
                        "contents": [],
                    }
                ],
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "予約確認",
                            "text": "予約確認",
                        },
                        "style": "primary",
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "予約変更",
                            "text": "予約変更",
                        },
                        "style": "primary",
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "予約キャンセル",
                            "text": "予約キャンセル",
                        },
                        "style": "secondary",
                    },
                ],
            },
        },
    }

    result = FlexSendMessage.new_from_json_dict(content_json)

    line_bot_api.push_message(line_id, messages=result)


# 予約がない場合
def send_new_menu_message(line_id):
    content_json = {
        "type": "flex",
        "altText": "メニューを選択してください",
        "contents": {
            "type": "bubble",
            "direction": "ltr",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "新規予約",
                        "align": "center",
                        "contents": [],
                    }
                ],
            },
            "body": {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "uri",
                            "label": "予約メニュー",
                            "uri": "https://liff.line.me/2004759968-qEJg32MP",
                        },
                        "style": "primary",
                    }
                ],
            },
        },
    }

    result = FlexSendMessage.new_from_json_dict(content_json)

    line_bot_api.push_message(line_id, messages=result)


# 予約確認
def send_check_reservation_message(line_id, reservations):
    content_json = {
        "type": "flex",
        "altText": "予約確認",
        "contents": {
            "type": "bubble",
            "direction": "ltr",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "確認したい予約を選択してください",
                        "align": "center",
                        "contents": [],
                    }
                ],
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [],
            },
        },
    }

    buttons = []
    for reservation in reservations:
        local_date = timezone.localtime(reservation.reservation_date)
        button = {
            "type": "button",
            "action": {
                "type": "postback",
                "label": local_date.strftime("%Y年%m月%d日 %H:%M"),
                "text": local_date.strftime("%Y年%m月%d日 %H:%M"),
                "data": f"action=予約確認&reservation_id={reservation.id}",
            },
            "style": "primary",
        }
        buttons.append(button)

    content_json["contents"]["body"]["contents"] = buttons

    result = FlexSendMessage.new_from_json_dict(content_json)

    line_bot_api.push_message(line_id, messages=result)


# 予約確認詳細
def send_check_reservation_detail_message(line_id, reservation):
    local_date = timezone.localtime(reservation.reservation_date)

    content_json = {
        "type": "flex",
        "altText": "予約確認",
        "contents": {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "flex": 0,
                "contents": [
                    {
                        "type": "text",
                        "text": "予約確認",
                        "weight": "bold",
                        "align": "center",
                        "contents": [],
                    }
                ],
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "日付",
                                    },
                                    {
                                        "type": "text",
                                        "text": local_date.strftime("%Y年%m月%d日"),
                                        "align": "end",
                                    },
                                ],
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "時間",
                                    },
                                    {
                                        "type": "text",
                                        "text": local_date.strftime("%H:%M"),
                                        "align": "end",
                                    },
                                ],
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "店舗",
                                    },
                                    {
                                        "type": "text",
                                        "text": reservation.service.store.name,
                                        "align": "end",
                                    },
                                ],
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "住所",
                                    },
                                    {
                                        "type": "text",
                                        "text": reservation.service.store.address,
                                        "align": "end",
                                    },
                                ],
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "電話番号",
                                    },
                                    {
                                        "type": "text",
                                        "text": reservation.service.store.tel,
                                        "align": "end",
                                    },
                                ],
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "サービス",
                                    },
                                    {
                                        "type": "text",
                                        "text": reservation.service.name,
                                        "align": "end",
                                    },
                                ],
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "スタッフ",
                                    },
                                    {
                                        "type": "text",
                                        "text": (
                                            reservation.staff.user.name
                                            if reservation.staff
                                            else "指定なし"
                                        ),
                                        "align": "end",
                                    },
                                ],
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "お支払金額",
                                    },
                                    {
                                        "type": "text",
                                        "text": (
                                            f"{reservation.service.price + reservation.staff.nomination_fee}円"
                                            if reservation.staff
                                            else f"{reservation.service.price}円"
                                        ),
                                        "align": "end",
                                    },
                                ],
                            },
                        ],
                    }
                ],
            },
        },
    }

    result = FlexSendMessage.new_from_json_dict(content_json)

    line_bot_api.push_message(line_id, messages=result)


# 予約変更
def send_change_reservation_message(line_id, reservations):
    content_json = {
        "type": "flex",
        "altText": "予約変更",
        "contents": {
            "type": "bubble",
            "direction": "ltr",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "変更したい予約を選択してください",
                        "align": "center",
                        "contents": [],
                    }
                ],
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [],
            },
        },
    }

    buttons = []
    for reservation in reservations:
        local_date = timezone.localtime(reservation.reservation_date)

        button = {
            "type": "button",
            "action": {
                "type": "uri",
                "label": local_date.strftime("%Y年%m月%d日 %H:%M"),
                "uri": f"https://liff.line.me/{settings.LIFF_ID}?reservation_id={reservation.id}",
            },
            "style": "primary",
        }
        buttons.append(button)

    content_json["contents"]["body"]["contents"] = buttons

    result = FlexSendMessage.new_from_json_dict(content_json)

    line_bot_api.push_message(line_id, messages=result)


# 予約キャンセル
def send_cancel_reservation_message(line_id, reservations):
    content_json = {
        "type": "flex",
        "altText": "予約キャンセル",
        "contents": {
            "type": "bubble",
            "direction": "ltr",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "キャンセルしたい予約を選択してください",
                        "align": "center",
                        "contents": [],
                    }
                ],
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [],
            },
        },
    }

    buttons = []
    for reservation in reservations:
        local_date = timezone.localtime(reservation.reservation_date)

        button = {
            "type": "button",
            "action": {
                "type": "postback",
                "label": local_date.strftime("%Y年%m月%d日 %H:%M"),
                "text": local_date.strftime("%Y年%m月%d日 %H:%M"),
                "data": f"action=予約キャンセル&reservation_id={reservation.id}",
            },
            "style": "secondary",
        }
        buttons.append(button)

    content_json["contents"]["body"]["contents"] = buttons

    result = FlexSendMessage.new_from_json_dict(content_json)

    line_bot_api.push_message(line_id, messages=result)
