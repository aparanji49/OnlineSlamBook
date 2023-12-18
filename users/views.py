from django.contrib.auth import authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect


# Create your views here.
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.create_user(username=username, email=email, password=password, first_name=firstname,
                                        last_name=lastname)
        messages.add_message(request, messages.SUCCESS,
                             "You have successfully registered with the username: %s" % user.username)
        return redirect('slambook:slambook_home')
    else:
        return render(request, "users/user/signup.html")


def profile(request, username):
    if not request.session.get("username", False):
        messages.add_message(request, messages.ERROR,
                             "Please login to view any user's profile")
        return redirect('slambook:slambook_home')
    else:
        user = get_object_or_404(User, username=username)
        current_s_user = User.objects.get(username=request.session.get("username"))
        return render(request,
                      "users/user/profile.html",
                      {"user": user, "current_username": current_s_user.username,
                       "current_role": current_s_user.details.role})


@csrf_protect
def login_user(request):
    username = request.POST.get("uname")
    password = request.POST.get("pw")
    user = authenticate(username=username, password=password)

    if user is not None:
        request.session['username'] = user.username
        request.session['role'] = user.details.role
        messages.add_message(request, messages.SUCCESS,
                             "You have logged in successfully")
        if user.details.role == "regular":
            return redirect('slambook:slambook_home')
        elif user.details.role == "admin":
            return redirect('slambook:slambook_themes')
    else:
        messages.add_message(request, messages.ERROR,
                             "Invalid username or password")
        return redirect('users:user_login_page')


def user_login_page(request):
    return render(request, "users/user/login.html")


def logout_user(request):
    del request.session['username']
    del request.session['role']
    return redirect('slambook:slambook_home')


def list_users(request):
    all_users = User.objects.all().filter(details__role="regular")
    print(list(all_users.values()))
    return render(request, "users/user/list_users.html", {"all_users": all_users})


#
# def make_user_admin(request, username):
# if request.method == 'POST':
#     drop_val = request.POST.get('make_admin')
#     if drop_val == "yes":
#         user = User.objects.get(username=username)
#         print(user)
#         user.details.role = "admin"
#         user.save()
#         # current_username = request.session.get('username')
#         # print(current_username)
#         # current_user = get_object_or_404(User, username=current_username)
#         current_user = User.objects.get(username=request.session.get("username"))
#         current_user.details.role = "regular"
#         current_user.save()
#         logout_user(request)
#     else:
#         return redirect('users:list_users')
def update_profile(request, username):
    user = User.objects.get(username=username)
    # current_s_user = User.objects.get(username=request.session.get("username"))
    if request.method == 'POST':
        email = request.POST.get('profile_email')
        first_name = request.POST.get('profile_first_name')
        last_name = request.POST.get('profile_last_name')
        password = request.POST.get('profile_password')
        school = request.POST.get('schools')

        # Check if there are any changes
        if (email != user.email or
                first_name != user.first_name or
                last_name != user.last_name or
                user.check_password(password) or school != school):
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            # user.password = password
            user.details.school = school
            user.set_password(password)
            user.save(force_update=True)
            messages.add_message(request, messages.INFO,
                                 "You have successfully updated your profile: %s" % user.username)
            # {"user": user, "current_username": current_s_user.username, "current_role":current_s_user.details.role})
            return redirect('users:profile', username=user.username)
        else:
            print("no changes")

    return redirect('users:profile', username=user.username)
