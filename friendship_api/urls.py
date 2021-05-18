import debug_toolbar
from django.contrib import admin
from django.urls import include, path

api_urlpatterns = [
    path('users/', include(('users.api.urls', 'users'), namespace='users'), name='users'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('api/', include(api_urlpatterns)),
]
