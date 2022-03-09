from email.policy import default
from django.db import DatabaseError, models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
   type = models.CharField(choices=(("Staff","Staff"),("Startup", "Startup"),("Mentor", "Mentor")), max_length=20,default='Staff')
   terms_and_conditions_confirmed = models.BooleanField(default=0)
   profile_pic =  models.ImageField(upload_to="images/",default='null')
   approved = models.BooleanField(default=False)
   profile_locked = models.BooleanField(default=False)

class emailOTP(models.Model):
    email = models.EmailField(primary_key=True)
    otp = models.CharField(max_length=10)

class UserPersonalInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    gender = models.CharField(max_length=20)
    place = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    whatsappnumber = models.CharField(max_length=15)
    profilepic = models.ImageField(upload_to="images/")   

class StartupCompanyInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    companyname = models.CharField(max_length=255)
    registration_year = models.CharField(default='',max_length=255)
    date_of_incubation = models.CharField(default='',max_length=255)
    type_of_incubation = models.CharField(max_length=255)
    sector = models.CharField(max_length=255)
    operational_model = models.TextField()
    target_market = models.CharField(max_length=255)
    cin_number = models.CharField(max_length=255)
    dipp_number = models.CharField(max_length=255)
    founder = models.CharField(max_length=255)
    num_directors = models.CharField(max_length=255)
    num_women_dir = models.CharField(max_length=255)
    stage = models.CharField(max_length=255)
    employees = models.CharField(max_length=255)
    webpage = models.CharField(max_length=255)
    msme_registration = models.CharField(max_length=255)
    flagship_program = models.CharField(max_length=255)    
    nature_of_firm = models.CharField(max_length=255)
    company_address = models.TextField()    
    intelectual_property = models.BooleanField(default=False)
    i_property_type = models.CharField(max_length=255)
    number_of_ip = models.CharField(max_length=10)    
    funding = models.CharField(max_length=255)    
    academic_qualification_founder = models.CharField(max_length=255)
    field_of_study = models.CharField(max_length=255)
    experience_of_founder = models.CharField(max_length=255)
    core_competancy = models.CharField(max_length=255)
    expectation = models.TextField()
    company_logo = models.FileField(upload_to='company_logo/')
    startup_pitch = models.FileField(upload_to='pitch/')
    about = models.TextField()
    other_info = models.TextField()
    applied_for_incubation = models.BooleanField(default=False)
    contract_date = models.CharField(max_length=255)
    contract_expiry = models.CharField(max_length=255)
    contract_pdf = models.FileField(upload_to='contracts/')
    
    
class MentorInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    username = models.CharField(primary_key = True,max_length=100)
    Designation = models.CharField(max_length=100)
    Current_working_company = models.CharField(max_length=100)
    Previous_working_experience = models.TextField()
    supported_any_startup  = models.BooleanField(default=False)
    Working_Domain =  models.CharField(max_length=100)
    areas_of_expertise = models.CharField(max_length=255)
    Presently_residing = models.TextField()
    Bachelors_Degree = models.BooleanField(default=False)
    Masters_Degree = models.BooleanField(default=False)
    PHD = models.BooleanField(default=False)
    B_Institute = models.CharField(max_length=255)
    M_Institute = models.CharField(max_length=255)
    P_Institute = models.CharField(max_length=255)
    B_Subject = models.CharField(max_length=255)
    M_Subject = models.CharField(max_length=255)
    P_Subject = models.CharField(max_length=255)
    experience_as_mentor = models.CharField(max_length=255,default='null')
    contribution_to_startup_echosystem = models.TextField(default='null')
    post_doctorate = models.BooleanField(default=False)
    post_doctorate_domain = models.CharField(max_length=255,default='null')

class User_Posts(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    post_time = models.CharField(max_length=255)
    post_title = models.CharField(max_length=255)
    post_content = models.TextField()
    post_photo = models.ImageField(upload_to="post_images/")
    like_count = models.CharField(max_length=255,default=0)
    comment_count = models.CharField(max_length=255,default=0)

class User_Comments(models.Model):
    post_id = models.IntegerField()
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,max_length=255)
    like_count = models.IntegerField(default=0)
    reply_count = models.IntegerField(default=0)
    comment_content = models.TextField()
    comment_time =  models.CharField(max_length=255)
    
class User_Liked(models.Model):
    post_id = models.ForeignKey(User_Posts,on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    is_liked = models.BooleanField(default=False)
class Comment_Replies(models.Model):
    comment_id = models.ForeignKey(User_Comments,on_delete=models.CASCADE)
    reply_content =  models.TextField()



