from django.urls import path
from .import views



urlpatterns = [
    path('',views.main_index,name='main-index'),
    path('index/',views.index,name='index'),
    path('index-doc/',views.index_doc,name='index-doc'),
    path('index-pat/',views.index_pat,name='index-pat'),
    path('login',views.login,name='login'),
    path('logout/',views.logout,name='logout'),

    #----------------------------Doctor-----------------------------------#
    path('create-doctor/',views.create_doctor,name='create-doctor'),
    path('view-doctor/',views.view_doctor,name='view-doctor'),
    path('update-doctor/<int:pk>',views.update_doctor,name='update-doctor'),
    path('delete-doctor/<int:pk>',views.delete_doctor,name='delete-doctor'),
    path('profile-doc/',views.profile_doc,name='profile-doc'),


    #----------------------------patient---------------------------------#
    path('create-patient/',views.create_patient,name='create-patient'),
    path('view-patient/',views.view_patient,name='view-patient'),
    path('update-patient/<int:pk>',views.update_patient,name='update-patient'),
    path('delete-patient/<int:pk>',views.delete_patient,name='delete-patient'),
    path('profile-pat/',views.profile_pat,name='profile-pat'),


    #-----------------------------slot-----------------------------------#
    path('slot/',views.slot,name='slot'),


    #----------------------------Appoinment------------------------------#
    path('book-app',views.book_app,name='book-app'),
    path('book-app-view/',views.book_app_view,name='book-app-view'),
    path('view-appoinment/',views.view_appoinment,name='view-appoinment'),



    # #Admin view appoinment #
    path('view-appoinment-admin/',views.view_appoinment_admin,name='view-appoinment-admin'),



    # #------------------------------Status-action--------------------------#
    path('status-complete/<int:pk>',views.status_complete,name='status-complete'),
    path('status-absent/<int:pk>',views.status_absent,name='status-absent'),
    path('status-cancelled/<int:pk>',views.status_cancelled,name='status-cancelled'),
    path('pat-status-cancelled/<int:pk>',views.pat_status_cancelled,name='pat-status-cancelled'),

]