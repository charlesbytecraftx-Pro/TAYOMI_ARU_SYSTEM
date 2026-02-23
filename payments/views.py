import openpyxl
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Sum, Q
from django.utils import timezone
from .models import Payment, ContributionType, Profile
from .forms import PaymentSubmissionForm
from django.template.loader import get_template
from xhtml2pdf import pisa

@login_required
def user_dashboard(request):
    """Dashboard ya Mwanachama & Admin Overview"""
    all_payments = Payment.objects.filter(member=request.user).order_by('-id')
    
    total_to_pay = all_payments.aggregate(Sum('amount'))['amount__sum'] or 0
    total_paid = all_payments.filter(status='Confirmed').aggregate(Sum('amount'))['amount__sum'] or 0
    remaining_balance = total_to_pay - total_paid

    context = {
        'recent_payments': all_payments[:10],
        'total_to_pay': total_to_pay,
        'total_paid': total_paid,
        'remaining_balance': remaining_balance,
        'contribution_types': ContributionType.objects.all(),
        'admin_pending': Payment.objects.filter(status='Pending').count() if request.user.is_staff else 0,
    }
    return render(request, 'payments/payment_dashboard.html', context)

@login_required
def submit_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, member=request.user)
    if request.method == 'POST':
        form = PaymentSubmissionForm(request.POST, request.FILES, instance=payment)
        if form.is_valid():
            try:
                temp_payment = form.save(commit=False)
                temp_payment.status = 'Pending'
                temp_payment.save()
                messages.success(request, f"Muamala {temp_payment.reference_number} umepokelewa!")
                return redirect('user_dashboard')
            except IntegrityError:
                messages.error(request, "Namba hii ya muamala tayari imetumika.")
    else:
        form = PaymentSubmissionForm(instance=payment)
    return render(request, 'payments/submit_payment.html', {'form': form, 'payment': payment})

@login_required
def payment_list(request):
    payments = Payment.objects.filter(member=request.user).order_by('-id')
    return render(request, 'payments/payment_list.html', {'payments': payments})

# --- ADMIN CRUD FOR CONTRIBUTIONS ---

@user_passes_test(lambda u: u.is_staff)
def add_contribution_type(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        amount = request.POST.get('base_amount', 0)
        if name:
            ContributionType.objects.create(name=name, base_amount=amount)
            messages.success(request, f"Mchango wa '{name}' umeongezwa kwa wanachama wote!")
    return redirect('user_dashboard')

@user_passes_test(lambda u: u.is_staff)
def edit_contribution_type(request, pk):
    contribution = get_object_or_404(ContributionType, pk=pk)
    if request.method == 'POST':
        contribution.name = request.POST.get('name')
        contribution.save()
        messages.success(request, "Mchango umerekebishwa kikamilifu!")
    return redirect('user_dashboard')

@user_passes_test(lambda u: u.is_staff)
def delete_contribution_type(request, pk):
    contribution = get_object_or_404(ContributionType, pk=pk)
    contribution.delete()
    messages.warning(request, "Mchango umefutwa kwenye mfumo.")
    return redirect('user_dashboard')

# --- ADMIN PAYMENT MANAGEMENT ---

@user_passes_test(lambda u: u.is_staff)
def admin_payment_list(request):
    query = request.GET.get('q', '')
    payments = Payment.objects.all().order_by('-id')
    if query:
        payments = payments.filter(Q(member__username__icontains=query) | Q(reference_number__icontains=query))
    
    return render(request, 'payments/admin_payments.html', {'payments': payments, 'query': query})

@user_passes_test(lambda u: u.is_staff)
def confirm_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    action = request.GET.get('action')
    if action == 'confirm':
        payment.status = 'Confirmed'
        payment.verified_by = request.user
        messages.success(request, "Malipo yamethibitishwa!")
    elif action == 'reject':
        payment.status = 'Rejected'
        messages.warning(request, "Malipo yamekataliwa.")
    payment.save()
    return redirect('admin_payment_list')

@login_required
def download_receipt(request, payment_id):
    """Tengeneza PDF ya Risiti kwa malipo yaliyothibitishwa"""
    payment = get_object_or_404(Payment, id=payment_id, member=request.user, status='Confirmed')
    template_path = 'payments/receipt_pdf.html'
    context = {'payment': payment, 'request': request}
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Risiti_{payment.reference_number}.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse('Tatizo la kutengeneza PDF limetokea. Tafadhali jaribu tena.')
    return response
import openpyxl
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Sum, Q
from django.utils import timezone
from .models import Payment, ContributionType, Profile
from .forms import PaymentSubmissionForm
from django.template.loader import get_template
from xhtml2pdf import pisa

@login_required
def user_dashboard(request):
    """Dashboard ya Mwanachama & Admin Overview"""
    all_payments = Payment.objects.filter(member=request.user).order_by('-id')
    
    total_to_pay = all_payments.aggregate(Sum('amount'))['amount__sum'] or 0
    total_paid = all_payments.filter(status='Confirmed').aggregate(Sum('amount'))['amount__sum'] or 0
    remaining_balance = total_to_pay - total_paid

    context = {
        'recent_payments': all_payments[:10],
        'total_to_pay': total_to_pay,
        'total_paid': total_paid,
        'remaining_balance': remaining_balance,
        'contribution_types': ContributionType.objects.all(),
        'admin_pending': Payment.objects.filter(status='Pending').count() if request.user.is_staff else 0,
    }
    return render(request, 'payments/payment_dashboard.html', context)

@login_required
def submit_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, member=request.user)
    if request.method == 'POST':
        form = PaymentSubmissionForm(request.POST, request.FILES, instance=payment)
        if form.is_valid():
            try:
                temp_payment = form.save(commit=False)
                temp_payment.status = 'Pending'
                temp_payment.save()
                messages.success(request, f"Muamala {temp_payment.reference_number} umepokelewa!")
                return redirect('user_dashboard')
            except IntegrityError:
                messages.error(request, "Namba hii ya muamala tayari imetumika.")
    else:
        form = PaymentSubmissionForm(instance=payment)
    return render(request, 'payments/submit_payment.html', {'form': form, 'payment': payment})

@login_required
def payment_list(request):
    payments = Payment.objects.filter(member=request.user).order_by('-id')
    return render(request, 'payments/payment_list.html', {'payments': payments})

# --- ADMIN CRUD FOR CONTRIBUTIONS ---

@user_passes_test(lambda u: u.is_staff)
def add_contribution_type(request):
    """Kuongeza mchango mpya na kiasi chake pamoja na maelezo"""
    if request.method == 'POST':
        name = request.POST.get('name')
        amount = request.POST.get('base_amount', 0)
        description = request.POST.get('description', '')
        if name:
            ContributionType.objects.create(
                name=name, 
                base_amount=amount, 
                description=description
            )
            messages.success(request, f"Mchango wa '{name}' wenye kiasi cha TZS {amount} umeongezwa kwa wanachama wote!")
    return redirect('user_dashboard')

@user_passes_test(lambda u: u.is_staff)
def edit_contribution_type(request, pk):
    """Kuhariri mchango: Jina, Kiasi, na Maelezo"""
    contribution = get_object_or_404(ContributionType, pk=pk)
    if request.method == 'POST':
        contribution.name = request.POST.get('name')
        contribution.base_amount = request.POST.get('base_amount', 0)
        contribution.description = request.POST.get('description', '')
        contribution.save()
        messages.success(request, f"Mchango wa {contribution.name} umerekebishwa kikamilifu!")
    return redirect('user_dashboard')

@user_passes_test(lambda u: u.is_staff)
def delete_contribution_type(request, pk):
    contribution = get_object_or_404(ContributionType, pk=pk)
    contribution.delete()
    messages.warning(request, "Mchango umefutwa kwenye mfumo.")
    return redirect('user_dashboard')

# --- ADMIN PAYMENT MANAGEMENT ---

@user_passes_test(lambda u: u.is_staff)
def admin_payment_list(request):
    query = request.GET.get('q', '')
    payments = Payment.objects.all().order_by('-id')
    if query:
        payments = payments.filter(Q(member__username__icontains=query) | Q(reference_number__icontains=query))
    
    return render(request, 'payments/admin_payments.html', {'payments': payments, 'query': query})

@user_passes_test(lambda u: u.is_staff)
def confirm_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    action = request.GET.get('action')
    if action == 'confirm':
        payment.status = 'Confirmed'
        payment.verified_by = request.user
        messages.success(request, "Malipo yamethibitishwa!")
    elif action == 'reject':
        payment.status = 'Rejected'
        messages.warning(request, "Malipo yamekataliwa.")
    payment.save()
    return redirect('admin_payment_list')

@login_required
def download_receipt(request, payment_id):
    """Tengeneza PDF ya Risiti kwa malipo yaliyothibitishwa"""
    payment = get_object_or_404(Payment, id=payment_id, member=request.user, status='Confirmed')
    template_path = 'payments/receipt_pdf.html'
    context = {'payment': payment, 'request': request}
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Risiti_{payment.reference_number}.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse('Tatizo la kutengeneza PDF limetokea. Tafadhali jaribu tena.')
    return response
