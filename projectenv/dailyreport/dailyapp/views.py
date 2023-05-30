from django.shortcuts import render
from .models import *
from dailyapp.models import notes,login,enquiry,dactivity
from dailyapp.models import enquiry,appointment_detail,employee_details,domestic_cust_add,business_cust_add
from django.http import HttpResponse
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime
from django.db import connection
# Create your views here.

def request_resource(request):
    return render(request,'request_resource.html')

def save_request(request):
    if request.method=='POST':
        s = request.session['sid']
        robj = resource_requests()
        robj.resource = request.POST.get('res')
        robj.details = request.POST.get('desc')
        robj.date = request.POST.get('date')
        robj.time = request.POST.get('time')
        robj.status = 1
        robj.requested_by_id = s
        robj.save()
        messages.success(request, 'Request send!!')
        return render(request,'request_resource.html')
    else:
        return render(request,'request_resource.html')

def request_list(request):
    # rlist = resource_requests.objects.filter(status=1).select_related('requested_by')
    # return render(request,'request_list.html',{'rlist':rlist})
    rlist = resource_requests.objects.filter(status=1)
    employee_ids = rlist.values_list('requested_by', flat=True)
    employees = employee_details.objects.filter(id__in=employee_ids)
    employee_names = {employee.id: employee.emp_name for employee in employees}
    return render(request, 'request_list.html', {'rlist': rlist, 'employee_names': employee_names})

def rapprove(request,id):
    appobj = resource_requests.objects.get(id=id)
    appobj.status = 2
    appobj.save()
    messages.success(request, 'Request Approved!!')
    rlist = resource_requests.objects.filter(status=1)
    employee_ids = rlist.values_list('requested_by', flat=True)
    employees = employee_details.objects.filter(id__in=employee_ids)
    employee_names = {employee.id: employee.emp_name for employee in employees}
    return render(request, 'request_list.html', {'rlist': rlist, 'employee_names': employee_names})
    # return render(request,'request_list.html')

def rreject(request,id):
    appobj = resource_requests.objects.get(id=id)
    appobj.status = 3
    appobj.save()
    messages.success(request, 'Request Rejected!!')
    rlist = resource_requests.objects.filter(status=1)
    employee_ids = rlist.values_list('requested_by', flat=True)
    employees = employee_details.objects.filter(id__in=employee_ids)
    employee_names = {employee.id: employee.emp_name for employee in employees}
    return render(request, 'request_list.html', {'rlist': rlist, 'employee_names': employee_names})
    # return render(request,'request_list.html')

def view_rstatus(request):
    s = request.session['sid']
    status_list = resource_requests.objects.filter(requested_by=s)
    return render(request,'view_status.html',{'status_list':status_list})

def view_cust_details(request):
    s = request.session['sid']
    empobj = employee_details.objects.get(id=s)
    desid = empobj.designation_id
    depid = empobj.department_id
    desobj = designation.objects.get(id=desid)
    desname = desobj.des_name
    if desname == 'Manager':
        # bcust_details = business_cust_add.objects.all().select_related('benquiry')
        # dcust_details = domestic_cust_add.objects.all().select_related('enquiry')
        bcust_details = business_cust_add.objects.filter(benquiry__emp_id__in=employee_details.objects.filter(department_id=depid).values('id')).select_related('benquiry')
        dcust_details = domestic_cust_add.objects.filter(enquiry__emp_id__in=employee_details.objects.filter(department_id=depid).values('id')).select_related('enquiry')
        context ={
            'bcust_details':bcust_details,
            'dcust_details':dcust_details,
        }
        return render(request,'view_cust_details.html',context)
    elif desname == 'Employee':
        # bcust_details = business_cust_add.objects.filter(emp_id=s).select_related('benquiry')
        # dcust_details = domestic_cust_add.objects.filter(emp_id=s).select_related('enquiry')
        enq_ids = enquiry.objects.filter(emp_id=s).values_list('id', flat=True)
        bcust_details = business_cust_add.objects.filter(benquiry_id__in=enq_ids).select_related('benquiry')
        dcust_details = domestic_cust_add.objects.filter(enquiry_id__in=enq_ids).select_related('enquiry')

        context ={
            'bcust_details':bcust_details,
            'dcust_details':dcust_details,
        }
        return render(request,'view_cust_details.html',context)

def view_app(request):
    s = request.session['sid']
    disapp = appointment_detail.objects.filter(emp_id =s)
    return render(request,'view_app.html',{'disapp':disapp})

def admin_page(request):
    deptobj = department.objects.all()
    desobj = designation.objects.all()
    contact = {
        'deptobj':deptobj,
        'desobj':desobj,
    }
    return render(request,'admin.html',context)

def index(request):
    sid = request.session['sid']
    lobj = login.objects.get(employee_id=sid)
    desid = lobj.des_id
    desobj = designation.objects.get(id=desid)
    return render(request,'index.html',{'desobj':desobj})

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
        if login.objects.filter(user_name=uname).exists():
            messages.warning(request, 'Username already taken!!')
            return render(request,'add_credentials.html')
        else:
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

def view_status(request):
    dtask = dactivity.objects.all().select_related('t', 'updated_emp')
    return render(request,'view_tstatus.html',{'dtask':dtask})

def task(request):
    s = request.session['sid']
    empobj = employee_details.objects.get(id=s)
    desid = empobj.designation_id
    dep_id = empobj.department_id
    desobj = designation.objects.get(id=desid)
    displaytask = task_create.objects.filter(created_by=s)
    viewtask = task_assigning.objects.filter(task_assigned_to_id=s).select_related('task')
    # dtask = dactivity.objects.select_related('t', 'updated_emp').all()
    dtask = dactivity.objects.filter(updated_emp_dept=dep_id).select_related('t', 'updated_emp')
    context = {
        'desobj':desobj,
        'displaytask':displaytask,
        'viewtask':viewtask,
        'dtask':dtask,
    }
    return render(request,'task.html',context)
        

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

def d_activity(request):
    s = request.session['sid']
    #distask = task_create.objects.filter(task_assigned_to_id=s).select_related('task')
    distask = task_assigning.objects.filter(task_assigned_to_id = s).select_related('task')
    dtemp = employee_details.objects.get(id=s)
    did = dtemp.department_id
    context ={
        'distask':distask,
        'did':did,
        's':s,
    }
    return render(request,'daily_activity.html',context)

def createnote(request):
    return render(request,'create_note.html')

def enquiry_details(request):
    s = request.session['sid']
    return render(request,'enquiry_details.html')

def test(request):
    return render(request,'test.html')

def appointment_details(request):
        s = request.session['sid']
        custo = enquiry.objects.filter(emp_id=s)
        return render(request,'appointment.html',{'custo':custo})

#ajax
def option_detail_ajax(request):
    q = request.GET.get('q')  # Retrieve the value of the "q" parameter
    option = enquiry.objects.get(id=q)
    data = {
        'phn_num': option.phn_num,
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
    bobj = business_cust_add.objects.all()
    benquiry_ids = [obj.benquiry.id for obj in bobj]
    displaycust = enquiry.objects.exclude(id__in=benquiry_ids)
    # displaycust = enquiry.objects.exclude(id=bobj.benquiry)
    return render(request,'domestic_cust.html',{'displaycust':displaycust})

def business_customer(request):
    dobj = domestic_cust_add.objects.all()
    enquiry_ids = [obj.enquiry.id for obj in dobj]
    displaycust = enquiry.objects.exclude(id__in=enquiry_ids)
    return render(request,'business_cust.html',{'displaycust':displaycust})

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
                    departobj = department.objects.all()
                    desigobj = designation.objects.all()
                    eobj = employee_details.objects.all().select_related('department')
                    context = {
                        'departobj':departobj,
                        'desigobj':desigobj,
                        'eobj':eobj,
                    }
                    return render(request,'admin.html',context)
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
                        tobj = employee_details.objects.get(id=sid)
                        context={
                            'desobj':desobj,
                            'tobj':tobj,
                        }
                        return render(request,'index.html',context)
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
        if enquiry.objects.filter(email=email).exists():
            messages.warning(request, 'email already exists!!')
            return render(request,'enquiry_details.html')
        else:
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
        c_name = request.POST.get('optionSelect')
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
        if employee_details.objects.filter(email=email).exists():
            messages.warning(request, 'email already exists!!')
            return render(request,'emp_detail.html')
        else:
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
        ob = domestic_cust_add()
        ob.enquiry_id = request.POST.get('optionSelect')
        ob.added_by = request.session['sid']
        ob.p_address = request.POST.get('paddress')
        ob.save()
        return HttpResponse('details Added')
    else:
        return render(request,'domestic_cust.html')


def save_business(request):
    if request.method == 'POST':
        obj4 = business_cust_add()
        obj4.company_name = request.POST.get('company')
        obj4.website_address = request.POST.get('website')
        obj4.b_address = request.POST.get('baddress')
        obj4.benquiry_id = request.POST.get('cname')
        obj4.added_by = request.session['sid']
        obj4.save()
        messages.success(request, 'Details added!!')
        return render(request, 'business_cust.html')
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
        s = request.session['sid']
        empobj = employee_details.objects.get(id=s)
        d_id = empobj.department_id
        obj7 = dactivity()
        obj7.status = request.POST.get('status')
        obj7.submitted_date = datetime.now().date()
        obj7.remarks = request.POST.get('remarks')
        taskname = request.POST.get('taskname')
        obj7.t_id = int(taskname)
        obj7.updated_emp_id = request.session['sid']
        obj7.updated_emp_dept = d_id
        obj7.save()
        messages.success(request, 'Daily report submitted!!')
        return render(request, 'daily_activity.html')
    else:
        return render(request, 'daily_activity.html')


def lgout(request):
        request.session.flush()
        return render(request,'login.html')