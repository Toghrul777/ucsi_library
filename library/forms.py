from django import forms
from django.contrib.auth.forms import UserCreationForm

from library.models import Student, get_due


class EntryForm(forms.Form):
    borrower = forms.ModelChoiceField(Student.objects.all())
    isbn = forms.CharField(max_length=15)
    teacher = forms.CharField(max_length=30)
    contact = forms.CharField(max_length=50)
    due = forms.DateField(initial=get_due, disabled=True, widget=forms.DateInput(
        format='%B %d %Y'), input_formats=['%B %d %Y'])


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=40)
    student = forms.ModelChoiceField(Student.objects.all())
