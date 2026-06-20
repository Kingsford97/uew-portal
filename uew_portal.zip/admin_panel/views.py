from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils import timezone
from students.models import Student, Teacher
from .models import DuesSettings, PaymentAccount, MemberVerification, PortalSettings, SystemLog


@staff_member_required
def admin_dashboard(request):
    total_students = Student.objects.count()
    verified_students = Student.objects.filter(is_verified=True).count()
    pending_verification = Student.objects.filter(is_verified=False).count()
    total_teachers = Teacher.objects.count()

    context = {
        'total_students': total_students,
        'verified_students': verified_students,
        'pending_verification': pending_verification,
        'total_teachers': total_teachers,
        'recent_verifications': MemberVerification.objects.all().order_by('-created_date')[:10],
        'recent_logs': SystemLog.objects.all().order_by('-created_date')[:10],
    }
    return render(request, 'admin_panel/dashboard.html', context)


@staff_member_required
def verify_member(request, member_id):
    student = get_object_or_404(Student, id=member_id)

    if request.method == 'POST':
        student.is_verified = True
        student.save()

        MemberVerification.objects.create(
            member=student,
            admin_user=request.user,
            status='approved',
            verified_date=timezone.now()
        )

        messages.success(request, f'{student.full_name()} has been verified successfully!')
        return redirect('admin_panel:admin_dashboard')

    return render(request, 'admin_panel/verify_member.html', {'member': student})


@staff_member_required
def manage_dues(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        due_date = request.POST.get('due_date')
        academic_year = request.POST.get('academic_year')

        if amount and due_date:
            DuesSettings.objects.create(
                admin_user=request.user,
                default_amount=amount,
                due_date=due_date,
                academic_year=academic_year,
                is_active=True
            )
            messages.success(request, 'Dues settings updated successfully!')
            return redirect('admin_panel:manage_dues')

    current_settings = DuesSettings.objects.filter(is_active=True).first()
    all_settings = DuesSettings.objects.all().order_by('-created_date')[:10]

    context = {
        'current_settings': current_settings,
        'all_settings': all_settings,
    }
    return render(request, 'admin_panel/manage_dues.html', context)


@staff_member_required
def manage_payment_accounts(request):
    if request.method == 'POST':
        provider = request.POST.get('provider')
        account_number = request.POST.get('account_number')
        account_name = request.POST.get('account_name')
        account_holder = request.POST.get('account_holder')

        if provider and account_number and account_name:
            PaymentAccount.objects.create(
                admin_user=request.user,
                provider=provider,
                account_number=account_number,
                account_name=account_name,
                account_holder=account_holder or account_name,
                is_active=True
            )
            messages.success(request, 'Payment account added successfully!')
            return redirect('admin_panel:manage_payment_accounts')

    accounts = PaymentAccount.objects.all()
    return render(request, 'admin_panel/manage_payment_accounts.html', {'accounts': accounts})


@staff_member_required
def upload_portal_picture(request):
    if request.method == 'POST' and request.FILES.get('portal_picture'):
        portal_picture = request.FILES['portal_picture']

        settings, created = PortalSettings.objects.get_or_create(id=1)
        settings.portal_profile_picture = portal_picture
        settings.save()

        messages.success(request, 'Portal profile picture uploaded successfully!')
        return redirect('admin_panel:admin_dashboard')

    return render(request, 'admin_panel/upload_portal_picture.html')


@staff_member_required
def member_list(request):
    members = Student.objects.all()
    return render(request, 'admin_panel/member_list.html', {'members': members})


@staff_member_required
def add_member(request):
    if request.method == 'POST':
        # Handle adding member
        pass
    return render(request, 'admin_panel/add_member.html')