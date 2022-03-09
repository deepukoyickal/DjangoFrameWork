from django.db import models

class News(models.Model):
    date = models.DateField(max_length=255)
    title = models.CharField(max_length=255)
    content = models.TextField()
    pdf =  models.FileField(upload_to='news/')

class Appointment(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    mobile = models.CharField(max_length=20,default='null')
    date = models.CharField(max_length=30)
    time = models.CharField(max_length=20)
    purpose = models.TextField()
    fixed = models.BooleanField(default=False)

class OurTeam(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    fb_link = models.CharField(max_length=255,default='null')
    twitter_link = models.CharField(max_length=255,default='null')
    insta_link = models.CharField(max_length=255,default='null')
    linkedin_link = models.CharField(max_length=255,default='null')
    profile_pic =  models.FileField(upload_to='our_team/')

class Gallery(models.Model):
    path = models.FileField(upload_to='gallery/')
    description = models.TextField()

class BoardMembers(models.Model):
    path = models.FileField(upload_to='board_members/')
    name = models.CharField(max_length=255)
    designation1 = models.CharField(max_length=255)
    designation2 = models.CharField(max_length=255) 

class Careers(models.Model):
    job_title = models.CharField(max_length=255)
    job_description = models.TextField()
    job_pdf = models.FileField(upload_to='careers/')
    job_qualification = models.TextField()
    date = models.DateField(max_length=255)
    num_applications = models.IntegerField(default=0)

class QueriesAndReviews(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    content = models.TextField()
    date = models.DateTimeField()

class Events(models.Model):
    event_title = models.CharField(max_length=255)
    organizers = models.TextField()
    event_content = models.TextField()
    start_date  = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=255)
    more_info = models.FileField(upload_to='events/')

class Notifications(models.Model):
     date  = models.DateField()
     title = models.CharField(max_length=255)
     content = models.TextField()
     user = models.BigIntegerField()


class JobApplication(models.Model):
    date = models.DateField()
    job = models.ForeignKey(Careers,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    qualification = models.CharField(max_length=255)
    experience = models.BooleanField(default=False)
    years = models.CharField(max_length=10)
    resume = models.FileField(upload_to='resumes/')


