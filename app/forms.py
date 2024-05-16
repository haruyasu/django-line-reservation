from django import forms

from app.models import Service, Staff, StaffHoliday, Store, StoreHoliday


class StoreRegisterForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = [
            "name",
            "address",
            "tel",
            "description",
            "image",
            "open_time",
            "close_time",
            "closed_monday",
            "closed_tuesday",
            "closed_wednesday",
            "closed_thursday",
            "closed_friday",
            "closed_saturday",
            "closed_sunday",
        ]

        widgets = {
            "open_time": forms.TimeInput(attrs={"type": "time"}),
            "close_time": forms.TimeInput(attrs={"type": "time"}),
        }


class ServiceRegisterForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ["store", "name", "duration", "price", "description", "image"]


class StoreHolidayForm(forms.ModelForm):
    class Meta:
        model = StoreHoliday
        fields = ["store", "holiday", "reason"]
        widgets = {
            "holiday": forms.DateInput(attrs={"type": "date"}),
        }


class ProfileEditForm(forms.ModelForm):
    name = forms.CharField(max_length=255, required=False, label="名前")

    class Meta:
        model = Staff
        fields = ["position", "nomination_fee", "bio", "image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields["name"].initial = self.instance.user.name

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.user.name = self.cleaned_data["name"]
            instance.user.save()
            instance.save()
        return instance


class StaffHolidayForm(forms.ModelForm):
    class Meta:
        model = StaffHoliday
        fields = ["holiday", "reason"]
        widgets = {
            "holiday": forms.DateInput(attrs={"type": "date"}),
        }
