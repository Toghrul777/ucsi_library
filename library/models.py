import requests
from datetime import date, timedelta
from django.contrib.auth.models import User
from django.utils.dateformat import format
from django.db import models


def get_due():
    fortnight = date.today() + timedelta(days=14)
    if fortnight.weekday() == 5:
        fortnight += timedelta(days=2)
    elif fortnight.weekday() == 6:
        fortnight += timedelta(days=1)
    return fortnight


def bookdata(isbn):
    url = "https://www.googleapis.com/books/v1/volumes?q= isbn:" + isbn
    resp = requests.get(url=url).json()
    info = resp["items"][0]["volumeInfo"]
    borrow = {
        "title": info["title"],
        "author": info["authors"][0],
        "image": info["imageLinks"]["thumbnail"]
    }
    return borrow


# models here.


class Student(models.Model):
    name = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="student")

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.name}"


class Borrow(models.Model):
    borrower = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="books")
    isbn = models.CharField(max_length=15)
    title = models.CharField(max_length=220, blank=True)
    author = models.CharField(max_length=220, blank=True)
    image = models.CharField(max_length=450, blank=True)
    teacher = models.CharField(max_length=30)
    contact = models.CharField(max_length=50)
    taken = models.DateField(default=date.today)
    due = models.DateField(default=get_due)
    returned = models.BooleanField(default=False)

    class Meta:
        ordering = ["returned", "due"]

    def save(self, *args, **kwargs):
        data = bookdata(self.isbn)
        self.title = data["title"]
        self.author = data["author"]
        self.image = data["image"]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Book: {self.title} | " \
               f"Student: {self.borrower} | " \
               f"Taken: {format(self.taken, 'l, F jS')} | " \
               f"Due: {format(self.due, 'l, F jS')} | " \
               f"Teacher: {self.teacher} | " \
               f"Contact: {self.contact} | " \
               f"{'Returned' if self.returned else 'Not Returned'}"

