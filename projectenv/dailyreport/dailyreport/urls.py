"""dailyreport URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from django.views.generic import TemplateView
from dailyapp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',TemplateView.as_view(template_name='login.html')),
    path('user_login/',views.user_login,name='user_login'),
    path('admin_page/',views.admin_page,name='admin_page'),
    path('index/',views.index,name='index'),
    path('note/',views.note,name='note'),
    path('add_dept/',views.add_dept,name='add_dept'),
    path('save_dept/',views.save_dept,name='save_dept'),
    path('add_des/',views.add_des,name='add_des'),
    path('save_des/',views.save_des,name='save_des'),
    path('add_login/',views.add_login,name='add_login'),
    path('loginoption/',views.option_ajax,name='option_ajax'),
    path('save_login/',views.save_login,name='save_login'),
    path('change_pwd/',views.change_pwd,name='change_pwd'),
    path('save_changep/',views.save_changep,name='save_changep'),
    path('task/',views.task,name='task'),
    path('create_task/',views.create_task,name='create_task'),
    path('create_user_group/',views.create_user_group,name='create_user_group'),
    path('assign_grp/',views.assign_grp,name='assign_grp'),
    path('save_user_group/',views.save_user_group,name='save_user_group'),
    path('save_emp_grp/',views.save_emp_grp,name='save_emp_grp'),
    path('admin_tassign/',views.admin_tassign,name='admin_tassign'),
    path('save_admin_tassign/',views.save_admin_tassign,name='save_admin_tassign'),
    path('assign_task/',views.assign_task,name='assign_task'),
    path('d_activity/',views.d_activity,name='d_activity'),
    path('enquiry_details/',views.enquiry_details,name='enquiry_details'),
    path('appointment_details/',views.appointment_details,name='appointment_details'),
    path('emp_details/',views.emp_details,name='emp_details'),
    path('domestic_customer/',views.domestic_customer,name='domestic_customer'),
    path('business_customer/',views.business_customer,name='business_customer'),
    path('createnote/',views.createnote,name='createnote'), 
    path('save_daily_activity/',views.save_daily_activity,name='save_daily_activity'),
    path('save_enquiry/',views.save_enquiry,name='save_enquiry'),
    path('save_appointment/',views.save_appointment,name='save_appointment'),
    path('save_emp/',views.save_emp,name='save_emp'),
    path('save_domestic/',views.save_domestic,name='save_domestic'),
    path('save_business/',views.save_business,name='save_business'),
    path('save_task/',views.save_task,name='save_task'),
    path('save_assign_task/',views.save_assign_task,name='save_assign_task'),
    path('save_note/',views.save_note,name='save_note'),
    path('test/',views.test,name='test'),
    path('lgout/',views.lgout,name='lgout'),
    path('request_resource/',views.request_resource,name='request_resource'),
    path('save_request/',views.save_request,name='save_request'),
    path('request_list/',views.request_list,name='request_list'),
    path('rapprove/<int:id>',views.rapprove,name='rapprove'),
    path('rreject/<int:id>',views.rreject,name='rreject'),
    path('view_rstatus/',views.view_rstatus,name='view_rstatus'),
    path('view_cust_details/',views.view_cust_details,name='view_cust_details'),
    path('view_status/',views.view_status,name='view_status'),
    path('view_app/',views.view_app,name='view_app'),
    path('option/', views.option_detail_ajax, name='option_detail_ajax'),
    path('empoption/', views.emp_detail_ajax, name='emp_detail_ajax'),
]
