from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # トップページ
    path("", include("app.urls")),
    # アカウント認証
    path("accounts/", include("accounts.urls")),
    # 認証ライブラリ
    path("accounts/", include("allauth.urls")),
    # LINE
    path("line/", include("line.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
