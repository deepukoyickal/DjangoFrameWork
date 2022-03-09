from cProfile import label
from random import choice
from select import select
from django import forms
from user_accounts.forms import YESNO
from user_accounts.models import StartupCompanyInfo
from services.models import Careers, Events, Gallery, JobApplication, News, OurTeam, QueriesAndReviews

CODE = [('+91','+91')]

class NewsForm(forms.ModelForm):
    date = forms.DateTimeField(required=False)
    title = forms.CharField(label="title",max_length=255)
    content = forms.CharField( label="News Content", widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))
    pdf =  forms.FileField(label="Upload pdf(supported formats:*pdf,*pptx)", required=False, widget=forms.ClearableFileInput(attrs={'id':"news_pdf"}))
    class Meta:
        model = News
        fields = ('title','content','pdf')

class AddTeamMember(forms.ModelForm):
    first_name = forms.CharField(label="First Name",max_length=255)
    last_name = forms.CharField(label="Last Name",max_length=255)
    designation = forms.CharField(label="Designation",max_length=255)
    phone = forms.CharField(label="Phone",max_length=20)
    fb_link = forms.CharField(label="Facebook profile Link",max_length=255,required=False)
    twitter_link = forms.CharField(label="Twitter profile link",max_length=255,required=False)
    insta_link = forms.CharField(label="Instagram link",max_length=255,required=False)
    linkedin_link = forms.CharField(label="Linkedin profile",max_length=255,required=False)
    profile_pic =  forms.FileField(label="Upload profile pic(supported formats:*jpg,*jpeg,*png)", required=False,widget=forms.ClearableFileInput(attrs={'id':"member_pic"}))

    class Meta:
        model = OurTeam
        fields = ('first_name','last_name','designation','phone','fb_link','twitter_link','insta_link','insta_link','linkedin_link','profile_pic')

class GalleryForm(forms.ModelForm):
    path = forms.FileField(label="Upload photo to gallery(supported formats:*jpg,*jpeg,*png)", required=False,widget=forms.ClearableFileInput(attrs={'id':"gallery_pic"}))
    description = forms.CharField(label="Description",widget=forms.Textarea(attrs={'rows':4,'cols':4}))

    class Meta:
        model = Gallery
        fields = ('path','description')

class AddJobForm(forms.ModelForm):
    date = forms.DateField(required=False)
    job_title = forms.CharField(label="Job title",max_length=255)
    job_description = forms.CharField(label="Job description",widget=forms.Textarea(attrs={'rows': 4,'cols': 40}))
    job_pdf = forms.FileField(label="upload pdf", required=False,widget=forms.ClearableFileInput(attrs={'id':"job_pdf"}))
    job_qualification = forms.CharField(label="Qualifications(separate each qualification with comma)",widget=forms.Textarea(attrs={'cols':40,'rows':4}))

    class Meta:
        model = Careers
        fields = ('job_title','job_description','job_pdf')
        
class AddEvents(forms.ModelForm):
    event_title = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':'Event Title'}))
    organizers = forms.CharField(label='',widget=forms.Textarea(attrs={'cols':40,'rows':2,'placeholder':'Organizors'}))
    event_content = forms.CharField(label='',widget=forms.Textarea(attrs={'cols':40,'rows':2,'placeholder':'Event Content'}))
    start_date  = forms.DateField(widget = forms.DateInput(attrs={'placeholder':'Starting Date','type':'date'}))
    end_date = forms.DateField(widget = forms.DateInput(attrs={'placeholder':'Ending Date','type':'date'}))
    start_time = forms.TimeField(label='',widget=forms.TimeInput(format='%H:%M',attrs={'placeholder':'Starting Time in HH:MM fomat'}))
    end_time = forms.TimeField(label='',widget=forms.TimeInput(format='%H:%M',attrs={'placeholder':'Ending Time in HH:MM format'}))
    more_info = forms.FileField(label='', required=False,widget=forms.ClearableFileInput(attrs={'id':"event_pdf",'placeholder':'Upload PDF file'}))

    class Meta:
        model = Events
        fields = 'event_title','organizers','event_content','start_date','end_date','start_time','end_time','more_info'


class StartupContract(forms.ModelForm):
    contract_date = forms.DateField(label="Contract Date",widget = forms.DateInput(attrs={'type':'date'}))
    contract_expiry = forms.DateField(label="Contract Expiry Date",widget = forms.DateInput(attrs={'type':'date'}))
    contract_pdf = forms.FileField(label='Upload Contract as PDF file', widget = forms.ClearableFileInput(attrs={'name':'contractPdf'}))

    class Meta:
        model = StartupCompanyInfo
        fields = 'contract_date','contract_expiry','contract_pdf'


class JobApplicationForm(forms.Form):
    first_name = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':'First Name'}))
    last_name =  forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':'Last Name'}))
    email = forms.CharField(label="",widget=forms.EmailInput(attrs={'placeholder':'Email','type':'email'}))
    phone = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':'Phone'}))
    experience = forms.ChoiceField(label="Experience",required=False,choices=YESNO,widget=forms.Select(attrs={'id':'experience'}))
    years = forms.CharField(label="Experience in years",required=False)
    resume = forms.FileField(label="Upload Resume",required=False ,widget=forms.ClearableFileInput(attrs={'id':'applicants_resume','name':'resume'}))
    country_code = forms.ChoiceField(label="",choices=CODE,widget=forms.Select(attrs={'name':'country-code'}))
    
    class Meta:
        model = JobApplication
        fields = 'first_name','last_name','email','phone','experience','resume','country_code'
