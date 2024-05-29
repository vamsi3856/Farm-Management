from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile
import random
from efarming import settings
from twilio.rest import Client
from django.contrib.auth import authenticate, login

# Create your views here.


def send_otp(mobile, otp):
    print("FUNCTION CALLED")
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=f"The otp is {otp}", from_=settings.TWILIO_PHONE_NUMBER, to=f"+91{mobile}"
    )
    print(message)
    return None


def login_attempt(request):
    if request.method == "POST":
        mobile = request.POST.get("mobile")
        user = Profile.objects.filter(mobile=mobile).first()
        if user is None:
            context = {"message": "User not found", "class": "danger"}
            return render(request, "accounts/login.html", context)
        otp = '1234'
        user.save()
        # send_otp(mobile, otp)
        request.session["mobile"] = mobile
        request.session["otp"] = otp
        return redirect("login_otp")
    return render(request, "accounts/login.html")


def login_otp(request):
    mobile = request.session["mobile"]
    context = {"mobile": mobile}
    if request.method == "POST":
        otp = request.session['otp']
        entered_otp = request.POST.get("otp")
        print(otp, entered_otp)
        profile = Profile.objects.filter(mobile=mobile).first()
        if entered_otp == otp and profile is not None:
            user = User.objects.get(id=profile.user.id)
            login(request, user)
            print(user)
            return redirect("/")
        else:
            context = {"message": "Wrong OTP", "class": "danger", "mobile": mobile}
            return render(request, "accounts/login_otp.html", context)

    return render(request, "accounts/login_otp.html", context)


def register(request):
    if request.method == "POST":
        email = request.POST["email"]
        name = request.POST["first_name"]
        mobile = request.POST["mobile"]
        username = request.POST["username"]
        gender = request.POST["gender"]
        city = request.POST["city"]
        state = request.POST["state"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        if password1 == password2:
            if Profile.objects.filter(mobile=mobile).exists():
                messages.info(request, "Phone number is already Taken.")
                return render(request, "accounts/register.html", {"class": 'danger'})
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username is already Taken.")
                return render(request, "accounts/register.html", {"success": True})
            else:
                user = User.objects.create_user(
                    username=username, password=password1, email=email, first_name=name
                )
                otp = '1234'
                request.session["otp"] = otp
                request.session["mobile"] = mobile
                request.session['gender']=gender
                request.session['city']=city
                request.session['state']=state
                request.session['id']=user.id
                user.save()
                # send_otp(mobile, otp)
                return redirect("register_otp")
        else:
            messages.info(request, "Password is not matched")
            return render(request, "accounts/register.html", {"success": True})

    return render(request, "accounts/register.html")

def register_otp(request):
    mobile = request.session["mobile"]
    context = {"mobile": mobile}
    if request.method == "POST":
        otp = request.session['otp']
        entered_otp = request.POST.get("otp")
        # import pdb;pdb.set_trace()
        if entered_otp == otp :
            user = User.objects.get(id=request.session['id'])
            profile = Profile(user=user,gender=request.session['gender'],city=request.session['city'],state=request.session['state'],mobile=mobile)
            profile.save()
            login(request, user)
            print(user)
            return redirect("/")
        else:
            context = {"message": "Wrong OTP", "class": "danger", "mobile": mobile}
            return render(request, "accounts/login_otp.html", context)

    return render(request, "accounts/login_otp.html", context)



def logout(request):
    auth.logout(request)
    return redirect("/")
