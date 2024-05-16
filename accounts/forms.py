from allauth.account.forms import SignupForm
from django import forms


# アカウント登録フォーム
class SignupUserForm(SignupForm):
    # 名前入力フォーム
    name = forms.CharField(max_length=255, label="名前")

    def save(self, request):
        # ログインユーザー取得
        user = super(SignupUserForm, self).save(request)
        # 名前を保存
        user.name = self.cleaned_data["name"]
        user.save()
        return user
