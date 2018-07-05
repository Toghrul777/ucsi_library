from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from library.models import Borrow, Student
from django.utils.dateformat import format
from datetime import date, timedelta


def borrows(request):
    context = {
        "overdue": Borrow.objects.filter(due__lt=date.today(), returned__exact=False).all(),
        "today": Borrow.objects.filter(due__exact=date.today(), returned__exact=False).all(),
        "week": Borrow.objects.filter(due__gt=date.today(), returned__exact=False).exclude(
            due__gt=(date.today() + timedelta(7))).all(),
        "later": Borrow.objects.filter(due__gt=(date.today() + timedelta(7)), returned__exact=False).all(),
    }
    return render(request, "library/index.html", context)


def completes(request):
    context = {
        "completes": Borrow.objects.filter(returned__exact=True).all()
    }
    return render(request, "library/completes.html", context)


def borrow(request, borrow_id):
    try:
        borrow = Borrow.objects.get(pk=borrow_id)
    except Borrow.DoesNotExist:
        raise Http404("Borrow does not exist")

    context = {
        "borrow": borrow,
        "taken": format(borrow.taken, 'jS F Y'),
        "due": format(borrow.due, 'jS F Y')
    }
    return render(request, "library/borrow.html", context)



def returned(request, borrow_id):
    b = Borrow.objects.get(pk=borrow_id)
    if 'returned' in request.POST:
        b.returned = not b.returned
        b.save()
    elif 'delete' in request.POST:
        b.delete()
    return HttpResponseRedirect(reverse("borrows"))