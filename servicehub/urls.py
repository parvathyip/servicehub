"""
URL configuration for servicehub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from servicehub_app import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('users-login/',views.users_login),
    #admin
    path('admin-dashboard/',views.admin_dashboard),
    path('admin-addbrand/',views.admin_addbrand),
    path('admin-approvehub/',views.admin_approvehub),
    path('admin-approveeachhub/',views.admin_approveeachhub),
    path('admin-rejecteachhub/',views.admin_rejecteachhub),
    path('admin-viewapprovedhubs/',views.admin_viewapprovedhubs),
    path('admin-viewsinglehub/',views.admin_viewsinglehub),
    path('admin-updatebrand/',views.admin_updatebrand),
    path('admin-deletebrand/',views.admin_deletebrand),
    path('admin-message/',views.admin_message),
    path('admin-hubchat/',views.admin_hubchat),
    path('admin-viewusers/',views.admin_viewusers),
    path('admin-viewsingleuser/',views.admin_viewsingleuser),
    path('admin-deleteuser/',views.admin_deleteuser),
    path('admin-viewpayments/',views.admin_viewpayments),
    path('admin-viewmorecomplaintdetail/',views.admin_viewmorecomplaintdetail),
    #servicehub
    path('servicehub-signup/',views.servicehub_signup),
    path('hub-dashboard/',views.hub_dashboard),
    path('hub-addserviceproducts/',views.hub_addserviceproducts),
    path('hub-deleteservice/',views.hub_deleteservice),
    path('hub-viewtroubleshoots/',views.hub_viewtroubleshoots),
    path('hub-chat/',views.hub_chat),
    path('hub-viewcomplaints/',views.hub_viewcomplaints),
    path('hub-acceptcomplaint/',views.hub_acceptcomplaint),
    path('hub-rejectcomplaint/',views.hub_rejectcomplaint),
    path('hub-addcharge/',views.hub_addcharge),
    path('hub-viewmorecomplaintdetail/',views.hub_viewmorecomplaintdetail),
    path('hub-completecomplaint/',views.hub_completecomplaint),
    path('hub-viewcompletedworks/',views.hub_viewcompletedworks),
    path('hub-addfaq/',views.hub_addfaq),
    path('hub-viewfaq/',views.hub_viewfaq),
    path('hub-deletefaq/',views.hub_deletefaq),
    path('hub-viewprofile/',views.hub_viewprofile),
    path('hub-updateprofile/',views.hub_updateprofile),
    # path('hub-deleteprofile/',views.hub_deleteprofile),
    path('hub-adminchat/',views.hub_adminchat),
    #user
    path('user-signup/',views.user_signup),
    path('user-dashboard/',views.user_dashboard),
    path('user-viewcompany/',views.user_viewcompany),
    path('user-viewhubs/',views.user_viewhubs),
    path('user-viewhubsbybrand/',views.user_viewhubsbybrand),
    path('user-viewsinglehub/',views.user_viewsinglehub),
    path('user-viewfaq/',views.user_viewfaq),
    path('users-viewtroubleshootchat/',views.users_viewtroubleshootchat),
    path('user-deletecomplaint/',views.user_deletecomplaint),
    path('user-chat/',views.user_chat),
    path('user-viewcomplaints/',views.user_viewcomplaints),
    path('user-acceptsubmitdate/',views.user_acceptsubmitdate),
    path('user-rejectsubmitdate/',views.user_rejectsubmitdate),
    path('user-viewmorecomplaintdetail/',views.user_viewmorecomplaintdetail),
    path('user-payment/',views.user_payment),
    path('user-addcarddetails/',views.user_addcarddetails),
    path('user-viewhistory/',views.user_viewhistory),
    path('user-addfeedback/',views.user_addfeedback),
    path('user-viewprofile/',views.user_viewprofile),
    path('user-updateprofile/',views.user_updateprofile),
    path('getproductname/', views.getproductname, name='getproductname'),
]
