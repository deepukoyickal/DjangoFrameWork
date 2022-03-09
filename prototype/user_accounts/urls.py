from os import name
from django.urls import path
from . import views


urlpatterns = [
  
   path("register/", views.userRegistration, name="userRegistration"),
   path("login/", views.login, name="login"),
   path("logout/",views.logout, name="logout"),
   path("startupprofile/", views.Startupprofile, name="Startupprofile"),
   path("mentorprofile/",views.Mentorprofile,name="Mentorprofile"),
   path("save/",views.SavePersonalInfo, name="save"),
   path("savecompany/", views.SaveCompanyInfo, name="savecompany"),
   path("saveotherinfo/", views.SaveOtherInfo, name="SaveOtherInfo"),
   path("getotp/", views.getOTP, name="getOTP"),
   path("resendotp/", views.resendOTP, name="resendOTP"),
   path("verifyotp/", views.verfiyOTP, name="verfiyOTP"),
   path("savecareer/", views.SaveCareerInfo, name="savecareer"),
   path("saveacademic/", views.SaveAcademicInfo, name="saveacademic"),
   path("forum/", views.viewForum, name="forum"),
   path("savepost/",views.savePost,name="savepost"),
   path("add_like/",views.addLikes,name="add_like"),
   path("postcomment/",views.postComments,name="postcomment"),
   path('comments/<int:post_id>/',views.viewComments,name="comments"),
   path('likeComment/',views.likeComment,name="likeComment"),
   path('startup_pitch/<int:user_id>/',views.viewPdf,name='viewpdf'),
   path('about/',views.about,name='about'),
   path('deleteUser/',views.deleteUser,name="deleteUser"),
   path('approveUser/',views.approveUser,name="approveUser"),
   path('apply_incubation/',views.applyIncubation,name="applyIncubation"),
   path('cancel_incubation/',views.cancelIncubation,name="cancelIncubation"),
   path('startup_home/',views.Startup_home,name="startup_home"),
   
   
]