from django.urls import path
from django.views.generic import TemplateView
from .views import index, issues, editIssues, deleteIssue, export_csv,\
    export_pdf, export_excel, register_page, login_page, logoutUser, userPage
from django.contrib.auth import views as auth_views
from main import forms
from django.contrib.auth import login

app_name = 'main'

urlpatterns = [
    path('', index, name='home'),
    path('issues/', issues, name='issues'),
    path('edit_issues/<int:issue_id>/', editIssues, name='edit_issues'),
    path('delete/<int:issue_id>/', deleteIssue, name='delete'),
    path('export_csv/', export_csv, name='export_csv'),
    path('export_pdf/', export_pdf, name='export_pdf'),
    path('export_excel/', export_excel, name='export_excel'),
    path('user/', userPage, name='user-page'),
    path('register/', register_page, name='register', ),
    path('login/', login_page, name='login'),
    path('logout/', logoutUser, name='logout'),
]
