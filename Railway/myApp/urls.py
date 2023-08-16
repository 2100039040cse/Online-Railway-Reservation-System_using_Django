# from . import views
# from django.urls import path


# app_name = 'myApp'

# urlpatterns = [
#     path("", views.home, name="home"),
#     path('user-login/', views.user_login, name='user-login'),
#     path('user-home/', views.user_home, name='user_home'),
#     path('user-register/', views.user_register, name='user-register'),
#     path("admin-login/", views.admin_login, name="admin-login"),
#     path("admin-home/", views.admin_home, name="admin-home"),
#     path("admin-search-train/", views.admin_search_train, name="admin-search-train"),
#     path("view-trains/", views.view_trains, name="view-trains"),
#     path("add-trains/", views.add_trains, name="add-trains"),
#     path("admin-update-train/", views.admin_update_train, name="admin-update-train"),
#     path("cancle-train/", views.cancle_train, name="cancle-train"),
#     path("my-bookings/", views.my_bookings, name='my-bookings'),
#     path("pnr-status/", views.pnr_status, name='pnr-status'),
#     path("avail-ability/", views.avail_ability, name="avail-ability"),
#     path("user-home/", views.user_home, name="user-home"),
#     path("user-profile/", views.user_profile, name="user-profile"),
#     path("admin-super-login/", views.admin_super_login, name="admin-super-login"),
#     path("admin-add-train/", views.admin_add_train, name="admin-add-train"),
#     path('admin-cancel-train/', views.admin_cancel_train, name='admin-cancel-train'),
#     path("admin-view-trains/", views.admin_view_trains, name="admin-view-trains"),
#     path("user-view-trains/", views.user_view_trains, name="user-view-trains"),
#     path("user-confirm-train/<int:train_id>/", views.user_confirm_train, name="user-confirm-train"),
#     path('user-payment/<int:train_id>/', views.user_payment_view, name='user-payment-view'),
#     path('user-payment-type/<int:train_id>/', views.user_payment_type, name='user-payment-type'),
#     path("user-confirm-train/<int:train_id>/", views.user_confirm_train, name="user-confirm-train"),

#     path('payment-status/<int:train_id>/', views.payment_status, name='payment-status'),
    
# ]
from django.urls import path
from . import views

app_name = 'myApp'

urlpatterns = [
    path("", views.home, name="home"),
    path('user-login/', views.user_login, name='user-login'),
    path('user-home/', views.user_home, name='user_home'),
    path('user-register/', views.user_register, name='user-register'),
    path("admin-login/", views.admin_login, name="admin-login"),
    path("admin-home/", views.admin_home, name="admin-home"),
    path("admin-search-train/", views.admin_search_train, name="admin-search-train"),
    path("view-trains/", views.view_trains, name="view-trains"),
    path("add-trains/", views.add_trains, name="add-trains"),
    path("admin-update-train/", views.admin_update_train, name="admin-update-train"),
    path("cancle-train/", views.cancle_train, name="cancle-train"),
    path("my-bookings/", views.my_bookings, name='my-bookings'),
    path("pnr-status/", views.pnr_status, name='pnr-status'),
    path("avail-ability/", views.avail_ability, name="avail-ability"),
    path("user-home/", views.user_home, name="user-home"),
    path("user-profile/", views.user_profile, name="user-profile"),
    path("admin-super-login/", views.admin_super_login, name="admin-super-login"),
    path("admin-add-train/", views.admin_add_train, name="admin-add-train"),
    path('admin-cancel-train/', views.admin_cancel_train, name='admin-cancel-train'),
    path("admin-view-trains/", views.admin_view_trains, name="admin-view-trains"),
    path("user-view-trains/", views.user_view_trains, name="user-view-trains"),
    path("user-confirm-train/", views.user_confirm_train, name="user-confirm-train"),
    path('user-payment/', views.user_payment, name='user-payment'),
    path('user-payment-type/', views.user_payment_type, name='user-payment-type'),
    path("payment-status/", views.payment_status, name='payment-status'), 
    path('user-payment-view/', views.user_payment_view, name='user-payment-view'),
]

