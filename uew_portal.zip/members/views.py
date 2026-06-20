from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import MemberProfile, PaymentAccount, DuesSettings
from .forms import MemberSignUpForm, MemberProfileUpdateForm, PaymentForm


def signup(request):
    if request.method == 'POST':
        form = MemberSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('member_dashboard')
    else:
        form = MemberSignUpForm()
    return render(request, 'members/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Welcome back!')
            return redirect('member_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'members/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')


@login_required
def member_dashboard(request):
    try:
        member = MemberProfile.objects.get(user=request.user)
        return render(request, 'members/dashboard.html', {'member': member})
    except MemberProfile.DoesNotExist:
        messages.error(request, 'Profile not found.')
        return redirect('profile_setup')


@login_required
def upload_profile_picture(request):
    try:
        member = MemberProfile.objects.get(user=request.user)
        if request.method == 'POST':
            form = MemberProfileUpdateForm(request.POST, request.FILES, instance=member)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile picture updated!')
                return redirect('member_dashboard')
        else:
            form = MemberProfileUpdateForm(instance=member)

        return render(request, 'members/upload_picture.html', {'form': form, 'member': member})
    except MemberProfile.DoesNotExist:
        messages.error(request, 'Profile not found.')
        return redirect('profile_setup')


@login_required
def update_member_details(request):
    try:
        member = MemberProfile.objects.get(user=request.user)
        if request.method == 'POST':
            member.name = request.POST.get('name')
            member.course = request.POST.get('course')
            member.department = request.POST.get('department')
            member.index_number = request.POST.get('index_number')
            member.department_association = request.POST.get('department_association')
            member.position = request.POST.get('position')
            member.save()

            messages.success(request, 'Details updated!')
            return redirect('member_dashboard')

        return render(request, 'members/update_details.html', {'member': member})
    except MemberProfile.DoesNotExist:
        messages.error(request, 'Profile not found.')
        return redirect('profile_setup')


@login_required
def pay_dues(request):
    try:
        member = MemberProfile.objects.get(user=request.user)
        payment_accounts = PaymentAccount.objects.filter(is_active=True)
        dues_settings = DuesSettings.objects.filter(is_active=True).first()

        if request.method == 'POST':
            form = PaymentForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']

                member.has_paid_dues = True
                member.dues_amount = amount
                member.payment_date = timezone.now()
                member.payment_method = 'Mobile Money'
                member.payment_reference = f"PAY-{timezone.now().strftime('%Y%m%d%H%M%S')}"
                member.save()

                messages.success(request, f'Payment of GHS {amount} successful!')
                return redirect('member_dashboard')
        else:
            form = PaymentForm()

        context = {
            'member': member,
            'payment_accounts': payment_accounts,
            'dues_settings': dues_settings,
            'form': form
        }
        return render(request, 'members/pay_dues.html', context)
    except MemberProfile.DoesNotExist:
        messages.error(request, 'Profile not found.')
        return redirect('profile_setup')


@login_required
def profile_setup(request):
    try:
        member = MemberProfile.objects.get(user=request.user)
        if request.method == 'POST':
            form = MemberProfileUpdateForm(request.POST, request.FILES, instance=member)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile setup complete!')
                return redirect('member_dashboard')
        else:
            form = MemberProfileUpdateForm(instance=member)

        return render(request, 'members/profile_setup.html', {'form': form, 'member': member})
    except MemberProfile.DoesNotExist:
        messages.error(request, 'Please contact admin.')
        return redirect('home')