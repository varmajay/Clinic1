import email
from time import strptime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.conf import settings
from django.core.mail import send_mail
from .models import *
from django.contrib.auth.decorators import login_required
from datetime import date
from datetime import datetime



# def check_login(request):
#     try: 
#         uid = User.objects.get(email=request.session['email'])
#         return redirect(True)
#     except:
#         return redirect('login')




# Create your views here.
def main_index(request): 
    doc_count = User.objects.filter(roles ='doctor').count()
    pat_count = User.objects.filter(roles ='patients').count()
    doc = User.objects.filter(roles ='doctor')
    return render(request,'main-index.html',{'doc_count':doc_count,'pat_count':pat_count,'doc':doc})




def index(request):
    # try:
    doc_count = User.objects.filter(roles ='doctor').count()
    pat_count = User.objects.filter(roles ='patients').count()
    # app_count = Appoinment.objects.filter().count()
    # print(app_count)
    admin = User.objects.get(email=request.session['email'])
    return render(request,'index.html',{'admin':admin,'pat_count':pat_count,'doc_count':doc_count})
    # except:
    #     return redirect('login')


def index_doc(request):
    # try:
    doc_count = User.objects.filter(roles ='doctor').count()
    pat_count = User.objects.filter(roles ='patients').count()
    # app_count = Appoinment.objects.all().count()
    uid = User.objects.get(email=request.session['email'])
    return render(request,'index-doc.html',{'uid':uid,'pat_count':pat_count,'doc_count':doc_count})
    # except:
    #     return redirect('login')


def index_pat(request):
    # try:
    uid = User.objects.get(email=request.session['email'])
    return render(request,'index-pat.html',{'uid':uid})
    # except:
    #     return redirect('login')




def login(request):
        try:
            uid = User.objects.get(email=request.session['email'])
            if uid.roles == "admin":
                return redirect('index')
            elif uid.roles =="doctor":
                return redirect('index-doc')
            else:
                return redirect('index-pat')
        except:
            # print(User.roles)
            if request.method == 'POST':
                try:
                    uid = User.objects.get(email=request.POST['email'])
                    if uid.roles == "admin":
                        if request.POST['password'] == uid.password:
                            request.session['email'] = request.POST['email']
                            return redirect('index')
                        return render(request,'login.html',{'msg':'Please Enter Valid Password'})
                    elif uid.roles == "doctor":
                        if request.POST['password'] == uid.password:
                            request.session['email'] = request.POST['email']
                            return redirect('index-doc')
                        return render(request,'login.html',{'msg':'Please Enter Valid Password'})
                    else:
                        if request.POST['password'] == uid.password:
                            request.session['email'] = request.POST['email']
                            return redirect('index-pat')
                        return render(request,'login.html',{'msg':'Please Enter Valid Password'})
                except:
                    msg = "Please Enter Valid Email"
                    return render(request,'login.html',{'msg':msg})
        return render(request,'login.html') 



def logout(request):
    del request.session['email']
    return redirect('main-index')




#-------------------------------------------------Doctor------------------------------------------------------# 
# @login_required(login_url='login')
# @check_login()
def create_doctor(request):
    try:
        # uid = User.objects.get(email=request.session['email'])
        admin = User.objects.get(email=request.session['email'])
        if request.method == "POST":
            try:
                User.objects.get(email=request.POST['email'])
                msg = "Doctor Email is already Exits "
                return render(request,'create-doctor.html',{'msg':msg,'admin':admin})
            except:
                password = ''.join(choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))
                subject = 'welcome to Clinic'
                message = f"""Hello {request.POST['name']},
                Your Username is  {request.POST['email']},
                Your Password is {password} """
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.POST['email'], ]
                send_mail( subject, message, email_from, recipient_list )
                User.objects.create(
                    roles = request.POST['roles'],
                    name = request.POST['name'],
                    email = request.POST['email'],
                    password = password,
                ) 
        return render(request,'create-doctor.html',{'admin':admin})
    except:
        return redirect('login')
        



def view_doctor(request):
    try:
        admin = User.objects.get(email=request.session['email'])
        uid = User.objects.all().filter(roles ='doctor')
        return render(request,'view-doctor.html',{'admin':admin,'uid':uid})
    except:
        return redirect('login')



def update_doctor(request,pk):
    try:
        admin = User.objects.get(email=request.session['email'])
        uid = User.objects.get(id=pk)
        if request.method == 'POST':
            uid.name=request.POST['name']
            uid.clinic_name = request.POST['clinic_name']
            uid.gender = request.POST['gender']
            uid.specialty = request.POST['specialty']
            uid.address = request.POST['address']
            uid.save()
        return render(request,'update-doctor.html',{'admin':admin,'uid':uid})
    except:
        return redirect('login')





def delete_doctor(request,pk):
    doc = User.objects.get(id=pk)
    doc.delete()
    return redirect('view-doctor')


def profile_doc(request):
    try:
        admin = User.objects.get(email=request.session['email'])
        uid = User.objects.get(email=request.session['email'])
        if request.method == 'POST':
            uid.name = request.POST['name']
            uid.clinic_name = request.POST['clinic_name']
            uid.gender = request.POST['gender']
            uid.specialty = request.POST['specialty']
            uid.address = request.POST['address']
            uid.save()
            # return redirect('index-doc')
        return render(request,'profile-doc.html',{'uid':uid})
    except:
        return redirect('login')



#---------------------------------------------------------patient-----------------------------------------------#

def create_patient(request):
    try:
        admin = User.objects.get(email=request.session['email'])
        if request.method == "POST":
            try:
                User.objects.get(email=request.POST['email'])
                msg = "Patient Email is already Exits "
                return render(request,'create-patient.html',{'msg':msg})
            except:
                password = ''.join(choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))
                subject = 'welcome to Clinic'
                message = f"""Hello {request.POST['name']},
                Your Username is  {request.POST['email']},
                Your Password is {password} """
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.POST['email'], ]
                send_mail( subject, message, email_from, recipient_list )
                User.objects.create(
                    roles = request.POST['roles'],
                    name = request.POST['name'],
                    email = request.POST['email'],
                    password = password,
                )
        return render(request,'create-patient.html',{'admin':admin})
    except:
        return redirect('login')



def view_patient(request):
    try:
        admin = User.objects.get(email=request.session['email'])
        uid = User.objects.all().filter(roles = 'patients')
        return render(request,'view-patient.html',{'uid':uid,'admin':admin})
    except:
        return redirect('login')


def update_patient(request,pk):
    try:
        admin = User.objects.get(email=request.session['email'])
        uid = User.objects.get(id=pk)
        if request.method == 'POST':
            uid.name=request.POST['name']
            uid.phone = request.POST['phone']
            uid.gender = request.POST['gender']
            uid.address = request.POST['address']
            if 'profile' in request.FILES:
                uid.profile = request.FILES['profile']
            uid.save()
        return render(request,'update-patient.html',{'uid':uid,'admin':admin})
    except:
        return redirect('login')




def delete_patient(request,pk):
    pat = User.objects.get(id=pk)
    pat.delete()
    return redirect('view-patient')



def profile_pat(request):
    try:
        admin = User.objects.get(email=request.session['email'])
        uid = User.objects.get(email=request.session['email'])
        if request.method == "POST":
            uid.name = request.POST['name']
            uid.gender = request.POST['gender']
            uid.address = request.POST['address']
            if 'profile' in request.FILES:
                uid.profile = request.FILES['profile']
            uid.save()
        return render(request,'profile-pat.html',{'uid':uid,'admin':admin})
    except:
        return redirect('login')




#----------------------------------------------------------slot---------------------------------------------------#
def create_doc_availibility(doc_id,day,start,end):
    Doctor_availability.objects.create(
                doctor = doc_id,
                week = day,
                start_time = start,
                end_time = end,
            )

def update_doc_availability(doc_id,day,start,end):
    uid = Doctor_availability.objects.get(doctor__id = doc_id,week = day)
    uid.week = day
    uid.start_time = start
    uid.end_time = end
    uid.save()


def slot(request):
    uid = User.objects.get(email=request.session['email'])
    # if request.method == "GET":
    #     res={}
    #     avl =  Doctor_availability.objects.filter(doctor = uid)
    #     for data in avl:
    #         res[data.week] = {
    #             "week":data.week,
    #             "st":data.start_time,
    #             "et":data.end_time,
    #         }
    #     return render(request,'slot.html',{'res':res})
    mon = Doctor_availability.objects.filter(doctor__id = uid.id ,week = 'Mon').first()
    tue = Doctor_availability.objects.filter(doctor__id = uid.id ,week = 'Tue').first()
    wed = Doctor_availability.objects.filter(doctor__id = uid.id ,week = 'Wed').first()
    thu = Doctor_availability.objects.filter(doctor__id = uid.id ,week = 'Thu').first()
    fri = Doctor_availability.objects.filter(doctor__id = uid.id ,week = 'Fri').first()
    sat = Doctor_availability.objects.filter(doctor__id = uid.id ,week = 'Sat').first()


    if request.method == "POST":
        if request.POST.get('mon') is not None and request.POST.get('mon_starttime') is not None and request.POST.get('mon_endtime') is not None:
            # print(uid,request.POST.get('mon'),request.POST.get('mon_starttime'),request.POST.get('mon_endtime'),'-------------------1')
            if not Doctor_availability.objects.filter(doctor__id = uid.id , week=request.POST['mon']).exists():
                create_doc_availibility(uid,request.POST.get('mon'),request.POST.get('mon_starttime'),request.POST.get('mon_endtime'))
            else:
                update_doc_availability(uid.id,request.POST.get('mon'),request.POST.get('mon_starttime'),request.POST.get('mon_endtime'))



        if request.POST.get('tue') is not None and request.POST.get('tue_starttime') is not None and request.POST.get('tue_endtime') is not None:
            # print('-------------------2')
            if not Doctor_availability.objects.filter(doctor__id = uid.id , week=request.POST['tue']).exists():
                create_doc_availibility(uid,request.POST.get('tue'),request.POST.get('tue_starttime'),request.POST.get('tue_endtime'))
            else:
                update_doc_availability(uid.id,request.POST.get('tue'),request.POST.get('tue_starttime'),request.POST.get('tue_endtime'))



        if request.POST.get('wed') is not None and request.POST.get('wed_starttime') is not None and request.POST.get('wed_endtime') is not None:
            # print('-------------------3')
            if not Doctor_availability.objects.filter(doctor__id = uid.id , week=request.POST['wed']).exists():
                create_doc_availibility(uid,request.POST.get('wed'),request.POST.get('wed_starttime'),request.POST.get('wed_endtime'))
            else:
                update_doc_availability(uid.id,request.POST.get('wed'),request.POST.get('wed_starttime'),request.POST.get('wed_endtime'))



        if request.POST.get('thu') is not None and request.POST.get('thu_starttime') is not None and request.POST.get('thu_endtime') is not None:
            # print('-------------------4')
            if not Doctor_availability.objects.filter(doctor__id = uid.id , week=request.POST['thu']).exists():
                create_doc_availibility(uid,request.POST.get('thu'),request.POST.get('thu_starttime'),request.POST.get('thu_endtime'))
            else:
                update_doc_availability(uid.id,request.POST.get('thu'),request.POST.get('thu_starttime'),request.POST.get('thu_endtime'))



        if request.POST.get('fri') is not None and request.POST.get('fri_starttime') is not None and request.POST.get('fri_endtime') is not None:
            # print('-------------------5')
            if not Doctor_availability.objects.filter(doctor__id = uid.id , week=request.POST['fri']).exists():
                create_doc_availibility(uid,request.POST.get('fri'),request.POST.get('fri_starttime'),request.POST.get('fri_endtime'))
            else:
                update_doc_availability(uid.id,request.POST.get('fri'),request.POST.get('fri_starttime'),request.POST.get('fri_endtime'))



        if request.POST.get('sat') is not None and request.POST.get('sat_starttime') is not None and request.POST.get('sat_endtime') is not None:
            # print('-------------------6')
            if not Doctor_availability.objects.filter(doctor__id = uid.id , week=request.POST['sat']).exists():
                create_doc_availibility(uid,request.POST.get('sat'),request.POST.get('sat_starttime'),request.POST.get('sat_endtime'))
            else:
                update_doc_availability(uid.id,request.POST.get('sat'),request.POST.get('sat_starttime'),request.POST.get('sat_endtime'))
        return render(request,'slot.html',{'msg':'Sucessfully Slot is Added'})
    return render(request,'slot.html',{'mon':mon,'tue':tue,'wed':wed,'thu':thu,'fri':fri,'sat':sat,'mon':mon,})








# --------------------------------------------book Appoinment---------------------------------------------------
def book_app(request):
    uid = User.objects.filter(roles= 'doctor')
    if request.method == "POST":
        con = Doctor_availability.objects.filter(doctor__id = request.POST['doctor'])
        b =  datetime.strptime(request.POST['date'], "%Y-%m-%d").date()
        c = b.strftime("%a")
        for data in con :
            print(data.week)
            if data.week == c:
                return render(request,'book-app.html',{ 'uid':uid,'msg':'Doctor Not Available On This Time'})
            else:
                doc = User.objects.get(id = request.POST['doctor'])
                pat = User.objects.get(email=request.session['email'])
                data = Appoinment.objects.filter(date = request.POST['date'],doctor__id = request.POST['doctor'])
                print(data)
                x_start = request.POST['start_time']+':0'
                temp_start = datetime.strptime(x_start, '%H:%M:%S').time()
                # print(x)
                # print(temp_start)
                # print(type(temp_start))
                # print(data)
                for app in data:
                    # print(app)
                    # print(app.end_time )
                    if  temp_start >= app.start_time and temp_start < app.end_time :
                        return render(request,'book-app.html',{ 'uid':uid,'msg':'Doctor is not Available'})

                Appoinment.objects.create(
                    doctor = doc,
                    patient = pat,
                    date = request.POST['date'],
                    start_time = request.POST['start_time'],
                    end_time = request.POST['end_time'],
                    description =request.POST['description']
                )
                return render(request,'book-app.html',{ 'uid':uid,'msg':'Your Appoinment Is Successfully Book '})
    return render(request,'book-app.html',{'uid':uid })






    
def book_app_view(request):   #PATIENTS
    # try:
    pat = User.objects.get(email= request.session['email'])
    uid = Appoinment.objects.filter(patient__id=pat.id)
    return render(request,'book-app-view.html',{'uid':uid})
    # except:
    #     return redirect('login')


def view_appoinment(request): #DOCTOR
    # try:
    doc = User.objects.get(email= request.session['email'])
    now = date.today()
    # print(now)
    uid = Appoinment.objects.filter(doctor__id=doc.id).order_by('date')

    return render(request,'view-appoinment.html',{'uid':uid,'doc':doc,'now':now})
    # except:
    #     return redirect('login')








#----------------------------------------------Status-action-------------------------------------------------#

def status_complete(request,pk):
    uid = Appoinment.objects.get(id=pk)
    # var = Slot.objects.get(id=uid.slot.id)
    # print(var)
    uid.status = 1
    uid.save()
    # var.delete()
    # var.save()
    return redirect('view-appoinment')


def status_absent(request,pk):
    uid = Appoinment.objects.get(id=pk)
    uid.status = 2
    uid.save()
    return redirect('view-appoinment')


def status_cancelled(request,pk):
    uid = Appoinment.objects.get(id=pk)
    uid.status = 3
    uid.save()
    return redirect('view-appoinment')



def pat_status_cancelled(request,pk):
    uid = Appoinment.objects.get(id=pk)
    uid.status = 3
    uid.save()
    return redirect('book-app-view')








#----------------------------------------admin view Appoinment-------------------------------#


def view_appoinment_admin(request):
    try:
        uid = Appoinment.objects.all()
        admin = User.objects.get(email=request.session['email'])
        return render(request,'view-appoinment-admin.html',{'uid':uid,'admin':admin})
    except:
        return redirect('login')

