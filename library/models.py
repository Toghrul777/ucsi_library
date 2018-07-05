from datetime import date, timedelta
from django.utils.dateformat import format
from django.db import models


def get_due():
    fortnight = date.today() + timedelta(days=14)
    if fortnight.weekday() == 5:
        fortnight += timedelta(days=2)
    elif fortnight.weekday() == 6:
        fortnight += timedelta(days=1)
    return fortnight


# models here.


class Student(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.name}"



class Borrow(models.Model):
    borrower = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="books")
    isbn = models.CharField(max_length=15)
    teacher = models.CharField(max_length=30)
    contact = models.CharField(max_length=50)
    taken = models.DateField(default=date.today)
    due = models.DateField(default=get_due)
    returned = models.BooleanField(default=False)

    class Meta:
        ordering = ["returned", "due"]

    def __str__(self):
        return f"Book: {self.isbn} | " \
               f"{self.borrower} | " \
               f"Taken: {format(self.taken, 'l, F jS')} | " \
               f"Due: {format(self.due, 'l, F jS')} | " \
               f"Teacher: {self.teacher} | " \
               f"Contact: {self.contact} | " \
               f"{'Returned' if self.returned else 'Not Returned'}"
