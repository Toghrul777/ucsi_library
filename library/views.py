from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import date, timedelta

from library.models import Borrow
from library.forms import EntryForm, SignUpForm


@login_required
def borrows(request):
    if request.user.is_staff:
        context = {
            "overdue": Borrow.objects.filter(due__lt=date.today(), returned__exact=False).all(),
            "today": Borrow.objects.filter(due__exact=date.today(), returned__exact=False).all(),
            "week": Borrow.objects.filter(due__gt=date.today(), returned__exact=False).exclude(
                due__gt=(date.today() + timedelta(7))).all(),
            "later": Borrow.objects.filter(due__gt=(date.today() + timedelta(7)), returned__exact=False).all(),
        }
        return render(request, "library/index.html", context)
    else:
        context = {
            "name": request.user.student.first().name,
            "borrows": request.user.student.first().books.filter(returned__exact=False).all(),
        }
        return render(request, "library/personal.html", context)


@staff_member_required(login_url="accounts/login")
def completes(request):
    context = {
        "completes": Borrow.objects.filter(returned__exact=True).all()
    }
    return render(request, "library/completes.html", context)


@staff_member_required(login_url="accounts/login")
def borrow(request, borrow_id):
    try:
        borrow = Borrow.objects.get(pk=borrow_id)
    except Borrow.DoesNotExist:
        raise Http404("Borrow does not exist")

    context = {
        "borrow": borrow,
    }
    return render(request, "library/borrow.html", context)


@staff_member_required(login_url="accounts/login")
def returned(request, borrow_id):
    b = Borrow.objects.get(pk=borrow_id)
    if 'returned' in request.POST:
        b.returned = not b.returned
        b.save()
    elif 'delete' in request.POST:
        b.delete()
    return HttpResponseRedirect(reverse("borrows"))


@staff_member_required(login_url="accounts/login")
def add(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)

        if form.is_valid():
            borrower = form.cleaned_data['borrower']
            isbn = form.cleaned_data['isbn']
            teacher = form.cleaned_data['teacher']
            contact = form.cleaned_data['contact']

            Borrow.objects.create(
                borrower=borrower,
                isbn=isbn,
                teacher=teacher,
                contact=contact,
            ).save()

            return HttpResponseRedirect(reverse("borrows"))

    else:
        form = EntryForm()
    return render(request, "library/add.html", {"form": form})


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            student = form.cleaned_data['student']

            User.objects.create_user(username=username,
                                     email=email,
                                     password=password).student.add(student)

            user = authenticate(username=username, password=password)
            login(request, user)

            return HttpResponseRedirect(reverse("borrows"))

    else:
        form = SignUpForm()
    return render(request, "library/register.html", {"form": form})
