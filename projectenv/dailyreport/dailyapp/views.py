from django.shortcuts import render
from .models import *
from dailyapp.models import notes,login,enquiry
from dailyapp.models import enquiry,appointment_detail,employee_details,domestic_cust_add,business_cust_add
from django.http import HttpResponse
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime
from django.db import connection
# Create your views here.

def admin_page(request):
    return render(request,'admin.html')

def index(request):
    return render(request,'index.html',{})

def change_pwd(request):
    s = request.session['sid']
    pobj = login.objects.get(employee_id=s)
    return render(request,'change_password.html',{'pobj':pobj})

def save_changep(request):
    if request.method=='POST':
        s = request.session['sid']
        sobj = login.objects.get(employee_id=s)
        oldpwd = request.POST.get('oldpwd')
        newpwd = request.POST.get('newpwd')
        if sobj.password == oldpwd:
            sobj.password = newpwd
            sobj.save()
            messages.success(request, 'Password changed!!')
            return render(request,'change_password.html')
        else:
            messages.success(request, 'Password Incorrect!!')
            return render(request,'change_password.html')
    else:
        return render(request,'change_password.html')
def note(request):
    s = request.session['sid']
    displaynote = notes.objects.filter(created_by=s)
    return render(request,'note.html',{'displaynote':displaynote})

def add_dept(request):
    return render(request,'add_department.html')

def add_des(request):
    return render(request,'add_designation.html')

def save_dept(request):
    if request.method=='POST':
        deptobj = department()
        deptobj.dept_name = request.POST.get('dept_name')
        deptobj.save()
        messages.success(request, 'Department Added!!')
        return render(request,'add_department.html')
    else:
        return render(request,'add_department.html')

def save_des(request):
    if request.method=='POST':
        desobj = designation()
        desobj.des_name = request.POST.get('des_name')
        desobj.save()
        messages.success(request, 'Designation Added!!')
        return render(request,'add_designation.html')
    else:
        return render(request,'add_designation.html')

def add_login(request):
    emp = employee_details.objects.all()
    return render(request,'add_credentials.html',{'emp':emp})

#ajax
def option_ajax(request):
    q = request.GET.get('q')  # Retrieve the value of the "q" parameter
    option = employee_details.objects.get(id=q)
    data = {
        'email': option.email,
    }   
    return JsonResponse(data)

def save_login(request):
    if request.method=='POST':
        empid = request.POST.get('optionSelect')
        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')
        tempobj = employee_details.objects.get(id=empid)
        i = tempobj.designation_id
        logobj = login()
        logobj.user_name = uname
        logobj.password = pwd
        logobj.des_id = i
        logobj.employee_id = empid
        logobj.save()
        messages.success(request, 'Credentials Added!!')
        return render(request,'add_credentials.html')
    else:
        return render(request,'add_credentials.html')


def task(request):
    s = request.session['sid']
    empobj = employee_details.objects.get(id=s)
    desid = empobj.designation_id
    desobj = designation.objects.get(id=desid)
    desname = desobj.des_name
    if desname == 'Manager':
        displaytask = task_create.objects.filter(created_by=s)
        context = {
            'desobj':desobj,
            'displaytask':displaytask
        }
        return render(request,'task.html',context)
    elif desname == 'Employee':
        t = task_assigning.objects.filter(task_assigned_to_id=s).select_related('task')
        tcontext = {
            'desobj':desobj,
            't':t
        }
        return render(request,'task.html',tcontext)

def create_user_group(request):
    return render(request,'create_groups.html')

def assign_grp(request):
    disemp = employee_details.objects.all()
    disgrp = user_groups.objects.all()
    context={
        'disemp':disemp,
        'disgrp' : disgrp,
    }
    return render(request,'assign_group.html',context)

def admin_tassign(request):
    s = request.session['sid']
    task_names = task_create.objects.filter(created_by=s)
    emp_names = employee_details.objects.all()
    context ={
        'task_names':task_names,
        'emp_names':emp_names
    }
    return render(request,'admin_assign_task.html',context)

#ajax
def emp_detail_ajax(request):
    q = request.GET.get('q')  # Retrieve the value of the "q" parameter
    option = employee_details.objects.get(id=q)
    data = {
        'email': option.email,
    }   
    return JsonResponse(data)

def create_task(request):
    return render(request,'create_task.html',{})

def assign_task(request):
    s = request.session['sid']
    empobj = employee_details.objects.get(id=s)
    deptid = empobj.department_id
    task_names = task_create.objects.filter(created_by=s)
    emp_names = employee_details.objects.filter(department_id=deptid).exclude(id=s)
    context ={
        'task_names':task_names,
        'emp_names':emp_names
    }
    return render(request,'assign_task.html',context)

def dactivity(request):
    s = request.session['sid']
    #distask = task_create.objects.filter(task_assigned_to_id=s).select_related('task')
    gid = emp_group.objects.filter(employee_id=s)
    for i in gid:
        gdata = i
        gname = user_groups.objects.get(id=gdata.group_id)
    # admin_queryset = task_create.objects.get(admin_task_assigned_to_id=g).select_related('admin_task')
    return render(request,'daily_activity.html',{'gname':gname})

def createnote(request):
    return render(request,'create_note.html')

def enquiry_details(request):
    s = request.session['sid']
    return render(request,'enquiry_details.html')

def test(request):
    return render(request,'test.html')

def appointment_details(request):
        custo = enquiry.objects.all()
        s = request.session['sid']
        return render(request,'appointment.html',{'custo':custo})

#ajax
def option_detail_ajax(request):
    q = request.GET.get('q')  # Retrieve the value of the "q" parameter
    option = enquiry.objects.get(id=q)
    data = {
        'phn_num': option.phn_num,
        'email': option.email,
    }   
    return JsonResponse(data)

def emp_details(request):
    displaydept = department.objects.all()
    displaydes = designation.objects.all()
    context = {
        'displaydept' : displaydept,
        'displaydes' : displaydes,
    }
    return render(request,'emp_detail.html',context)
    # return render(request,'emp_detail.html')

def domestic_customer(request):
    displaycust = enquiry.objects.all()
    return render(request,'domestic_cust.html',{'displaycust':displaycust})

def business_customer(request):
    return render(request,'business_cust.html')

def user_login(request):
    if request.method == 'POST':
        if request.POST.get('user_name') and request.POST.get('password'):
            user_name = request.POST['user_name']
            password = request.POST['password']
            if user_name == 'admin':
                aobj = admin_login.objects.get(user_name = user_name)
                if aobj.password == password:
                    request.session['sid'] = aobj.id
                    sid = request.session['sid']
                    return render(request,'admin.html')
                else:
                    messages.error(request, 'Invalid username or password')
                    return render(request,'login.html')
            else:
                try:
                    lobj = login.objects.get(user_name = user_name)
                    if lobj.password == password:
                        request.session['sid'] = lobj.employee_id
                        sid = request.session['sid']
                        desid = lobj.des_id
                        desobj = designation.objects.get(id=desid)
                        return render(request,'index.html',{'desobj':desobj})
                    else:
                        messages.error(request, 'Invalid username or password')
                        return render(request,'login.html')
                except login.DoesNotExist:
                    messages.error(request, 'Invalid username or password')
                    return render(request,'login.html') 
        else:
                messages.error(request, 'Invalid username or password')
                return render(request,'login.html')
    else:
        return render(request,'login.html')

def save_emp_grp(request):
    if request.method=='POST':
        empobj = emp_group()
        empobj.employee_id = request.POST.get('empid')
        empobj.group_id = request.POST.get('grpid')
        empobj.save()
        messages.success(request, 'Group Assigned!!')
        return render(request,'assign_group.html')
    else:
        return render(request,'assign_group.html')

def save_user_group(request):
    if request.method=='POST':
        grpobj = user_groups()
        grpobj.gname = request.POST.get('grp_name')
        grpobj.save()
        messages.success(request, 'Group Created!!')
        return render(request,'create_groups.html')
    else:
        return render(request,'create_groups.html')

def save_admin_tassign(request):
    if request.method=='POST':
        tobj = admin_task_assign()
        tobj.assigned_to_id = request.POST.get('gid')
        tobj.task_id = request.POST.get('tid')
        tobj.start_date = request.POST.get('start_date')
        tobj.end_date = request.POST.get('end_date')
        tobj.save()
        messages.success(request, 'Task Assigned!!')
        return render(request,'admin_assign_task.html')
    else:
        return render(request,'admin_assign_task.html')

def save_assign_task(request):
    if request.method == 'POST':
        obj6 = task_assigning()
        task_name = request.POST.get('task_name')
        ename = request.POST.get('ename')
        s = request.session['sid']
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        tint = int(task_name)
        eint = int(ename)
        obj6.task_id = tint
        obj6.task_assigned_to_id  = eint
        obj6.task_assigned_by = s
        obj6.start_date = start_date
        obj6.end_date = end_date
        obj6.save()
        messages.success(request, 'Task Assigned!!')
        return render(request,'assign_task.html')
    else:
        return render(request,'assign_task.html')

def save_note(request):
    if request.method=='POST':
        t = request.POST.get('title')
        d = datetime.now().date()
        n = request.POST.get('note')
        e = request.session['sid']
        obj = notes()
        obj.title = t
        obj.ndate = d
        obj.note = n
        obj.created_by = e
        obj.save()
        messages.success(request, 'Note Added!!')
        return render(request,'create_note.html')
    else:
        return render(request,'create_note.html')


def save_enquiry(request):
    if request.method == 'POST':
        acc = enquiry()
        cust_name = request.POST.get('cname')
        email = request.POST.get('email')
        phn_num = request.POST.get('contact')
        add_for_comm = request.POST.get('address')
        details = request.POST.get('additional')
        employee_id = request.session['sid']

        acc.cust_name = cust_name
        acc.email = email
        acc.phn_num = phn_num
        acc.add_for_comm = add_for_comm
        acc.details = details
        acc.emp_id = employee_id
        acc.save()
        return HttpResponse('Details saved!!')
    else:
        return render(request, 'enquiry_details.html')

def save_appointment(request):
    if request.method == 'POST':
        c_name = request.POST.get('option-select')
        sdate = request.POST.get('scheduled_date')
        stime = request.POST.get('scheduled_time')
        p = request.POST.get('purpose')
        e_id = request.session['sid']

        obj2 = appointment_detail()
        obj2.cust_name = c_name
        obj2.scheduled_date = sdate
        obj2.scheduled_time = stime
        obj2.purpose = p
        obj2.emp_id = e_id
        obj2.save()
        return HttpResponse('Details Saved')
    else:
        return render('appointment.html')

def save_emp(request):
    if request.method=='POST':
        obj3 = employee_details()
        emp_name = request.POST.get('emp_name')
        email = request.POST.get('emp_email')
        department = request.POST.get('dept')
        designation = request.POST.get('des')
        deptint = int(department)
        desint = int(designation)
        obj3.emp_name = emp_name
        obj3.email = email
        obj3.department_id = deptint
        obj3.designation_id = desint
        obj3.save()
        return HttpResponse('details Added')
    else:
        return render(request,'emp_detail.html')

def save_domestic(request):
    if request.method == 'POST':
        c_name = request.POST.get('cname')
        p_address = request.POST.get('paddress')
        ob = domestic_cust_add()
        ob.cust_name = c_name
        ob.p_add = p_address
        ob.save()
        return HttpResponse('details Added')
    else:
        return render(request,'domestic_cust.html')

def save_business(request):
    if request.method == 'POST':
        obj4 = business_cust_add()
        obj4.cust_name = request.POST.get('cname')
        obj4.company_name = request.POST.get('company')
        obj4.website_address = request.POST.get('website')
        obj4.b_address = request.POST.get('baddress')
        obj4.save()
        return HttpResponse('Details saved!!')
    else:
        return render(request, 'business_cust.html')

def save_task(request):
    if request.method == 'POST':
        obj5 = task_create()
        obj5.t_name = request.POST.get('tname')
        obj5.t_desc = request.POST.get('tdesc')
        obj5.created_date = datetime.now().date()
        obj5.created_by = request.session['sid']
        obj5.save()
        messages.success(request, 'Task created!!')
        return render(request, 'create_task.html')
    else:
        return render(request, 'create_task.html')

def save_daily_activity(request):
    if request.method == 'POST':
        obj7 = daily_activity()
        obj7.status = request.POST.get('status')
        obj7.ddate = datetime.now().date()
        obj7.remaks = request.POST.get('remarks')
        obj7.emp_id = request.session['sid']
        obj7.task_id = request.POST.get('taskname')
        obj7.save()
        messages.success(request, 'Daily report submitted!!')
    else:
        return render(request, 'daily_activity.html')

def lgout(request):
        request.session.flush()
        return render(request,'login.html')