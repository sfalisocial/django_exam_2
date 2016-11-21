from django.shortcuts import render, redirect
from django.contrib import messages
from ..logreg.models import User
from .models import Wish, Shared
from datetime import datetime, date

def loggedin(request):
    if 'logged_user' not in request.session:
        messages.error(request, "You must login to view this page!")
        return redirect('/')

def index(request):
    loggedin(request)
    me = User.objects.get(id=request.session['logged_user'])

    my_wishes = Wish.objects.filter(creator=me)
    shared_wishes = Wish.objects.filter(shared__adder_id=me)
    wishes = my_wishes | shared_wishes

    other_wishes = Wish.objects.exclude(id__in=wishes)

    context = {
        "user": me,
        "wishes": wishes,
        "other_wishes" : other_wishes,
    }
    return render(request,'exam/index.html', context)

def new(request):
    loggedin(request)
    return render(request,'exam/new.html')

def create(request):
    loggedin(request)
    if request.method == "POST":
        form_errors = Wish.objects.validation(request.POST)
        print form_errors
        if form_errors:
            for error in form_errors:
                messages.error(request, error)
            return redirect('wish:new')
        else:
            user = User.objects.get(id=request.session['logged_user'])
            Wish.objects.create(wish=request.POST['wish'],description=request.POST['desc'],creator=user)
            messages.success(request, "Successfully added a wish!")
            return redirect('wish:index')


def viewWish(request, id):
    loggedin(request)
    wish = Wish.objects.filter(id=id)
    other_wishes = Shared.objects.filter(sharedwish=wish)
    context = {
        "wish" : wish,
        "adders" : other_wishes,
    }
    return render(request,'exam/view.html', context)


def addWish(request, id):
    loggedin(request)
    me = User.objects.get(id=request.session['logged_user'])
    sharedwish = Wish.objects.get(id=id)
    Shared.objects.create(adder=me, sharedwish=sharedwish)
    return redirect('wish:index')

def destroy(request, id):
    loggedin(request)
    wish = Wish.objects.get(id=id)
    if request.method == "GET":
        context = {
            "wish":wish,
        }
        return render(request, 'exam/destroy.html', context)
    wish.delete()
    return redirect('wish:index')

def remove(request, id):
    loggedin(request)
    wish = Shared.objects.get(sharedwish_id=id)
    wish.delete()
    return redirect('wish:index')
