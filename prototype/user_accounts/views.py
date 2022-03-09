from django.shortcuts import render,redirect
from django.contrib.auth.models import auth
from django.contrib import messages

from services.models import Notifications
from . forms import BasicInfo, MentorInfoAcademic, MentorInfoCareer, Registration,LoginForm, PersonalInfo, CompanyInfo, OtherCompanyInfo, User_social_posts, addLikesToPosts, saveOTP, saveOTP, addCommentsToPosts
from django.contrib.auth import get_user_model
from django.http import BadHeaderError, FileResponse, HttpResponse
from .models import User_Comments, User_Posts, UserPersonalInfo, StartupCompanyInfo, emailOTP, MentorInfo, User_Liked, User_Comments
# from django.contrib.auth.models import User
import random
from django.core.mail import send_mail
from .models import User
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.template import loader

def getOTP(request):
    User = get_user_model()
    otpform = saveOTP()
    if request.method == 'POST':  
        email = request.POST['email'] 
        if User.objects.filter(username=email).exists():
            messages.error(request,'email id already taken!!')
            return render(request, 'otp_form.html', {'otpform':otpform})

        otp = random.randint(100000,999999)
        otpmodel = emailOTP(email=email,otp=otp)
        otpmodel.save()
        subject = "OTP"
        from_email = 'aicwebtestproject@gmail.com'
        to_list = [email]
        message = ''
        html_message = loader.render_to_string(
                'otp_template.html',
                {
                    'name': email.split("@")[0],
                    'otp':  otp,
                }
            )
        try:
            send_mail(subject,message,from_email,to_list,fail_silently=True,html_message=html_message)
        except BadHeaderError:
                return HttpResponse('invalid credentials')
        otpform.initial['conf_email'] = email
        otpform.initial['resend_email'] = email
        return render(request, 'otp_confirmation.html', {'otpform':otpform})
    else:
        return render(request, 'otp_form.html', {'otpform':otpform})


def resendOTP(request):
    otpform = saveOTP()
    if request.method == 'POST':  
        email = request.POST['resend_email']  
        otp = random.randint(1000,9999)
        otpmodel = emailOTP(email=email,otp=otp)
        otpmodel.save()
        htmlgen = '<p>Your OTP is <strong>'+str(otp)+'</strong></p>'
        send_mail('OTP request',str(otp),'aicwebtestproject@gmail.com',[email], fail_silently=False, html_message=htmlgen)
    return render(request, 'otp_confirmation.html', {'otpform':otpform})

def verfiyOTP(request):
    if request.method == 'POST':
        otpform = saveOTP()
        email = request.POST['conf_email']
        otp= request.POST['otp']
        otpmodel = emailOTP.objects.get(email=email)
        if otpmodel.otp == otp:
            form = Registration()
            otpmodel.delete()
            form.initial['email'] = email
            return render(request, 'register.html', {'form': form})
        else:
            messages.error(request,'invalid OTP')
            return render(request, 'otp_form.html', {'otpform':otpform})


def userRegistration(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['email']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        type = request.POST['userType']
        terms_and_conditions_confirmed 	 = request.POST['terms']
        if terms_and_conditions_confirmed == 'on':
            terms_and_conditions_confirmed = True
        else:
            terms_and_conditions_confirmed = False
        User = get_user_model()
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, "User name is already Taken")
                return redirect('userRegistration')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email is already Taken")
                return redirect('userRegistration')
            else:
                user = User.objects.create_user(username=username, password=password,
                email=email,first_name=first_name,last_name=last_name,type=type,terms_and_conditions_confirmed=terms_and_conditions_confirmed)
                user.save()                
                data = UserPersonalInfo(user_id=user.id)
                if type == 'Startup':
                    company = StartupCompanyInfo(user_id=user.id)
                    company.save()
                elif type == 'Mentor':
                    mentor = MentorInfo(user_id=user.id)
                    mentor.save()                
                data.save()
                return redirect('login')
        else:
            messages.info(request, "Password does not match")
            return redirect('userRegistration')
    else:
        form = Registration()
        otpform = saveOTP()
        return render(request, 'otp_form.html', {'otpform':otpform})


def login(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            form = LoginForm()
            messages.error(request,'invalid user name or password')
            return render(request, 'login.html', {'form': form} )        
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

def logout(request):
    auth.logout(request)
    return redirect('index')
    
@login_required(login_url='/login/')
def Mentorprofile(request):
    user_id = request.user.id
    p_total_columns = 8
    o_total_columns = 20
    count = 0
    data = UserPersonalInfo.objects.get(user_id=user_id)
    cAcademic = MentorInfo.objects.get(user_id=user_id)
    if data.gender == 'null' or data.gender == '':
        count = int(count+1)
    if data.place == 'null' or data.place == '':
        count = int(count+1)
    if data.contact_number == 'null' or data.contact_number == '':
        count = int(count+1)
    if data.address == 'null' or data.address == '':
        count = int(count+1)
    if data.whatsappnumber == 'null' or data.whatsappnumber == '':
        count = int(count+1)
    if data.profilepic == 'null' or data.profilepic == '':
        count = int(count+1)
    p_percentage=int((count/p_total_columns)*100)
    personal = int(100-p_percentage)
   

    count=0
    if cAcademic.Designation == 'null' or cAcademic.Designation == '':
        count = int(count+1)

    if cAcademic.Current_working_company == 'null' or cAcademic.Current_working_company == '':
        count = int(count+1)

    if cAcademic.Previous_working_experience == 'null' or cAcademic.Previous_working_experience == '':
        count = int(count+1)

    if cAcademic.supported_any_startup == 'null' or cAcademic.supported_any_startup == '':
        count = int(count+1)

    if cAcademic.Working_Domain == 'null' or cAcademic.Working_Domain == '':
        count = int(count+1)

    if cAcademic.areas_of_expertise == 'null' or cAcademic.areas_of_expertise == '':
        count = int(count+1)

    if cAcademic.Presently_residing == 'null' or cAcademic.Presently_residing == '':
        count = int(count+1)

    if cAcademic.Bachelors_Degree == False or cAcademic.Bachelors_Degree == '':
        count = int(count+1)

    if cAcademic.Masters_Degree == False or cAcademic.Masters_Degree == '':
        count = int(count+1)

    if cAcademic.PHD == False or cAcademic.PHD == '':
        count = int(count+1)

    if cAcademic.experience_as_mentor == 'null' or cAcademic.experience_as_mentor == '':
        count = int(count+1)

    if cAcademic.contribution_to_startup_echosystem == 'null' or cAcademic.contribution_to_startup_echosystem == '':
        count = int(count+1)

    if cAcademic.post_doctorate == 'null' or cAcademic.post_doctorate == '':
        count = int(count+1)
    
    career_percentage=int((count/o_total_columns)*100)
    career = int(100-career_percentage)    
    mentor_personal = PersonalInfo()
    mentor_basic = BasicInfo()
    mentor_career = MentorInfoCareer()
    mentor_academic = MentorInfoAcademic()        
    user = User.objects.get(id=user_id)
    user_info = UserPersonalInfo.objects.get(user_id=user_id)
    mentor_info = MentorInfo.objects.get(user_id=user_id)
    mentor_basic.initial['first_name'] = user.first_name
    mentor_basic.initial['last_name'] = user.last_name
    mentor_basic.initial['email'] = user.email
    mentor_personal.initial['place'] = user_info.place
    mentor_personal.initial['contact_number'] = user_info.contact_number
    mentor_personal.initial['address'] = user_info.address
    mentor_personal.initial['whatsappnumber'] = user_info.whatsappnumber
    mentor_personal.initial['gender'] = user_info.gender
    mentor_career.initial['Designation'] = mentor_info.Designation
    mentor_career.initial['Current_working_company'] = mentor_info.Current_working_company
    mentor_career.initial['Previous_working_experience'] = mentor_info.Previous_working_experience
    mentor_career.initial['supported_any_startup'] = mentor_info.supported_any_startup
    mentor_career.initial['Working_Domain'] = mentor_info.Working_Domain
    mentor_career.initial['Presently_residing'] = mentor_info.Presently_residing
    mentor_academic.initial['Bachelors_Degree'] = mentor_info.Bachelors_Degree
    mentor_academic.initial['Masters_Degree'] = mentor_info.Masters_Degree
    mentor_academic.initial['PHD'] = mentor_info.PHD
    mentor_academic.initial['B_Institute'] = mentor_info.B_Institute
    mentor_academic.initial['M_Institute'] = mentor_info.M_Institute
    mentor_academic.initial['P_Institute'] = mentor_info.P_Institute
    mentor_academic.initial['B_Subject'] = mentor_info.B_Subject
    mentor_academic.initial['M_Subject'] = mentor_info.M_Subject
    mentor_academic.initial['P_Subject'] = mentor_info.P_Subject

    return render(request, 'mentorprofile.html', {'mentor_personal': mentor_personal, 'mentor_basic': mentor_basic,
     'mentor_career': mentor_career, 'mentor_academic': mentor_academic, 'user': user, 
     'user_info': user_info, 'mentor_info': mentor_info, 'personal':personal,'career':career})

@login_required(login_url='/login/')
def SavePersonalInfo(request):
    if request.method == 'POST' and request.user.profile_locked == False:
        user_id = request.user.id
        basic = User.objects.get(id=user_id)  
        data = UserPersonalInfo()
        personalinformation = PersonalInfo(request.POST, request.FILES)
        basicInformation = BasicInfo(request.POST, request.FILES)
        userObj = get_user_model()    
        if personalinformation.is_valid():
            data = UserPersonalInfo.objects.get(user_id=user_id)                  
            data.place = personalinformation.cleaned_data.get("place")
            data.contact_number = personalinformation.cleaned_data.get("contact_number")
            data.address = personalinformation.cleaned_data.get("address")
            data.whatsappnumber = personalinformation.cleaned_data.get("whatsappnumber")
            data.gender = personalinformation.cleaned_data.get("gender")
            profilepic = personalinformation.cleaned_data.get("profilepic")
            if profilepic:
                data.profilepic = profilepic
            data.save()       
            basic.profile_pic = data.profilepic
            basic.save()

        if basicInformation.is_valid():
            user = userObj.objects.get(id=user_id)     
            user.first_name = basicInformation.cleaned_data.get("first_name")
            user.last_name = basicInformation.cleaned_data.get("last_name")
            user.save()
        else:
            print('basic form is not valid' + str(basicInformation.errors))

        return HttpResponse("<h2>saved data successfully</h2>")
    else:
        error_no = "403 Forbbiden"
        error_msg = "You can't edit your profile. your application for incubation is under process"
        return render(request,'error.html',{'error_no':error_no,'error_msg':error_msg})


@login_required(login_url='/login/')
def SaveCompanyInfo(request):
    user_id = request.user.id   
    if request.method == 'POST' and request.user.profile_locked == False:
        data = StartupCompanyInfo()
        insertform = CompanyInfo(request.POST, request.FILES)
        if insertform.is_valid():
            data = StartupCompanyInfo.objects.get(user_id=user_id)
            data.companyname = insertform.cleaned_data.get("companyname")
            data.cin_number = insertform.cleaned_data.get("cin_number")
            data.dipp_number = insertform.cleaned_data.get("dipp_number")
            data.founder = insertform.cleaned_data.get("founder")
            data.num_directors = insertform.cleaned_data.get("num_directors")
            data.num_women_dir = insertform.cleaned_data.get("num_women_dir")
            data.stage = insertform.cleaned_data.get("stage")
            data.employees = insertform.cleaned_data.get("employees")
            data.webpage = insertform.cleaned_data.get("webpage")
            data.msme_registration = insertform.cleaned_data.get("msme_registration")
            data.flagship_program = insertform.cleaned_data.get("flagship_program") 
            data.about = insertform.cleaned_data.get("about")
            data.nature_of_firm = insertform.cleaned_data.get("nature_of_firm")
            data.company_address = insertform.cleaned_data.get("company_address")
            startup_pitch = insertform.cleaned_data.get("startup_pitch")
            data.intelectual_property = insertform.cleaned_data.get("intelectual_property")
            if insertform.cleaned_data.get('i_property_type'):
                data.number_of_ip = insertform.cleaned_data.get('number_of_ip')
                data.i_property_type = insertform.cleaned_data.get('i_property_type')
            data.year = insertform.cleaned_data.get('year_of_registration')
            data.funding = insertform.cleaned_data.get('funding')
            logo = insertform.cleaned_data.get('company_logo')
            if logo:
                data.company_logo = logo 
            if startup_pitch:
                data.startup_pitch = startup_pitch            
            data.type_of_incubation = insertform.cleaned_data.get('type_of_incubation')
            data.sector = insertform.cleaned_data.get('sector')
            data.operational_model = insertform.cleaned_data.get('operational_model')
            data.target_market = insertform.cleaned_data.get('target_market')
            registration_year = insertform.cleaned_data.get('year_of_registration')
            if registration_year:
                data.registration_year = registration_year
            data.save()
            return HttpResponse("<h2>saved data successfully</h2>")
    else:
        error_no = "403 Forbbiden"
        error_msg = "You can't edit your profile. your application for incubation is under process"
        return render(request,'error.html',{'error_no':error_no,'error_msg':error_msg})


@login_required(login_url='/login/')
def SaveOtherInfo(request):
    user_id = request.user.id  
    if request.method == 'POST':
        data = StartupCompanyInfo()
        insertform = OtherCompanyInfo(request.POST, request.FILES)
        if insertform.is_valid():
            data = StartupCompanyInfo.objects.get(user_id=user_id)
            data.academic_qualification_founder = insertform.cleaned_data.get("academic_qualification_founder")
            data.field_of_study = insertform.cleaned_data.get("field_of_study")
            data.experience_of_founder = insertform.cleaned_data.get("experience_of_founder")
            data.core_competancy = insertform.cleaned_data.get("core_competancy")
            data.expectation = insertform.cleaned_data.get("expectation")
            data.other_info = insertform.cleaned_data.get("other_info")
            data.save()
        else:
            print('form is not valid')
        return HttpResponse("saved")
    else:
        error_no = "403 Forbbiden"
        error_msg = "You can't edit your profile. your application for incubation is under process"
        return render(request,'error.html',{'error_no':error_no,'error_msg':error_msg})


@login_required(login_url='/login/')
def SaveCareerInfo(request):
    username = request.user.username
    if request.method == 'POST':
        mentorForm = MentorInfoCareer(request.POST, request.FILES)
        if mentorForm.is_valid():
            data = MentorInfo.objects.get(username=username)
            data.Designation = mentorForm.cleaned_data.get("Designation")
            data.Current_working_company = mentorForm.cleaned_data.get("Current_working_company")
            data.Previous_working_experience = mentorForm.cleaned_data.get("Previous_working_experience")
            data.supported_any_startup  = mentorForm.cleaned_data.get("supported_any_startup")
            data.Working_Domain = mentorForm.cleaned_data.get("Working_Domain")
            data.areas_of_expertise = mentorForm.cleaned_data.get("areas_of_expertise")
            data.Presently_residing = mentorForm.cleaned_data.get("Presently_residing")
            data.experience_as_mentor = mentorForm.cleaned_data.get("experience_as_mentor")
            data.contribution_to_startup_echosystem = mentorForm.cleaned_data.get("contribution_to_startup_echosystem")
            data.save()
        else:
            print('form is not valid:' + str(mentorForm.errors))
        return HttpResponse("saved")

@login_required(login_url='/login/')
def SaveAcademicInfo(request):
    username = request.user.username
    if request.method == 'POST':
        mentorForm = MentorInfoAcademic(request.POST, request.FILES)
        if mentorForm.is_valid():
            data = MentorInfo.objects.get(username=username)
            Bachelors_Degree = mentorForm.cleaned_data.get("Bachelors_Degree")            
            if Bachelors_Degree == True:
                data.B_Institute = mentorForm.cleaned_data.get("B_Institute")
                data.B_Subject = mentorForm.cleaned_data.get("B_Subject")
            else:
                data.B_Institute = ''
                data.B_Subject = ''
            data.Bachelors_Degree = Bachelors_Degree

            Masters_Degree = mentorForm.cleaned_data.get("Masters_Degree")
            if Masters_Degree == True:
                data.M_Institute = mentorForm.cleaned_data.get("M_Institute")
                data.M_Subject = mentorForm.cleaned_data.get("M_Subject")
            else:
                data.M_Institute = ''
                data.M_Subject = ''
            data.Masters_Degree = Masters_Degree

            PHD = mentorForm.cleaned_data.get("PHD")
            if PHD == True:
                data.P_Institute = mentorForm.cleaned_data.get("P_Institute")
                data.P_Subject = mentorForm.cleaned_data.get("P_Subject")
            else:
                data.P_Institute = ''
                data.P_Subject = ''
            data.PHD = PHD

            post_doctorate = mentorForm.cleaned_data.get("post_doctorate")
            if post_doctorate == True:
                data.post_doctorate_domain = mentorForm.cleaned_data.get("post_doctorate_domain")
            else:
                data.post_doctorate_domain = ''
            data.post_doctorate = post_doctorate
            data.save()
        else:
            print('form is not valid' + str(mentorForm.errors))
        return HttpResponse("saved")

@login_required(login_url='/login/')
def viewForum(request):
    user_post_form = User_social_posts()
    user_posts = User_Posts.objects.order_by('-post_time')
    user_info = UserPersonalInfo.objects.all()
    like_info = User_Liked.objects.all()
    like_count_form = addLikesToPosts()
    comment_count_form = addCommentsToPosts()
    user_comments = User_Comments.objects.order_by('-comment_time')
    return render(request,'forum.html',{'user_post_form':user_post_form,'user_posts':user_posts,'user_info':user_info,'like_info':like_info,'like_count_form':like_count_form,'comment_count_form':comment_count_form,'user_comments':user_comments})

@login_required(login_url='/login/')
def savePost(request):
    if request.method == 'POST':
        username = request.user.username
        # post_id = username + str(timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S"))
        post_time = str(timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S"))
        post_form = User_social_posts(request.POST, request.FILES)
        if post_form.is_valid():
            post_title = post_form.cleaned_data.get("post_title")
            post_content = post_form.cleaned_data.get("post_content")
            post_photo = post_form.cleaned_data.get("post_photo")
            data = User_Posts(username_id=request.user.id,post_time=post_time,post_title=post_title,post_content=post_content,post_photo=post_photo)
            data.save()
            return HttpResponse('saved')
        else:
            print(str(post_form.errors) + 'error')
            return HttpResponse('not valid')
    else:
        print('not post method')

@login_required(login_url='/login/')
def addLikes(request):
    if request.method == 'POST':
        user = request.user.id
        likeModel = User_Liked()
        like_form = addLikesToPosts(request.POST, request.FILES)
        if like_form.is_valid():
            id = request.POST.get('post_id')
            if not User_Liked.objects.filter(post_id_id=id,is_liked=1,user_id=user).exists():
                data = User_Posts.objects.get(id=id)
                is_liked_data = User_Liked(post_id_id=id,user_id=user,is_liked=True)
                count = like_form.cleaned_data.get('like_count')
                count = int(count) + 1
                data.like_count = count
                data.save()
                is_liked_data.save()
            else:
                print("already liked")
        else:
            print('not valid' + str(like_form.errors))
        return HttpResponse('')

@login_required(login_url='/login/')
def postComments(request):
    if request.method == 'POST':
        user = request.user.id
        commentModel = User_Comments()
        comment_time = str(timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S"))
        comment_form = addCommentsToPosts(request.POST, request.FILES)
        if comment_form.is_valid():
            id = request.POST.get('post_id')
            data = User_Posts.objects.get(id=id)
            comment_count = request.POST.get('comment_count')
            comment_count = int(comment_count) + 1
            content = comment_form.cleaned_data.get('comment_content')
            comment_data = User_Comments(post_id=id,user_id_id=user,comment_content=content,comment_time=comment_time)
            comment_data.save()
            print(id)
            print(comment_count)
            print(content)
            print(user)
            data.comment_count = comment_count
            data.save()
        else:
            print("form is not valid" + str(comment_form.errors))
        return HttpResponse('')

@login_required(login_url='/login/')
def viewComments(request,post_id):
    post_data =  User_Posts.objects.get(id=post_id)
    comment_data = User_Comments.objects.filter(post_id=post_id)
    return render(request,"comments.html",{'data':post_data,'comment':comment_data})

@login_required(login_url='/login/')
def likeComment(request):
    if request.method == 'POST':
        user = request.user.id
        like_form = addLikesToPosts(request.POST, request.FILES)
        if like_form.is_valid():
            id = request.POST.get('comment_id')
            data = User_Comments.objects.get(id=id)
            count = like_form.cleaned_data.get('like_count')
            count = int(count) + 1
            data.like_count = count
            data.save()
        else:
            print('not valid' + str(like_form.errors))
        return HttpResponse('')


@login_required(login_url='/login/')
def viewPdf(request,user_id):
    data = StartupCompanyInfo.objects.get(user_id=user_id)
    path = data.startup_pitch
    return FileResponse(open('media/' + str(path), 'rb'), content_type='application/pdf')

def about(request):
    return render(request,'about.html')
    
def deleteUser(request):
   if request.method == 'POST':
    user_id = request.POST.get('user_id')
    User.objects.filter(id=user_id).delete()
    return HttpResponse()

def approveUser(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        data = User.objects.get(id=user_id)
        if data.approved == False:
            data.approved = True 
        else:
            data.approved = False 
        data.save()
        return HttpResponse('updated')

@login_required(login_url='/login/')
def applyIncubation(request):    
    if request.method == 'POST':
        user_id = request.user.id
        data = StartupCompanyInfo.objects.get(user_id=user_id)
        basic = User.objects.get(id=user_id)
        data.applied_for_incubation = True
        basic.profile_locked = True
        data.save()
        basic.save()
        return Startup_home(request)
    else:
        return HttpResponse('page not found')

@login_required(login_url='/login/')
def cancelIncubation(request):    
    if request.method == 'POST':
        user_id = request.user.id
        data = StartupCompanyInfo.objects.get(user_id=user_id)
        data.applied_for_incubation = 0
        data.save()
        print(data)
        return HttpResponse('')
    else:
        return HttpResponse('page not found')


def Startup_home(request):
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    user_info = UserPersonalInfo.objects.get(user_id=user_id)
    company_info = StartupCompanyInfo.objects.get(user_id=user_id)
    personal = getPersonalPercentageStartup(user_info,user)
    comapny_percentage = getCompanyPercentage(company_info)
    notifications = Notifications.objects.order_by('-date')
    not_count = Notifications.objects.filter(user=user_id).count()
    return render(request,'startup_profile.html',{'user_info':user_info,'company_info':company_info,'personal':personal,
    'comapny_percentage':comapny_percentage,'notifications':notifications,'not_count':not_count})

@login_required(login_url='/login/')
def Startupprofile(request):
    user_id= request.user.id
    user = User.objects.get(id=user_id)
    user_info = UserPersonalInfo.objects.get(user_id=user_id)
    company_info = StartupCompanyInfo.objects.get(user_id=user_id)
    if  not company_info.applied_for_incubation or user.approved:
        form1 = PersonalInfo(initial={'place':user_info.place,'contact_number':user_info.contact_number,'address':user_info.address,
        'whatsappnumber':user_info.whatsappnumber,'gender':user_info.gender})
        form2 = BasicInfo(initial={'first_name':user.first_name,'last_name':user.last_name,'profilepic':user_info.profilepic})
        form3 = CompanyInfo(initial={'companyname':company_info.companyname,'year_of_registration':company_info.registration_year,'type_of_incubation':company_info.type_of_incubation,
        'cin_number':company_info.cin_number,'dipp_number':company_info.dipp_number,'founder':company_info.founder,'num_directors':company_info.num_directors,
        'num_women_dir':company_info.num_women_dir,'stage':company_info.stage,'employees':company_info.employees,'webpage':company_info.webpage,
        'msme_registration':company_info.msme_registration,'flagship_program':company_info.flagship_program,'about':company_info.about,'nature_of_firm':company_info.nature_of_firm,
        'company_address':company_info.company_address,'sector':company_info.sector,'operational_model':company_info.operational_model,'target_market':company_info.target_market})
        form4 = OtherCompanyInfo(initial={'academic_qualification_founder':company_info.academic_qualification_founder,'field_of_study':company_info.field_of_study,
        'experience_of_founder':company_info.experience_of_founder,'core_competancy':company_info.core_competancy,'expectation':company_info.expectation,
        'other_info':company_info.other_info})
        personal = getPersonalPercentageStartup(user_info,user)
        comapny_percentage = getCompanyPercentage(company_info)
        
        
        
        return render(request, 'startupprofile.html', {'form1': form1, 'form2': form2 , 'form3': form3, 'form4': form4,
        'user': user, 'user_info': user_info,'company_info': company_info,'personal':personal,'comapny_percentage':comapny_percentage
        })
    else:
        error_no = "403 Forbbiden"
        error_msg = str(user.approved) + "You can't edit your profile. your application for incubation is under process"
        return render(request,'error.html',{'error_no':error_no,'error_msg':error_msg})




def getPersonalPercentageStartup(user_info,base_info):
    personal_fields = 8
    count = 0
    if base_info.first_name == '' or base_info.first_name == 'null':
        count = count + 1
    if base_info.last_name == '' or base_info.last_name == 'null':
        count = count + 1
    if user_info.place == '' or user_info.place == 'null':
        count = count + 1
    if user_info.contact_number == '' or user_info.contact_number == 'null':
        count = count + 1
    if user_info.address == '' or user_info.address == 'null':
        count = count + 1
    if user_info.whatsappnumber == '' or user_info.whatsappnumber == 'null':
        count = count + 1
    if user_info.gender == '' or user_info.gender == 'null':
        count = count + 1
    if user_info.profilepic == '' or user_info.profilepic == 'null':
        count = count + 1

    p_percentage=int((count/personal_fields)*100)
    personal = int(100-p_percentage)
    return personal

def getCompanyPercentage(company_info):
    company_fields = 29 
    count = 0
    if company_info.companyname == 'null' or company_info.companyname == '':
        count = count + 1
    if company_info.registration_year  == 'null' or company_info.registration_year  == '':
        count = count + 1        
    if company_info.type_of_incubation  == 'null' or company_info.type_of_incubation == '':
        count = count + 1
    if company_info.sector  == 'null' or company_info.sector  == '':
        count = count + 1
    if company_info.operational_model  == 'null' or company_info.operational_model  == '':
        count = count + 1
    if company_info.target_market  == 'null' or company_info.target_market  == '':
        count = count + 1
    if company_info.cin_number  == 'null' or company_info.cin_number  == '':
        count = count + 1
    if company_info.dipp_number  == 'null' or company_info.dipp_number  == '':
        count = count + 1
    if company_info.founder  == 'null' or company_info.founder == '':
        count = count + 1
    if company_info.num_directors  == 'null' or company_info.num_directors  == '':
        count = count + 1
    if company_info.num_women_dir  == 'null' or company_info.num_women_dir == '':
        count = count + 1
    if company_info.employees  == 'null' or company_info.employees == '':
        count = count + 1
    if company_info.stage  == 'null' or company_info.stage == '':
        count = count + 1
    if company_info.webpage  == 'null' or company_info.webpage  == '':
        count = count + 1
    if company_info.msme_registration  == 'null' or company_info.msme_registration  == '':
        count = count + 1
    if company_info.flagship_program  == 'null' or company_info.flagship_program  == '':
        count = count + 1
    if company_info.nature_of_firm  == 'null' or company_info.nature_of_firm == '':
        count = count + 1
    if company_info.company_address  == 'null' or company_info.company_address == '':
        count = count + 1
    if company_info.intelectual_property  == 'null' or company_info.intelectual_property  == '':
        count = count + 1
    if company_info.funding  == 'null' or company_info.funding  == '':
        count = count + 1
    if company_info.academic_qualification_founder  == 'null' or company_info.academic_qualification_founder == '':
        count = count + 1
    if company_info.field_of_study  == 'null' or company_info.field_of_study == '':
        count = count + 1
    if company_info.experience_of_founder  == 'null' or company_info.experience_of_founder == '':
        count = count + 1
    if company_info.core_competancy  == 'null' or company_info.core_competancy  == '':
        count = count + 1
    if company_info.expectation  == 'null' or company_info.expectation  == '':
        count = count + 1
    if company_info.company_logo  == 'null' or company_info.company_logo  == '':
        count = count + 1 
    if company_info.startup_pitch  == 'null' or company_info.startup_pitch  == '':
        count = count + 1
    if company_info.about  == 'null' or company_info.about == '':
        count = count + 1
    if company_info.other_info  == 'null' or company_info.other_info  == '':
        count = count + 1 
    c_percentage = int((count/company_fields)*100)
    company_percentage = int(100-c_percentage)
    print(count)
    return company_percentage