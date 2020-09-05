from django.urls import path
from django.contrib.auth import views as auth_views
from myapp import views
app_name = 'myapp'
urlpatterns = [
 path(r'', views.index, name='index'),

 path(r'about/', views.about, name='about'),
 path(r'courses/',views.courses,name='courses'),
 path(r'courses/<cour_id>/', views.coursedetail, name='coursedetail'),
 path(r'place_order/',views.place_order,name='placeorder'),
 path(r'order_response/',views.order_response,name='order_response'),
 path(r'login/',views.user_login,name='user_login'),
 path(r'logout/',views.user_logout,name='user_logout'),
 path(r'register/',views.register, name='register'),
 path(r'reset_password/',auth_views.PasswordResetView.as_view(), name="reset_password"),
 path(r'reset_password_sent/',auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
 path(r'reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
 path(r'reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
 path(r'myaccount/', views.myaccount, name='myaccount'),
 path(r'<top_no>/', views.detail, name='detail')
]
