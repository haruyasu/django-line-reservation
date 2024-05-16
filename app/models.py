from django.db import models

from accounts.models import UserAccount


# 店舗
class Store(models.Model):
    name = models.CharField(verbose_name="店舗名", max_length=100)
    address = models.CharField(
        verbose_name="住所", max_length=100, null=True, blank=True
    )
    tel = models.CharField(
        verbose_name="電話番号", max_length=100, null=True, blank=True
    )
    description = models.TextField(verbose_name="詳細", null=True, blank=True)
    image = models.ImageField(
        upload_to="reservation/store", verbose_name="画像", null=True, blank=True
    )
    open_time = models.TimeField(verbose_name="開店時間", default="09:00:00")
    close_time = models.TimeField(verbose_name="閉店時間", default="21:00:00")

    closed_monday = models.BooleanField(verbose_name="月曜定休", default=False)
    closed_tuesday = models.BooleanField(verbose_name="火曜定休", default=False)
    closed_wednesday = models.BooleanField(verbose_name="水曜定休", default=False)
    closed_thursday = models.BooleanField(verbose_name="木曜定休", default=False)
    closed_friday = models.BooleanField(verbose_name="金曜定休", default=False)
    closed_saturday = models.BooleanField(verbose_name="土曜定休", default=False)
    closed_sunday = models.BooleanField(verbose_name="日曜定休", default=False)

    updated_at = models.DateTimeField("更新日", auto_now=True)
    created_at = models.DateTimeField("作成日", auto_now_add=True)

    def get_closed_days(self):
        days = []
        if self.closed_monday:
            days.append("月曜")
        if self.closed_tuesday:
            days.append("火曜")
        if self.closed_wednesday:
            days.append("水曜")
        if self.closed_thursday:
            days.append("木曜")
        if self.closed_friday:
            days.append("金曜")
        if self.closed_saturday:
            days.append("土曜")
        if self.closed_sunday:
            days.append("日曜")
        return ", ".join(days) if days else "なし"

    class Meta:
        verbose_name = "店舗"
        verbose_name_plural = "店舗"

    def __str__(self):
        return self.name


# サービス
class Service(models.Model):
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, verbose_name="店舗", related_name="services"
    )
    name = models.CharField(max_length=255, verbose_name="名前")
    duration = models.FloatField(verbose_name="所要時間")
    price = models.IntegerField(verbose_name="料金")
    description = models.TextField(verbose_name="詳細")
    image = models.ImageField(
        upload_to="reservation/service", verbose_name="画像", blank=True, null=True
    )

    updated_at = models.DateTimeField("更新日", auto_now=True)
    created_at = models.DateTimeField("作成日", auto_now_add=True)

    class Meta:
        verbose_name = "サービス"
        verbose_name_plural = "サービス"

    def __str__(self):
        return self.name


# スタッフ
class Staff(models.Model):
    user = models.OneToOneField(
        UserAccount,
        on_delete=models.CASCADE,
        related_name="staff_profile",
        verbose_name="アカウント",
    )
    services = models.ManyToManyField(
        Service, verbose_name="サービス", related_name="staff"
    )
    position = models.CharField(max_length=100, verbose_name="職位", default="未設定")
    nomination_fee = models.IntegerField(verbose_name="指名料", default=0)
    bio = models.TextField(verbose_name="自己紹介", blank=True, null=True)
    image = models.ImageField(
        upload_to="reservation/staff", verbose_name="画像", blank=True, null=True
    )

    updated_at = models.DateTimeField("更新日", auto_now=True)
    created_at = models.DateTimeField("作成日", auto_now_add=True)

    class Meta:
        verbose_name = "スタッフ"
        verbose_name_plural = "スタッフ"

    def __str__(self):
        return self.user.name


# 顧客
class Customer(models.Model):
    GENDER_CHOICES = (
        ("male", "男性"),
        ("female", "女性"),
        ("other", "その他"),
    )

    name = models.CharField(max_length=255, verbose_name="名前")
    gender = models.CharField(
        max_length=10,
        verbose_name="性別",
        choices=GENDER_CHOICES,
        blank=True,
        null=True,
    )
    phone_number = models.CharField(
        max_length=15, verbose_name="電話番号", blank=True, null=True
    )
    line_id = models.CharField(max_length=255, unique=True, verbose_name="LINE ID")

    updated_at = models.DateTimeField("更新日", auto_now=True)
    created_at = models.DateTimeField("作成日", auto_now_add=True)

    class Meta:
        verbose_name = "顧客"
        verbose_name_plural = "顧客"

    def __str__(self):
        return self.name


# 予約
class Reservation(models.Model):
    service = models.ForeignKey(
        Service, verbose_name="サービス", on_delete=models.CASCADE
    )
    staff = models.ForeignKey(Staff, verbose_name="スタッフ", on_delete=models.CASCADE)
    customer = models.ForeignKey(
        Customer, verbose_name="お客様情報", on_delete=models.CASCADE
    )
    reservation_date = models.DateTimeField(verbose_name="予約日時")

    updated_at = models.DateTimeField("更新日", auto_now=True)
    created_at = models.DateTimeField("作成日", auto_now_add=True)

    class Meta:
        verbose_name = "予約"
        verbose_name_plural = "予約"

    def __str__(self):
        return f"{self.reservation_date.strftime('%Y-%m-%d %H:%M')} - {self.customer.name} - {self.service.name} by {self.staff.user.name if self.staff else '指定なし'}"


# 店舗特別休日
class StoreHoliday(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, verbose_name="店舗")
    holiday = models.DateField(verbose_name="休業日")
    reason = models.CharField(max_length=255, verbose_name="理由", blank=True)
    updated_at = models.DateTimeField("更新日", auto_now=True)
    created_at = models.DateTimeField("作成日", auto_now_add=True)

    class Meta:
        verbose_name = "店舗休業日"
        verbose_name_plural = "店舗休業日"

    def __str__(self):
        return f"{self.holiday} - {self.reason}"


# スタッフ休日
class StaffHoliday(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, verbose_name="スタッフ")
    holiday = models.DateField(verbose_name="休日")
    reason = models.CharField(max_length=255, verbose_name="理由", blank=True)
    updated_at = models.DateTimeField("更新日", auto_now=True)
    created_at = models.DateTimeField("作成日", auto_now_add=True)

    class Meta:
        verbose_name = "スタッフ休日"
        verbose_name_plural = "スタッフ休日"

    def __str__(self):
        return f"{self.staff.user.name} - {self.holiday} - {self.reason}"
