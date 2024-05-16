from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from app.forms import (
    StoreRegisterForm,
    ServiceRegisterForm,
    StoreHolidayForm,
    ProfileEditForm,
    StaffHolidayForm,
)
from app.models import Reservation, Service, Staff, StaffHoliday, Store, StoreHoliday


# 店舗一覧
class IndexView(View):
    def get(self, request):
        stores = Store.objects.all().order_by("-created_at")

        return render(request, "app/index.html", {"stores": stores})


# 店舗詳細
class StoreDetailView(View):
    def get(self, request, store_id):
        store = Store.objects.get(id=store_id)
        services = store.services.all().order_by("-created_at")
        has_staff_profile = hasattr(request.user, "staff_profile")

        if has_staff_profile:
            staff = request.user.staff_profile
            staff_services = staff.services.all()
            services_status = {
                service.id: service in staff_services for service in services
            }
        else:
            services_status = {}

        return render(
            request,
            "app/store_detail.html",
            {
                "store": store,
                "services": services,
                "services_status": services_status,
                "has_staff_profile": has_staff_profile,
            },
        )

    def post(self, request, store_id, service_id):
        staff = request.user.staff_profile
        service = Service.objects.get(id=service_id)
        action = request.POST.get("action")

        if action == "assign":
            if service not in staff.services.all():
                staff.services.add(service)
        elif action == "remove":
            if service in staff.services.all():
                staff.services.remove(service)

        return redirect("app:store_detail", store_id=store_id)


# 管理者チェック
def check_superuser(request):
    if not request.user.is_superuser:
        return redirect("app:index")


# 店舗登録
class StoreRegisterView(LoginRequiredMixin, View):
    def get(self, request):
        check_superuser(request)

        form = StoreRegisterForm()

        return render(request, "app/store_register.html", {"form": form})

    def post(self, request):
        check_superuser(request)

        form = StoreRegisterForm(request.POST)

        if form.is_valid():
            store = Store()
            store.name = form.cleaned_data["name"]
            store.address = form.cleaned_data["address"]
            store.tel = form.cleaned_data["tel"]
            store.description = form.cleaned_data["description"]
            if request.FILES:
                store.image = request.FILES.get("image")
            store.save()

            return redirect("app:index")

        return render(request, "app/store_register.html", {"form": form})


# サービス登録
class ServiceRegisterView(LoginRequiredMixin, View):
    def get(self, request):
        check_superuser(request)

        form = ServiceRegisterForm()

        return render(request, "app/service_register.html", {"form": form})

    def post(self, request):
        check_superuser(request)

        form = ServiceRegisterForm(request.POST, request.FILES)

        if form.is_valid():
            service = form.save()
            url = reverse("app:store_detail", args=[service.store.id])

            return redirect(url)

        return render(request, "app/service_register.html", {"form": form})


# 店舗特別休日登録
class StoreHolidayView(LoginRequiredMixin, View):
    def get(self, request):
        check_superuser(request)

        form = StoreHolidayForm()
        store_holidays = StoreHoliday.objects.all().order_by("store", "-holiday")

        return render(
            request,
            "app/store_holiday.html",
            {"form": form, "store_holidays": store_holidays},
        )

    def post(self, request):
        check_superuser(request)

        form = StoreHolidayForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("app:store_holiday")

        store_holidays = StoreHoliday.objects.all().order_by("store", "-holiday")

        return render(
            request,
            "app/store_holiday.html",
            {"form": form, "store_holidays": store_holidays},
        )


# プロフィール
class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        staff, created = Staff.objects.get_or_create(user=request.user)
        form = ProfileEditForm(instance=staff)

        return render(request, "app/profile.html", {"form": form})

    def post(self, request):
        staff, created = Staff.objects.get_or_create(user=request.user)
        form = ProfileEditForm(request.POST, request.FILES, instance=staff)

        if form.is_valid():
            form.save()
            return redirect("app:index")

        return render(request, "app/profile.html", {"form": form})


# 予約一覧
class ReservationView(LoginRequiredMixin, View):
    def get(self, request):
        staff = Staff.objects.filter(user=request.user)

        reservations = []

        if staff.exists():
            staff = staff.first()
            reservations = Reservation.objects.filter(staff=staff).order_by(
                "-reservation_date"
            )

        return render(request, "app/reservation.html", {"reservations": reservations})


# スタッフ休日登録
class StaffHolidayView(LoginRequiredMixin, View):
    def get(self, request):
        form = StaffHolidayForm()
        staff = request.user.staff_profile
        staff_holidays = StaffHoliday.objects.filter(staff=staff).order_by("-holiday")

        return render(
            request,
            "app/staff_holiday.html",
            {"form": form, "staff_holidays": staff_holidays},
        )

    def post(self, request):
        form = StaffHolidayForm(request.POST)
        staff = request.user.staff_profile

        if form.is_valid():
            holiday = form.save(commit=False)
            holiday.staff = staff
            holiday.save()

            return redirect("app:staff_holiday")

        staff_holidays = StaffHoliday.objects.filter(staff=staff).order_by("-holiday")

        return render(
            request,
            "app/staff_holiday.html",
            {"form": form, "staff_holidays": staff_holidays},
        )
