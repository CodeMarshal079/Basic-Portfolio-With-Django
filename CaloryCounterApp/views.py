from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth import login, logout
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def registerPage(request):
    if request.method == "POST":
        form = UserForm(request.POST)

        if form.is_valid():
            user = form.save()

            ProfileModel.objects.get_or_create(user=user)

            messages.success(request, "User Created Successfully")
            return redirect("login")
    else:
        form = UserForm()

    con = {
        "form": form,
        "title": "Register Here",
        "btn": "Register"
    }

    return render(request, "pages/baseForm.html", con)


def loginPage(request):
    if request.method == "POST":
        form = AuthForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()

            if user:
                login(request, user)
                messages.success(request, "User Login Successfully")
                return redirect("dashboard")
    else:
        form = AuthForm()

    con = {
        "form": form,
        "title": "Login Here",
        "btn": "Login"
    }

    return render(request, "pages/baseForm.html", con)


def logoutPage(request):
    logout(request)
    messages.success(request, "User Logged Out")
    return redirect("login")


@login_required
def profileUpdatePage(request):
    profile, created = ProfileModel.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=profile)

        if form.is_valid():
            data = form.save(commit=False)

            if data.gender == "male":
                data.bmr = (
                    66.47 + (13.75 * float(data.weight)) + (5.003 * float(data.height)) - (6.755 * float(data.age)))
            else:
                data.bmr = (655.1 + (9.563 * float(data.weight)) +
                            (1.850 * float(data.height)) - (4.675 * float(data.age)))

            data.save()

            messages.success(
                request,
                "Profile Updated Successfully"
            )

            return redirect("dashboard")
    else:
        form = ProfileUpdateForm(instance=profile)

    con = {
        "form": form,
        "title": "Update Your Profile",
        "btn": "Update"
    }

    return render(request, "pages/baseForm.html", con)


@login_required
def consumePage(request):
    if request.method == "POST":
        form = ConsumeForm(request.POST)

        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.save()

            messages.success(
                request,
                "Consumed Calory Added Successfully"
            )

            return redirect("dashboard")
    else:
        form = ConsumeForm()

    con = {
        "form": form,
        "title": "Add Consumed Item",
        "btn": "Add"
    }

    return render(request, "pages/baseForm.html", con)


@login_required
def dashboardPage(request):
    profile, created = ProfileModel.objects.get_or_create(
        user=request.user
    )

    bmr = profile.bmr or 0

    consume_data = (
        ConsumeCaloryModel.objects
        .filter(user=request.user)
        .aggregate(total=Sum("calory"))["total"]
        or 0
    )

    remain = bmr - consume_data

    con = {
        "profile": profile,
        "bmr": round(bmr, 2),
        "consumed_data": round(consume_data, 2),
        "remain": round(remain, 2)
    }

    return render(request, "pages/dashboard.html", con)
