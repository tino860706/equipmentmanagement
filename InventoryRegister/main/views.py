from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from .models import EquipmentIssue
from . import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from django.http import FileResponse
import io

from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.db.models import Q

from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views.generic import ListView
import datetime
import csv

from tempfile import TemporaryFile, NamedTemporaryFile
from django.template.loader import render_to_string
from django.db.models import Sum
import xlwt
import os

from haystack.query import SearchQuerySet

os.add_dll_directory(r"C:\Program Files\GTK3-Runtime Win64")
from weasyprint import HTML
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group


# Create your views here.
@unauthenticated_user
def register_page(request):
    form = forms.CreateUserForm()
    if request.method == 'POST':
        form = forms.CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            group = Group.objects.get(name='ordinary')
            user.groups.add(group)
            messages.success(request, 'Account was created for ' + username)
            return redirect('main:login')
    else:
        form = forms.CreateUserForm()
    context = {'form': form}
    return render(request, 'register.html', context)


@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main:home')
        else:
            messages.info(request, 'Username OR password is incorrect')
    context = {}
    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('main:login')


@login_required(login_url='main:login')
@allowed_users(allowed_roles=['admin'])
def index(request):
    q = request.GET.get('q', None)
    items = ''
    equipment = EquipmentIssue.objects.all()
    if q == None == q == '':
        equipment = EquipmentIssue.objects.all()
    elif q != None:
        equipment = EquipmentIssue.objects.filter(Q(name__icontains=q)|
                                                  Q(department__icontains=q)|
                                                  Q(equipment_category__icontains=q)|
                                                  Q(slug__icontains=q))

    context = {'equipment': equipment}
    return render(request, 'index.html', context)


@login_required(login_url='main:login')
@allowed_users(allowed_roles=['ordinary'])
def userPage(request):
    gadgets = request.user.ordinary.equipment_set.all()
    print('GADGETS', gadgets)
    context = {'gadgets': gadgets}
    return render(request, 'user.html', context)


@login_required(login_url='main:login')
@allowed_users(allowed_roles=['admin'])
def issues(request):
    form = forms.IssueForm()
    if request.method == 'POST':
        form = forms.IssueForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('main:home'))
    else:
        form = forms.IssueForm()
    context = {'form': form}
    return render(request, 'issues.html', context)


@login_required(login_url='main:login')
@allowed_users(allowed_roles=['admin'])
def editIssues(request, issue_id):
    issue = EquipmentIssue.objects.get(id=issue_id)
    if request.method != 'POST':
        form = forms.IssueForm(instance=issue)
    else:
        form = forms.IssueForm(instance=issue, data=request.POST)
        if form.is_valid():
            updated = form.save(commit=False)
            updated.save()
            return HttpResponseRedirect(reverse('main:home'))
    context = {'issue': issue, 'form': form}
    return render(request, 'edit_issues.html', context)


@login_required(login_url='main:login')
@allowed_users(allowed_roles=['admin'])
def deleteIssue(request, issue_id):
    try:
        issue = EquipmentIssue.objects.get(id=issue_id)
        issue.delete()
        return HttpResponse('Record successfully deleted')
    except:
        return HttpResponse('Record doesn\'t exist')


@login_required(login_url='main:login')
@allowed_users(allowed_roles=['admin'])
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Equipment.csv"'
    writer = csv.writer(response)
    writer.writerow(['name', 'description', 'serial number', 'date of issue'])
    equipment = EquipmentIssue.objects.all()

    for equip in equipment:
        writer.writerow([equip.name, equip.description,
                         equip.serial_number, str(equip.date_of_issue)])
    return response


@login_required(login_url='main:login')
@allowed_users(allowed_roles=['admin'])
def export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename=Equipment.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    equipment = EquipmentIssue.objects.filter(active=True)
    html_to_string = render_to_string('pdf_output.html', {'equipment': equipment})
    html = HTML(string=html_to_string)
    result = html.write_pdf()
    with open('tempo.bin', 'w+b') as output:
        output.write(result)
        output.flush()
        output = open(output.name, mode='rb', buffering=-1, closefd=True)
        response.write(output.read())
    return response


@login_required(login_url='main:login')
@allowed_users(allowed_roles=['admin'])
def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=equipment.xls'
    work_book = xlwt.Workbook(encoding='utf-8')
    work_sheet = work_book.add_sheet('equipment')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['DATE ISSUED', 'RECIPIENT NAME', 'RECIPIENT  DEPARTMENT',
               'EQPT CATEGORY', 'EQPT DESCRIPTION', 'EQPT SERIAL NUMBER',
               'EQPT STATUS', ]
    for col_num in range(len(columns)):
        work_sheet.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = EquipmentIssue.objects.filter(active=True).values_list(
        'date_of_issue',
        'name', 'department', 'equipment_category', 'description', 'serial_number', 'status')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            work_sheet.write(row_num, col_num, str(row[col_num]), font_style)
    work_book.save(response)
    return response
