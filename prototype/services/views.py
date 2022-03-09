import datetime
from traceback import print_tb
from django.contrib import messages
from django.http import BadHeaderError, FileResponse, HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from user_accounts.models import MentorInfo, StartupCompanyInfo, User, UserPersonalInfo
from .models import Appointment, BoardMembers, Careers, Events, Gallery, JobApplication, News, Notifications, OurTeam, QueriesAndReviews
from .forms import AddEvents, AddJobForm, AddTeamMember, GalleryForm, JobApplicationForm, NewsForm, StartupContract
from user_accounts.views import getPersonalPercentageStartup, getCompanyPercentage, login
from django.core.mail import send_mail
from django.template import loader

@login_required(login_url='/login/')
def StaffView(request):
    if request.user.is_authenticated and request.user.type == 'Staff':
        today = datetime.datetime.now().date()
        data = User.objects.all()
        newsData = News.objects.all()
        team = OurTeam.objects.all()
        applications = JobApplication.objects.all()
        jobs = Careers.objects.all()
        list = []
        for job in jobs:
            list.append(job.id)
        print(list)

        p_data = StartupCompanyInfo.objects.all()   
        appointment = Appointment.objects.all() 
        gallery_data = Gallery.objects.all()
        queries = QueriesAndReviews.objects.all()
        jobs = Careers.objects.order_by('-date')
        member_form = AddTeamMember()
        gallery_form = GalleryForm()
        career_form = AddJobForm()
        events_form = AddEvents()
        total_startups = User.objects.filter(type="Startup").count()
        total_mentors = User.objects.filter(type="Mentor").count()
        approved_startups =  User.objects.filter(type="Startup",approved="True").count()
        approved_mentors = User.objects.filter(type="Mentor",approved="True").count()
        events = Events.objects.order_by('-start_date')
        return render(request,'staff_view.html',{'data':data,'p_data':p_data,'newsData':newsData,
        'newsForm':NewsForm,'appointment':appointment,'team':team,'member_form':member_form,
        'total_startups':total_startups,'total_mentors':total_mentors,'approved_startups':approved_startups,'approved_mentors':approved_mentors,
        'gallery_form':gallery_form,'gallery_data':gallery_data,'add_job':career_form,'jobs':jobs,'queries':queries,'events_form':events_form,
        'events':events,'today':today})

@login_required(login_url='/login/')
def addNews(request):    
    if request.user.is_authenticated and request.user.type == 'Staff' and request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            print('valid')
            time = datetime.date.today()
            data = News()
            data.title = form.cleaned_data.get('title')
            data.content = form.cleaned_data.get('content')
            data.pdf = form.cleaned_data.get('pdf')
            data.date = time
            data.save()
        else:
            print('not valid')
        return HttpResponse('saved')

def index(request):
    news = News.objects.order_by('-date')
    team = OurTeam.objects.all()
    board = BoardMembers.objects.all()
    return render(request, 'index.html',{'news':news,'team':team,'board':board})

def appointment(request):
    if request.method == 'POST':
        user = request.user
        print(user)
        data = Appointment()
        data.date = request.POST.get('date')
        data.time = request.POST.get('time')
        data.purpose = request.POST.get('purpose')
        if request.user.is_authenticated:
            data.name = user.first_name + '' + user.last_name
            data.email = user.email
        else:
            data.name = request.POST.get('name')
            data.email = request.POST.get('email')
            data.mobile = request.POST.get('mobile')
        data.save()
        return HttpResponse('')

def aboutAIC(request):
    team = OurTeam.objects.all()
    return render(request, 'about_aic.html',{'team':team})

def addTeamMember(request):
    if request.user.is_authenticated and request.user.type == 'Staff' and request.method == 'POST':
        form = AddTeamMember(request.POST, request.FILES)
        if form.is_valid():
            data = OurTeam()            
            data.first_name = form.cleaned_data.get('first_name')
            data.last_name = form.cleaned_data.get('last_name')
            data.designation = form.cleaned_data.get('designation')
            data.phone = form.cleaned_data.get('phone')
            data.profile_pic = form.cleaned_data.get('profile_pic')
            data.fb_link = form.cleaned_data.get('fb_link')
            data.twitter_link = form.cleaned_data.get('twitter_link')
            data.insta_link = form.cleaned_data.get('insta_link')
            data.linkedin_link = form.cleaned_data.get('linkedin_link')            
            data.save()
            
        else:
            print('invalid')
        return HttpResponse('')

def member(request,member_id):
    if request.user.is_authenticated and request.user.type == 'Staff' and request.method != 'POST':
        member = OurTeam.objects.get(id=member_id)
        form = AddTeamMember()
        form.initial['first_name'] = member.first_name
        form.initial['last_name'] = member.last_name
        form.initial['phone'] = member.phone
        # form.initial['profile_pic'] = member.profile_pic
        form.initial['designation'] = member.designation
        form.initial['fb_link'] = member.fb_link
        form.initial['twitter_link'] = member.twitter_link
        form.initial['insta_link'] = member.insta_link
        form.initial['linkedin_link'] = member.linkedin_link
        return render(request,'member.html',{'member':member,'member_form':form})
    else:
        return updateMember(request,member_id)

def updateMember(request,member_id):
    if request.user.is_authenticated and request.user.type == 'Staff' and request.method == 'POST':        
        data = OurTeam.objects.get(id=member_id)            
        form = AddTeamMember(request.POST, request.FILES)
        if form.is_valid():           
            data.first_name = form.cleaned_data.get('first_name')
            data.last_name = form.cleaned_data.get('last_name')
            data.designation = form.cleaned_data.get('designation')
            data.phone = form.cleaned_data.get('phone')
            data.profile_pic = form.cleaned_data.get('profile_pic')
            data.fb_link = form.cleaned_data.get('fb_link')
            data.twitter_link = form.cleaned_data.get('twitter_link')
            data.insta_link = form.cleaned_data.get('insta_link')
            data.linkedin_link = form.cleaned_data.get('linkedin_link')            
            data.save()
            pic = form.cleaned_data['profile_pic']
            print(pic)
        else:
            print('not valid'+ str(form.errors))            
        return StaffView(request)
    else:
        return index(request)

def gallery(request):
    data = Gallery.objects.all()
    return render(request,'gallery.html',{'data':data})

def addGallery(request):
    if request.user.is_authenticated and request.user.type == 'Staff' and request.method == 'POST':  
        form = GalleryForm(request.POST,request.FILES)
        if form.is_valid():
            data = Gallery()
            data.path = form.cleaned_data.get('path')
            data.description = form.cleaned_data.get('description')
            data.save()
        else:
            print('not valid')
        return HttpResponse('')

def startups(request):
    startups = User.objects.filter(type="Startup",approved="True")
    company = StartupCompanyInfo.objects.all()
    return render(request,'startups.html',{'startups':startups,'company':company})

def boardmembers(request):
    board = BoardMembers.objects.all()
    return render(request,'board_of_governors.html',{'board':board})

def news(request):
    news = News.objects.order_by('-date')
    return render(request,'news.html',{'news':news})

def viewPdf(request,news_id):
    data = News.objects.get(id=news_id)
    path = data.pdf
    return FileResponse(open('media/' + str(path), 'rb'), content_type='application/pdf')

def viewJobPdf(request,job_id):
    data = Careers.objects.get(id=job_id)
    path = data.job_pdf
    return FileResponse(open('media/' + str(path), 'rb'), content_type='application/pdf')


def careers(request):
    career = Careers.objects.order_by('-date')
    return render(request,'career.html',{'career':career})

@login_required(login_url='/login/')
def addJob(request):    
    if request.user.is_authenticated and request.user.type == 'Staff' and request.method == 'POST':
        form = AddJobForm(request.POST, request.FILES)
        if form.is_valid():
            time = datetime.date.today()
            data = Careers()
            data.job_title = form.cleaned_data.get('job_title')
            data.job_description = form.cleaned_data.get('job_description')
            data.job_pdf = form.cleaned_data.get('job_pdf')
            data.date = time
            data.job_qualification = form.cleaned_data.get('job_qualification')
            data.save()
        else:
            print('not valid')
        return HttpResponse('saved')

def queriesAndReviews(request):
    if request.method == 'POST':
        query = QueriesAndReviews()
        date = str(timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S"))
        if request.user.is_authenticated:
            query.name = str(request.user.first_name) + ' ' + str(request.user.last_name)
            query.email = str(request.user.email)
        else:
            query.name = request.POST.get('name')
            query.email = request.POST.get('email')
        query.subject = request.POST.get('subject')
        query.content = request.POST.get('content')
        query.date = date
        query.save()
    else:
        print('not valid')
    return HttpResponse('')

def addEvents(request):
    if request.user.is_authenticated and request.user.type == 'Staff' and request.method == 'POST':
        event = AddEvents(request.POST, request.FILES)
        if event.is_valid():
            data = Events()
            today = datetime.datetime.now().date()
            data.event_title = event.cleaned_data.get('event_title')
            data.event_content = event.cleaned_data.get('event_content')
            data.organizers = event.cleaned_data.get('organizers')
            data.start_date = event.cleaned_data.get('start_date')
            data.end_date = event.cleaned_data.get('end_date')
            data.start_time = event.cleaned_data.get('start_time')
            data.end_time = event.cleaned_data.get('end_time')
            data.more_info = event.cleaned_data.get('more_info')
            data.save()
            
            print(data.end_date)
            print(datetime.datetime.now().date())
            if data.end_date == today or data.start_date == today:
                print('today')
            elif data.start_date > today and data.end_date > today:
                print('upcoming')
            elif data.start_date < today and data.end_date < today:
                print('completed')

            
        else:
            print('not valid' + str(event.errors))
    return HttpResponse('<h2>404..Page Not Found!</h2>')

def viewEvents(request):
    events = Events.objects.order_by('-start_date')
    return render(request,'')

@login_required(login_url='/login/')
def RemoveNotifications(request):
    print('inside')
    if request.method == 'POST':
        n_id = request.POST.get('notification_id')
        row = Notifications.objects.get(id=n_id)
        row.delete()
        print(n_id)
    return HttpResponse('')

@login_required(login_url='/login/')
def IncubateStartupContract(request,user_id):
    if request.user.is_authenticated and request.user.type == 'Staff':
        form = StartupContract
        

@login_required(login_url='/login/')
def SendNotificationMail(request,user_id):
    if request.user.is_authenticated and request.user.type == 'Staff':
        subject = "Apply for incubation"
        line1 = "Greetings from AIC-IIIT Kottayam!."
        line2 = "Hope you are doing well."
        line3 = "we are happy to recieve your interest in AIC-IIIT Kottayam."
        line4 = "If you wish to be a part of us get incubated by clicking on"
        basic = User.objects.get(id=user_id)
        company = StartupCompanyInfo.objects.get(user_id=user_id)
        notification = Notifications()
        date = str(timezone.localtime(timezone.now()).strftime("%Y-%m-%d"))
        notification.date = date
        notification.user = user_id
        notification.title = subject
        notification.content = line3 + line4
        notification.save()
        email = basic.email
        name = str(basic.first_name) +' ' + str(basic.last_name)
        company_name = company.companyname
        from_email = 'aicwebtestproject@gmail.com'        
        to_list = [email]
        message =''
        html_message = loader.render_to_string(
                'notification_email.html',
                {
                    'name': name,
                    'line1': line1,
                    'line2': line2,
                    'line3': line3,
                    'line4': line4
                }
            )
        try:
            send_mail(subject,message,from_email,to_list,fail_silently=True,html_message=html_message)
        except BadHeaderError:
                return HttpResponse('invalid credentials')
        return redirect(StaffView)
    else:
         return login(request)

def Apply_job(request,job_id):
    if request.method == 'POST':
        form = JobApplicationForm(request.POST,request.FILES)
        if form.is_valid():            
            email = form.cleaned_data.get('email')
            if JobApplication.objects.filter(job_id=job_id,email=email).exists():
                error_no = ''
                error_msg = 'You are already applied for this job'
                return render(request,'error.html',{'error_no':error_no,'error_msg':error_msg})
            else:
                application = JobApplication()      
                career = Careers.objects.get(id=job_id)  
                count = int(career.num_applications) + 1
                country_code = request.POST.get('country_code')
                application.first_name = form.cleaned_data.get('first_name')
                application.last_name = form.cleaned_data.get('last_name')
                application.date = str(timezone.localtime(timezone.now()).strftime("%Y-%m-%d"))
                application.email = form.cleaned_data.get('email')
                application.phone = country_code + str(form.cleaned_data.get('phone'))
                application.qualification = request.POST.get('qualification')
                application.experience = form.cleaned_data.get('experience')
                application.years = form.cleaned_data.get('years')
                application.resume = form.cleaned_data.get('resume')
                application.job_id = job_id
                application.save()
                career.num_applications = count 
                career.save()
                messages.info(request, 'Your application has been submitted successfully!')
                return redirect(careers)
        
                    
        else:
            print(form.errors)
    else:   
        if job_id and Careers.objects.get(id=job_id):
            job = Careers.objects.get(id=job_id)    
            qualification = job.job_qualification
            qualification = qualification.split(",") 
            application_form = JobApplicationForm
            return render(request,'apply_job.html',{'form':application_form,'qualification':qualification,'job':job,'qualification':qualification})
        else:
            error_no = 404 
            error_msg = 'job not found'
            return render(request,'error.html',{'error_no':error_no,'error_msg':error_msg})
    return HttpResponse('error')

@login_required(login_url='/login/')
def ViewJob(request,job_id):
    if request.user.is_authenticated and request.user.type == 'Staff':
        job = Careers.objects.filter(id=job_id)
        if job: 
            job = Careers.objects.get(id=job_id)    
            if request.method == 'POST':
                jobform = AddJobForm(request.POST, request.FILES)
                if jobform.is_valid:
                    job.job_title = request.POST.get('job_title')
                    job.job_description = request.POST.get('job_description')
                    if request.FILES.get('job_pdf'):
                        job.job_pdf = request.FILES.get('job_pdf')
                    job.job_qualification = request.POST.get('job_qualification')
                    if request.POST.get('date'):
                        job.date = request.POST.get('date')
                    job.save()
                else:
                    print('form not valid')
                return redirect(StaffView)
            else:             
                form = AddJobForm()
                form.initial['job_title'] = job.job_title
                form.initial['job_description'] = job.job_description
                form.initial['job_qualification'] = job.job_qualification
                form.initial['job_pdf'] = job.job_pdf
                form.initial['date'] = job.date
                return render(request,'view_job.html',{'form':form,'job':job})
        else:
            error_no = 404 
            error_msg = 'job not found'
            return render(request,'error.html',{'error_no':error_no,'error_msg':error_msg}) 
    else:
        error_no = 404 
        error_msg = 'page not found'
        return render(request,'error.html',{'error_no':error_no,'error_msg':error_msg}) 


@login_required(login_url='/login/')
def deleteJob(request,job_id):
    if request.user.is_authenticated and request.user.type == 'Staff':
        job = Careers.objects.filter(id=job_id)
        if job:
            job.delete()
        else:
            error_no = 404 
            error_msg = 'job not found'
            return render(request,'error.html',{'error_no':error_no,'error_msg':error_msg}) 
        return redirect(StaffView)
    else:
        error_no = 404 
        error_msg = 'page not found'
        return render(request,'error.html',{'error_no':error_no,'error_msg':error_msg}) 

@login_required(login_url='/login/')
def ViewJobApplications(request,job_id):
    if request.user.is_authenticated and request.user.type == 'Staff':
        print('inside')
        application = JobApplication.objects.filter(job_id=job_id)
        job = Careers.objects.filter(id=job_id)
        if application and job:
            application = JobApplication.objects.all()
            job = Careers.objects.get(id=job_id)
            return render(request,'view_job_applications.html',{'application':application,'job':job})
        else:
            return HttpResponse('no applicants for this job')
    else:
        error_no = 404 
        error_msg = 'page not found'
        return render(request,'error.html',{'error_no':error_no,'error_msg':error_msg}) 

def viewApplicantPdf(request,id):
    print(id)
    data = JobApplication.objects.get(id=id)
    path = data.resume
    print(path)
    return FileResponse(open('media/' + str(path), 'rb'), content_type='application/pdf')

@login_required(login_url='/login/')
def ProfileView(request,user_id):
    if request.user.is_authenticated and request.user.type == 'Staff':
        basic = User.objects.get(id=user_id)
        form = StartupContract()
        personal = UserPersonalInfo.objects.get(user_id=user_id)
        p_percentage = getPersonalPercentageStartup(personal)
        if(basic.type == 'Mentor'):
            info = MentorInfo.objects.get(user_id=user_id)
            c_percentage = getCompanyPercentage(info)
        elif(basic.type=='Startup'):
            info = StartupCompanyInfo.objects.get(user_id=user_id)
            c_percentage = getCompanyPercentage(info) 
            print(c_percentage)            
        return render(request, 'profile.html',{'user_id':user_id,'basic':basic,'personal':personal,
        'info':info,'p_percentage':p_percentage,'c_percentage':c_percentage,'contract_form':form})


            
    else:
        error_no = "404 "
        error_msg = "page not found"
        return render(request,'error.html',{'error_no':error_no,'error_msg':error_msg})


@login_required(login_url='/login/')
def uploadStartupContract(request,id):
    if request.user.is_authenticated and request.user.type == 'Staff' and request.method == 'POST':
        startup = StartupCompanyInfo.objects.filter(user_id=id)
        if startup:
            startup_data = StartupCompanyInfo.objects.get(user_id=id)
            form = StartupContract(request.POST,request.FILES)
            if form.is_valid():
                contract_date = form.cleaned_data.get('contract_date')
                contract_expiry = form.cleaned_data.get('contract_expiry')
                contract_pdf = form.cleaned_data.get('contract_pdf')
                if contract_date and contract_expiry and contract_pdf:
                    startup_data.contract_date = contract_date
                    startup_data.contract_expiry = contract_expiry
                    startup_data.contract_pdf = contract_pdf
                    startup_data.save()
                else: 
                    print('failed')
                
            else:
                print(form.errors)
            return redirect(StaffView)
        else:
            error_no = 404 
            error_msg = 'user not found'
            return render(request,'error.html',{'error_no':error_no,'error_msg':error_msg}) 
    elif request.user.is_authenticated and request.user.type == 'Staff' and request.method == 'GET':
        form = StartupContract()
        return render(request,'uploadcontract.html',{'user_id':id,'form':form})
    else:
        error_no = 404 
        error_msg = 'page not found'
        return render(request,'error.html',{'error_no':error_no,'error_msg':error_msg}) 

        
@login_required(login_url='/login/')
def incubateStartup(request,id):
    if request.user.is_authenticated and request.user.type == 'Staff':
        basic_data = User.objects.get(id=id)
        basic_data.approved = True
        basic_data.save()
        return redirect('/profile/' + str(id) + '/')
    else:
        error_no = 404 
        error_msg = 'page not found'
        return render(request,'error.html',{'error_no':error_no,'error_msg':error_msg}) 
