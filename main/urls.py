from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include("accounts.urls")),
    path('groups/', include("groups.urls")),
    path('groups/statistics/', include("group_statistics.urls")),
]
