from unicodedata import name
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path("index/", views.index, name='index'),
    path('staffView/',views.StaffView,name="StaffView"),
    path('addNews/',views.addNews,name="addNews"),
    path('appointment/',views.appointment,name="appointment"),
    path('aboutAIC/',views.aboutAIC,name="aboutAIC"),
    path('addTeamMember/',views.addTeamMember,name="addTeamMember"),
    path('member/<int:member_id>/',views.member,name="member"),
    path('updateMember<int:member_id>/',views.updateMember,name="updateMember"),
    path('gallery/',views.gallery,name="gallery"),
    path('addGallery/',views.addGallery,name="addGallery"),
    path('startups/',views.startups,name="startups"),
    path('boardmembers/',views.boardmembers),
    path('news/',views.news,name="news"),
    path('viewnews/<int:news_id>/',views.viewPdf,name='viewpdf'),
    path('careers/',views.careers,name="careers"),
    path('addjob/',views.addJob,name="addJob"),
    path('queries&reviews/',views.queriesAndReviews,name="queriesandreviews"),
    path('addEvents/',views.addEvents,name="addEvents"),
    path('profile/<int:user_id>/',views.ProfileView,name='profile'),
    path('remove_notification/',views.RemoveNotifications,name="remove_notification"),
    path('SendNotificationMail/<int:user_id>',views.SendNotificationMail,name="SendNotificationEmail"),
    path('viewJobPdf/<int:job_id>/',views.viewJobPdf,name="viewJobPdf"),
    path('apply_job/<int:job_id>/',views.Apply_job,name="Apply_job"),
    path('viewJob/<int:job_id>',views.ViewJob,name="viewJob"),
    path('deleteJob/<int:job_id>/',views.deleteJob,name="deleteJob"),
    path('ViewJobApplications/<int:job_id>/',views.ViewJobApplications,name="ViewJobApplications"),
    path('viewApplicantPdf/<int:id>/',views.viewApplicantPdf,name="viewApplicantPdf"),
    path('uploadStartupContract/<int:id>/',views.uploadStartupContract,name="uploadStartupContract"),
    path('incubateStartup/<int:id>/',views.incubateStartup,name="incubateStartup"),
]