from curses.ascii import NUL
from django import forms
from django.forms.widgets import EmailInput, Select, TextInput, Textarea
from . models import StartupCompanyInfo, User_Comments, User_Posts, UserPersonalInfo, MentorInfo

NATUREOFFIRM=[('Not yet registered','Not yet registered'),
         ('Proprietary','Proprietary'),
         ('Private Limited', 'Private Limited'),
         ('Other', 'Other')]
USERTYPE=[('Mentor', 'Mentor'),
            ('Startup', 'Startup')]

COMPANYSTAGE=[('seed', 'seed'),
            ('early', 'early'),
            ('late', 'late')]
MSMEREGISTRATION=[('udyam','udyam'),
                ('udyog','udyog'),
                ('nill','nill')]
FLAGSHIPPROGRAM=[('women empowerment','women empowerment'),
                ('make in India', 'make in India'),
                ('swatch bharat', 'swatch bharat'),
                ('startup India','startup India'),
                ('beti bachao beti padhao', 'beti bachao beti padhao')]
GENDER=[('Male','Male'),
        ('Female','Female'),
        ('Other','Other')]

AREASOFEXPERTISE=[('Product development','Product development'),
                ('Marketing strategy','Marketing strategy'),
                ('Business Development','Business Development'),
                ('social media marketing','social media marketing')]
YESNO=[('False','No'),('True','Yes')]

PROPERTY =[('applied','applied'),('waiting','waiting'),('approved','approved')]

FUNDING =[('none','none'),('seedfund','seedfund'),('investors','investors')]

INCUBATION = [('physical','physical'),('virtual','virtual')]


class Registration(forms.Form):
    first_name= forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'class':'border border-info','placeholder':'First Name'}))
    last_name = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'class':'border border-info','placeholder':'Last Name'}))
    password = forms.CharField(label='',widget=forms.PasswordInput(attrs={'id':'password','class':'border border-info','placeholder':'Password'}))
    confirm_password =  forms.CharField(label='',widget=forms.PasswordInput(attrs={'id':'confirm_password','class':'border border-info','placeholder':'Confirm Password'}))   
    email = forms.EmailField(label='',widget=EmailInput(attrs={'id':'email','readonly':'true','class':'border border-info','placeholder':'Email Id'}))
    userType = forms.ChoiceField(label='',choices=USERTYPE, widget=forms.Select(attrs={'class':'border border-info','placeholder':'User Type'}))
    terms = forms.BooleanField(label="I accept terms and conditions", widget=forms.CheckboxInput(attrs={'class':'form-check-input','id':'terms','required':'true'}))
   
class saveOTP(forms.Form):
    email = forms.EmailField(label='',widget=EmailInput(attrs={'id':'email_otp','placeholder':'Enter your email','class':'border border-info'}))
    conf_email = forms.EmailField(label='',widget=EmailInput(attrs={'id':'conf_email','readonly':'true','class':'border border-info'}))
    resend_email = forms.EmailField(label='',widget=EmailInput(attrs={'id':'resend_email','readonly':'true','style':'visibility:hidden'}))
    otp = forms.CharField(label='',max_length=6, widget=TextInput(attrs={'placeholder':'Enter OTP number','autocomplete':'off','class':'border border-info'}))
   
class BasicInfo(forms.ModelForm):
    first_name= forms.CharField(label='First Name*', max_length=100)
    last_name = forms.CharField(label='Last Name*', max_length=100)
    class Meta:
        model = UserPersonalInfo
        fields = ('first_name','last_name')

class PersonalInfo(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #    super(PersonalInfo, self).__init__(*args, **kwargs)
    #    for key in self.fields.keys():
    #        if self.fields[key] != '':
    #         self.fields[key].widget.attrs['readonly'] = True
    place = forms.CharField(label="Place",required=False)
    gender = forms.ChoiceField(choices=GENDER, widget=forms.RadioSelect,required=False)   
    contact_number = forms.CharField(max_length=20,required=False)
    address = forms.CharField( widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}),required=False)
    whatsappnumber=forms.CharField(label="Whatsapp", max_length=20,required=False)
    profilepic = forms.ImageField(label="Profile Picture", required=False, widget=forms.ClearableFileInput(attrs={'id':"profile_pic"}))    
    class Meta:
        model = UserPersonalInfo
        fields = ('place','contact_number','address','whatsappnumber','profilepic',)


class LoginForm(forms.Form):
    email = forms.EmailField(label='',widget=forms.EmailInput(attrs={'class':'border border-info','placeholder':'Email'}))
    password = forms.CharField(label='',widget= forms.PasswordInput(attrs={'autocomplete': 'off','data-toggle': 'true','class':'border border-info','placeholder':'Password'}))




class OtherCompanyInfo(forms.ModelForm):
    academic_qualification_founder = forms.CharField(label='Highest Qualification*', max_length=100, required=False)
    field_of_study =  forms.CharField(label='Specialization*', max_length=50, required=False)
    experience_of_founder = forms.CharField(label='Experience*', max_length=100, required=False)
    core_competancy = forms.CharField(label='core competancy', max_length=100,required=False)   
    expectation = forms.CharField(label="what do you expect from AIC-IIITKottayam?", widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}),required=False)
    other_info = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}),required=False)
    class Meta:
        model = StartupCompanyInfo
        fields = ('academic_qualification_founder','field_of_study','experience_of_founder','core_competancy','expectation','other_info')

class CompanyInfo(forms.ModelForm):
    companyname = forms.CharField(label='Company Name*', required=False)
    cin_number = forms.CharField(label='CIN Number', max_length=100, required=False)
    dipp_number = forms.CharField(label='DIPP Number', max_length=100, required=False)
    founder = forms.CharField(label='Founder*', max_length=100, required=False)
    num_directors = forms.CharField(label='Number of Directors*', max_length=100, required=False)
    num_women_dir = forms.CharField(label='Number of Women Directors*', max_length=100, required=False)
    stage = forms.ChoiceField(choices=COMPANYSTAGE, label="Company Stage*", widget=forms.RadioSelect, required=False)
    employees = forms.CharField(label='NUmber of Employees*', max_length=100, required=False)
    webpage = forms.CharField(label='Webpage', max_length=100, required=False)
    msme_registration = forms.ChoiceField(choices=MSMEREGISTRATION, label="MSME Registration", widget=forms.RadioSelect,required=False)
    flagship_program = forms.ChoiceField(choices = FLAGSHIPPROGRAM, label="Flagship Program", widget=forms.RadioSelect(),required=False)
    about = forms.CharField( label="About Company and Product*", widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}), required=False)
    nature_of_firm = forms.ChoiceField(choices=NATUREOFFIRM, widget=forms.RadioSelect(),label="Nature of firm*", required=False)
    company_address = forms.CharField( label="Company Address*", widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}), required=False)
    startup_pitch = forms.FileField(label="Upload Pitch(supported formats:*pdf,*pptx)", required=False, widget=forms.ClearableFileInput(attrs={'id':"startup_pitch"}))
    intelectual_property = forms.ChoiceField(label='Intelectual Property',choices=YESNO,widget=Select(attrs={'id':'intelectual_property'}),required=False)
    i_property_type = forms.ChoiceField(label='Intelectual Property Type',choices=PROPERTY,widget=Select(attrs={'id':'i_propery_type'}),required=False)
    year_of_registration = forms.DateField(widget = forms.DateInput(attrs={'type':'date'}),required=False)
    funding = forms.ChoiceField(choices=FUNDING,required=False)
    company_logo = forms.FileField(label="Upload Company Logo(supported formats:*jpg,*png,jpeg)", widget=forms.ClearableFileInput(attrs={'id':"company_logo"}), required=False)
    number_of_ip = forms.CharField(label="Number of IP",widget=forms.TextInput(attrs={'id':'i_property_num'}),required=False)
    type_of_incubation = forms.ChoiceField(choices=INCUBATION,label="Type of incubation*", required=False)
    sector = forms.CharField(label="Sector of company",required=False)
    operational_model = forms.CharField(label="Operational model",required=False,widget=forms.Textarea(attrs={'cols':40,'rows':2}))
    target_market = forms.CharField(label="Target market",required=False,widget=forms.Textarea(attrs={'cols':40,'rows':2}))

    class Meta:
        model = StartupCompanyInfo 
        fields = ('companyname','cin_number','dipp_number','founder','num_directors','num_women_dir','stage',
        'employees','webpage','msme_registration','flagship_program','about','nature_of_firm','company_address',
        'startup_pitch','intelectual_property','i_property_type','year_of_registration','funding','company_logo',
        'number_of_ip','operational_model','target_market','sector','type_of_incubation')

class MentorInfoCareer(forms.ModelForm):
    Designation = forms.CharField(max_length=100)
    Current_working_company = forms.CharField(max_length=100)
    Previous_working_experience = forms.CharField(widget=Textarea(attrs={'rows':'3','cols':40}))
    supported_any_startup  = forms.ChoiceField(choices=YESNO,widget=Select())
    Working_Domain =  forms.CharField(max_length=100)
    areas_of_expertise = forms.MultipleChoiceField(choices=AREASOFEXPERTISE,widget=forms.CheckboxSelectMultiple())
    Presently_residing = forms.CharField(widget=Textarea(attrs={'rows':'3','cols':40}))
    experience_as_mentor = forms.CharField(max_length=100)
    contribution_to_startup_echosystem = forms.CharField(widget=Textarea(attrs={'rows':'3','cols':40}))
    
    
    
    class Meta:
        model = MentorInfo
        fields = ('Designation','Current_working_company','Previous_working_experience','supported_any_startup','Working_Domain','areas_of_expertise','Presently_residing','experience_as_mentor','contribution_to_startup_echosystem')


class MentorInfoAcademic(forms.ModelForm):
    Bachelors_Degree = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'form-check-input','id':'bachelors_degree'}),required=False)
    Masters_Degree = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'form-check-input','id':'masters_degree'}),required=False)
    PHD = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'form-check-input','id':'phd'}),required=False)
    B_Institute = forms.CharField(label="Institute", max_length=100,widget=forms.TextInput(attrs={'id':'B_Institute','readonly':'true'}),required=False)
    M_Institute = forms.CharField(label="Institute",max_length=100,widget=forms.TextInput(attrs={'id':'M_Institute','readonly':'true'}),required=False)
    P_Institute = forms.CharField(label="Institute",max_length=100,widget=forms.TextInput(attrs={'id':'P_Institute','readonly':'true'}),required=False)
    B_Subject = forms.CharField(label="Course",max_length=100,widget=forms.TextInput(attrs={'id':'B_Subject','readonly':'true'}),required=False)
    M_Subject = forms.CharField(label="Course",max_length=100,widget=forms.TextInput(attrs={'id':'M_Subject','readonly':'true'}),required=False)
    P_Subject = forms.CharField(label="Domain",max_length=100,widget=forms.TextInput(attrs={'id':'P_Subject','readonly':'true'}),required=False)
    post_doctorate = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'form-check-input','id':'post_doctorate'}),required=False)
    post_doctorate_domain = forms.CharField(label="Domain",max_length=100,widget=forms.TextInput(attrs={'id':'post_doctorate_sub','readonly':'true'}),required=False)

    class Meta:
        model = MentorInfo
        fields = ('Bachelors_Degree','Masters_Degree','PHD','B_Institute','M_Institute','P_Institute','B_Subject','M_Subject','P_Subject','post_doctorate','post_doctorate_domain')

class User_social_posts(forms.ModelForm):
    post_id = forms.CharField(max_length=255,widget=forms.TextInput(attrs={}),required=False)
    username = forms.CharField(max_length=100,required=False)
    post_time = forms.DateTimeField(required=False)
    post_title = forms.CharField(max_length=100)
    post_content = forms.CharField(label="",widget=forms.Textarea(attrs={'rows':10,'placeholder':'enter your content here.'}),required=True)
    post_photo = forms.ImageField(required=False, widget=forms.ClearableFileInput(),label="select from gallery")  
    like_count = forms.CharField(max_length=100,required=False)
    comment_count = forms.CharField(max_length=100,required=False)

    class Meta:
        model = User_Posts
        fields = ('post_title','post_content','post_photo','like_count','comment_count')

class addLikesToPosts(forms.ModelForm):
    like_count = forms.CharField(max_length=100,required=True)

    class Meta:
        model = User_Posts
        fields = ('like_count',)

class addCommentsToPosts(forms.ModelForm):
    class Meta:
        model = User_Comments
        fields = ('comment_content',)


    



