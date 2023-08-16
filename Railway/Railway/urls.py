from django.contrib import admin
from django.urls import path, include
from myApp.views import user_view_trains, view_trains

app_name = 'myApp'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user-view-trains/', user_view_trains, name='user-view-trains'),
    path('view-trains/', view_trains, name='view-trains'),
    path('', include('myApp.urls')),
]
