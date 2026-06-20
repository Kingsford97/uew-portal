from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import MemberProfile, PaymentAccount, DuesSettings


class MemberSignUpForm(UserCreationForm):
    name = forms.CharField(max_length=200, required=True)
    course = forms.CharField(max_length=100, required=True)
    department = forms.CharField(max_length=100, required=True)
    index_number = forms.CharField(max_length=20, required=True)
    department_association = forms.CharField(max_length=200, required=True)
    position = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

            # Create member profile
            member = MemberProfile.objects.create(
                user=user,
                name=self.cleaned_data['name'],
                course=self.cleaned_data['course'],
                department=self.cleaned_data['department'],
                index_number=self.cleaned_data['index_number'],
                department_association=self.cleaned_data['department_association'],
                position=self.cleaned_data['position']
            )
        return user


class MemberLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class MemberProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = MemberProfile
        fields = ['profile_picture']


class PaymentForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, required=True)
    payment_method = forms.ChoiceField(choices=[('Mobile Money', 'Mobile Money')])
    phone_number = forms.CharField(max_length=15, required=True)
    account_number = forms.CharField(max_length=20, required=True)
    account_name = forms.CharField(max_length=200, required=True)


class AdminAddMemberForm(forms.ModelForm):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()

    class Meta:
        model = MemberProfile
        fields = ['name', 'course', 'department', 'index_number',
                  'department_association', 'position']

    def save(self, commit=True):
        # Create user account
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email']
        )

        member = super().save(commit=False)
        member.user = user
        if commit:
            member.save()
        return member


class AdminDuesSettingsForm(forms.ModelForm):
    class Meta:
        model = DuesSettings
        fields = ['default_amount', 'due_date']


class AdminPaymentAccountForm(forms.ModelForm):
    class Meta:
        model = PaymentAccount
        fields = ['provider', 'account_number', 'account_name']