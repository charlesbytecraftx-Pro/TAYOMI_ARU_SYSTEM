from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Sum, Q
from django.utils import timezone
from django.http import HttpResponse
from openpyxl import Workbook

from .forms import UserSignUpForm, ProfileUpdateForm
from .models import CustomUser
from payments.models import Payment
from events.models import Event
from groups.models import Group

def register(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Akaunti imetengenezwa! Tafadhali kamilisha profile yako hapa.")
            return redirect('complete_profile') 
    else:
        form = UserSignUpForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def complete_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile imekamilika! Karibu kwenye Menu Kuu.")
            return redirect('user_dashboard')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'accounts/complete_profile.html', {'form': form})

@login_required
def user_dashboard(request):
    pending_payments = Payment.objects.filter(
        member=request.user, 
        status__in=['Not Paid', 'Pending']
    ).order_by('-date_paid')
    
    today = timezone.now().date()
    
    if request.user.is_staff:
        upcoming_events = Event.objects.filter(date__gte=today).order_by('date', 'time')[:3]
    else:
        upcoming_events = Event.objects.filter(
            Q(group=request.user.group) | Q(group__isnull=True),
            date__gte=today
        ).order_by('date', 'time')[:3]

    my_groups = Group.objects.filter(members=request.user)

    admin_data = None
    if request.user.is_staff:
        admin_data = {
            'total_members': CustomUser.objects.count(),
            'total_collections': Payment.objects.filter(status='Confirmed').aggregate(Sum('amount'))['amount__sum'] or 0,
            'pending_verifications': Payment.objects.filter(status='Pending').count(),
            'recent_members': CustomUser.objects.order_by('-date_joined')[:5],
            'total_groups': Group.objects.count(),
        }

    context = {
        'pending_payments': pending_payments,
        'upcoming_events': upcoming_events,
        'my_groups': my_groups,
        'admin_data': admin_data,
    }
    return render(request, 'accounts/dashboard.html', context)

@user_passes_test(lambda u: u.is_staff, login_url='user_dashboard')
def members_list(request):
    query = request.GET.get('search')
    all_members = CustomUser.objects.all().order_by('-date_joined')

    if query:
        all_members = all_members.filter(
            Q(username__icontains=query) |
            Q(full_name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query) |  # Logic mpya ya kutafuta kwa namba
            Q(group__name__icontains=query)
        ).distinct()

    # LOGIC YA EXPORT EXCEL
    if 'export' in request.GET:
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="Wanachama_TAYOMI_ARU.xlsx"'
        wb = Workbook()
        ws = wb.active
        ws.title = "Wanachama"
        ws.append(['Jina Kamili', 'Namba ya Simu', 'Email', 'Kikundi', 'Reg No', 'Mkoa'])
        for member in all_members:
            ws.append([member.full_name or member.username, member.phone or '-', member.email, str(member.group or 'General'), member.registration_number or '-', member.mkoa_wa_makazi or '-'])
        wb.save(response)
        return response

    context = {
        'members': all_members,
        'search_query': query
    }
    return render(request, 'accounts/members_list.html', context)

@login_required
def msaada_view(request):
    return render(request, 'accounts/msaada.html')