from django.db import models

# Create your models here.


class department(models.Model):
    dept_name = models.CharField(max_length=30)
    def __str__(self):
        return self.dept_name

class designation(models.Model):
    des_name = models.CharField(max_length=30)
    def __str__(self):
        return self.des_name

class employee_details(models.Model):
    emp_name = models.CharField(max_length=40)
    email = models.CharField(max_length=40)
    designation = models.ForeignKey(designation, on_delete = models.CASCADE, default=1)
    department = models.ForeignKey(department, on_delete = models.CASCADE, default=1)
    def __str__(self):
        return self.emp_name

class login(models.Model):
    user_name = models.CharField(max_length=80)
    password = models.CharField(max_length=80)
    employee = models.ForeignKey(employee_details, on_delete = models.CASCADE, default=1)
    des = models.ForeignKey(designation, on_delete = models.CASCADE, default=1)
    def __str__(self):
        return self.user_name

class resource_requests(models.Model):
    resource = models.CharField(max_length=80)
    details = models.TextField()
    date = models.DateField()
    time = models.CharField(max_length=80)
    status = models.IntegerField(default=1)
    requested_by = models.ForeignKey(employee_details, on_delete = models.CASCADE)


class enquiry(models.Model):
    emp_id = models.IntegerField(default=0)
    #emp_id = models.IntegerField(default=1)
    cust_name = models.CharField(max_length=40)
    email = models.CharField(max_length=40)
    phn_num = models.CharField(max_length=30)
    add_for_comm = models.TextField()
    details = models.TextField()
    def __str__(self):
        return self.cust_name

class appointment_detail(models.Model):
    cust_name = models.CharField(max_length=40)
    scheduled_date = models.DateField()
    scheduled_time = models.CharField(max_length=40)
    purpose = models.CharField(max_length=40)
    emp_id = models.IntegerField(default=1)
    def __str__(self):
        return self.cust_name

class domestic_cust_add(models.Model):
    enquiry = models.ForeignKey(enquiry,on_delete = models.CASCADE, default=1)
    added_by = models.IntegerField(default=0)
    p_address = models.TextField()
    def __str__(self):
        return self.p_address

class business_cust_add(models.Model):
    benquiry = models.ForeignKey(enquiry,on_delete = models.CASCADE, default=1)
    added_by = models.IntegerField(default=0)
    company_name = models.CharField(max_length=40)
    b_address = models.TextField()
    website_address = models.TextField()
    def __str__(self):
        return self.company_name

class task_create(models.Model):
    t_name = models.CharField(max_length=40)
    t_desc = models.TextField()
    created_date = models.DateField()
    created_by = models.IntegerField(default=1)
    def __str__(self):
        return self.t_name



class task_assigning(models.Model):
    task = models.ForeignKey(task_create, on_delete = models.CASCADE, default=1)
    task_assigned_to = models.ForeignKey(employee_details, on_delete = models.CASCADE, default=1, related_name='taskassign')
    task_assigned_by = models.IntegerField(default=1)
    start_date = models.DateField()
    end_date = models.DateField()
    def __str__(self):
        return self.task


class notes(models.Model):
    created_by = models.IntegerField(default=0)
    #emp_id = models.IntegerField(default=1)
    title = models.CharField(max_length=40, default='note title')
    ndate = models.DateField()
    note = models.TextField()
    def __str__(self):
        return self.emp

class dactivity(models.Model):
    updated_emp = models.ForeignKey(employee_details, on_delete = models.CASCADE, default=1)
    updated_emp_dept = models.IntegerField(default=0)
    t = models.ForeignKey(task_create, on_delete = models.CASCADE, default=1)
    status = models.CharField(max_length=40)
    submitted_date = models.DateField()
    remarks = models.TextField(default='remarks')
    def __str__(self):
        return self.task

class admin_login(models.Model):
    user_name = models.CharField(max_length=80)
    password = models.CharField(max_length=80)
