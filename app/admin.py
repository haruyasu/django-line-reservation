from django.contrib import admin

from .models import (
    Customer,
    Reservation,
    Service,
    Staff,
    StaffHoliday,
    Store,
    StoreHoliday,
)


class StoreCustom(admin.ModelAdmin):
    # 一覧
    list_display = (
        "id",
        "name",
        "address",
        "tel",
        "open_time",
        "close_time",
        "created_at",
    )
    # 順番
    ordering = ("created_at",)
    list_display_links = ("id", "name")


class ServiceCustom(admin.ModelAdmin):
    # 一覧
    list_display = ("id", "store", "name", "duration", "price", "created_at")
    # 順番
    ordering = ("created_at",)
    list_display_links = ("id", "store", "name")


class StaffCustom(admin.ModelAdmin):
    # 一覧
    list_display = ("id", "user", "created_at")
    # 順番
    ordering = ("created_at",)
    list_display_links = ("id", "user")


class CustomerCustom(admin.ModelAdmin):
    # 一覧
    list_display = ("id", "name", "created_at")
    # 順番
    ordering = ("created_at",)
    list_display_links = ("id", "name")


class ReservationCustom(admin.ModelAdmin):
    # 一覧
    list_display = (
        "id",
        "service",
        "staff",
        "customer",
        "reservation_date",
        "updated_at",
        "created_at",
    )
    # 順番
    ordering = ("updated_at",)
    list_display_links = ("id", "service", "staff", "customer", "reservation_date")


class StoreHolidayCustom(admin.ModelAdmin):
    # 一覧
    list_display = ("id", "store", "holiday", "reason", "created_at")
    # 順番
    ordering = ("store", "holiday")
    list_display_links = ("id", "store", "holiday")


class StaffHolidayCustom(admin.ModelAdmin):
    # 一覧
    list_display = ("id", "staff", "holiday", "reason", "created_at")
    # 順番
    ordering = ("holiday",)
    list_display_links = ("id", "staff", "holiday")


admin.site.register(Store, StoreCustom)
admin.site.register(Service, ServiceCustom)
admin.site.register(Staff, StaffCustom)
admin.site.register(Customer, CustomerCustom)
admin.site.register(Reservation, ReservationCustom)
admin.site.register(StoreHoliday, StoreHolidayCustom)
admin.site.register(StaffHoliday, StaffHolidayCustom)
