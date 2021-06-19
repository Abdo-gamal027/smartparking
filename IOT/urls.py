from django.contrib import admin
from django.urls import path
from register import views as v
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', v.home, name="home"),
    path('register/', v.register, name="register"),
    path('card_validator/', v.validator, name="validator"),
    path('login/', v.loginpage, name="login"),
    path('logout/', v.logoutuser, name="logout"),
    path('location/', v.loc, name="location"),
    path('location/index.html/', v.sel, name="select"),
    path('location/index.html/email.html', v.email, name="email"),

]
