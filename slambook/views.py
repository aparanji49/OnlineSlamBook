from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from _datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.http import require_POST
from django.utils.timesince import timesince
from actions.models import Action
from .forms import CommentForm
from .models import regular_user, admin_user, Questions, Friends, Comment


# Create your views here.

# home
def slambook_home(request):
    actions = Action.objects.all().order_by('-created')
    return render(request, "slambook/index.html", {"actions": actions})


# help
def slambook_help(request):
    return render(request, "slambook/help.html")


# themes
def slambook_themes(request):
    return render(request, "slambook/themes.html")


# ==============
# friends
# =============

def slambook_friends(request):
    friends = Friends.objects.all().order_by('-dateUpdated').values()
    return render(request,
                  "slambook/friends.html",
                  {'friends': friends})


def slambook_friend_detail(request, friend_id):
    friends = Friends.objects.all()
    for friend in friends:
        if friend.id == friend_id:
            break
    return render(request,
                  "slambook/friendsdetail.html",
                  {'friend': friend})


def add_friend(request):
    if not request.session.get("username", False):
        return redirect('users:user_login_page')

    user = User.objects.get(username=request.session.get('username'))
    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        if name and email:
            friend = Friends(name=name, email=email, phone=phone, status="Send Form", )
            friend.save()
            # log the action
            action = Action(
                user=user,
                verb="added friend",
                target=friend
            )
            action.save()
            messages.add_message(request, messages.SUCCESS, "You have successfully added friend: %s" % friend.name)
            return redirect('slambook:slambook_friends')

    return render(request, "slambook/friends.html")


def edit_friend(request, friend_id):
    friend = get_object_or_404(Friends, id=friend_id)
    user = User.objects.get(username=request.session.get('username'))

    if request.method == 'POST':
        name = request.POST.get("name")
        print(name)
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        # Check if there are any changes
        if name != friend.name or email != friend.email or phone != friend.phone:
            friend.name = name
            friend.email = email
            friend.phone = phone
            friend.save(force_update=True)
            # log the action
            action = Action(
                user=user,
                verb="edited friend",
                target=friend
            )
            action.save()
            messages.add_message(request, messages.INFO, "You have successfully updated friend: %s" % friend.name)
            return redirect('slambook:slambook_friend_detail', friend_id=friend.id)
        else:
            print("no changes")

    return render(request, "slambook/friendsdetail.html", {'friend': friend})


def delete_friend(request, friend_id):
    friend = get_object_or_404(Friends, id=friend_id)
    user = User.objects.get(username=request.session.get('username'))
    if request.method == 'POST':
        if request.POST.get("confirm_delete") == "1":
            friend.delete()
            # # log the action
            # action = Action(
            #     user=user,
            #     verb="deleted friend",
            #     target=friend
            # )
            # action.save()
            messages.add_message(request, messages.WARNING, "You have deleted friend: %s" % friend.name)
            return redirect('slambook:slambook_friends')

    return render(request, "slambook/friendsdetail.html", {'friend': friend})


# =============
#  questions
# ===========

def slambook_questions(request):
    questions = Questions.objects.all()
    return render(request,
                  "slambook/questions.html",
                  {'questions': questions})


def slambook_question_detail(request, question_id):
    questions = Questions.objects.all()
    for question in questions:
        if question.id == question_id:
            break
    return render(request,
                  "slambook/questionsdetail.html",
                  {'question': question})


def add_question(request):
    if not request.session.get("username", False):
        return redirect('users:user_login_page')

    if request.method == 'POST':
        questionName = request.POST.get("question")
        user = User.objects.get(username=request.session.get('username'))

        if questionName:
            question = Questions(question=questionName)
            question.save()
            # log the action
            action = Action(
                user=user,
                verb="added question",
                target=question
            )
            action.save()
            messages.add_message(request, messages.SUCCESS,
                                 "You have successfully added question: %s" % question.question)
            return redirect('slambook:slambook_questions')

    return render(request, "slambook/questions.html")


def edit_question(request, question_id):
    question = get_object_or_404(Questions, id=question_id)

    if request.method == 'POST':
        questionName = request.POST.get("question")
        user = User.objects.get(username=request.session.get('username'))

        # Check if there are any changes
        if questionName != question.question:
            question.question = questionName
            question.save(force_update=True)
            # log the action
            action = Action(
                user=user,
                verb="edited question",
                target=question
            )
            action.save()
            messages.add_message(request, messages.INFO,
                                 "You have successfully updated question: %s" % question.question)
            return redirect('slambook:slambook_question_detail', question_id=question.id)
        else:
            print("no changes")

    return render(request, "slambook/questionsdetail.html", {'question': question})


def delete_question(request, question_id):
    question = get_object_or_404(Questions, id=question_id)
    user = User.objects.get(username=request.session.get('username'))

    if request.method == 'POST':
        if request.POST.get("confirm_delete") == "1":
            question.delete()
            # # log the action
            # action = Action(
            #     user=user,
            #     verb="deleted question",
            #     target=question
            # )
            # action.save()
            messages.add_message(request, messages.WARNING, "You have deleted question: %s" % question.question)
            return redirect('slambook:slambook_questions')

    return render(request, "slambook/questionsdetail.html", {'question': question})


#
# def addquestion(request):
#     question = request.POST.get("questioninput")
#     if question != "":
#         question1 = Questions(question, datetime.now())
#         questions.append(question1)
#     return render(request, "slambook/questions.html")

# def delete_row(request):
#     # Retrieve the object based on the provided ID, or return a 404 error if it doesn't exist
#
#     if request.method == 'POST':
#         deleted_id = int(request.POST.get('delete_id', -1))# Get the ID to delete
#         if deleted_id > 0:
#             data = [item for item in questions if questions['id'] != deleted_id]  # Remove the row by ID
#
#     context = {'data': data}
#     return render(request, 'slambook/questions.html', context)


#
# def search_friends(request):
#     if request.method == 'GET':
#         searchterm = request.GET['searchterm']
#         if searchterm:
#             # Perform a search in your database
#             friends = Friends.objects.filter(name__icontains=searchterm)
#             friend_data = []  # List to store friend data
#
#             for friend in friends:
#                 friend_data.append({
#                     'name': friend.name,
#                     'status': friend.status,
#                     'dateUpdated': friend.dateUpdated | naturaltime,  # Format the date as needed
#                 })
#
#             return JsonResponse(friend_data, safe=False)  # Return search results as JSON
#
#     return JsonResponse([], safe=False)  # Return an empty JSON response if no results are found
#
#
# def sort_friends(request):
#     if request.method == 'GET':
#         # Retrieve and sort the friends by name
#         friends = Friends.objects.all().order_by('name')
#         friend_data = []
#
#         for friend in friends:
#             friend_data.append({
#                 'name': friend.name,
#                 'status': friend.status,
#                 'dateUpdated': friend.dateUpdated | naturaltime,
#             })
#
#         return JsonResponse(friend_data, safe=False)
#     else:
#         return JsonResponse([], safe=False)
def slambook_responses(request):
    return render(request, "slambook/responses.html")


def slambook_received_requests(request):
    return render(request, "slambook/received_requests.html")


def slambook_friend_form_detail(request, friend_id):
    friends = Friends.objects.all()
    for friend in friends:
        if friend.id == friend_id:
            break
    return render(request,
                  "slambook/friendformdetails.html",
                  {'friend': friend})


# def slambook_friend_response(request, friend_id):
#     return render(request, "slambook/responses.html")


# ======================
# comments
# =====================

def comment_list(request, friend_id):
    friend = get_object_or_404(Friends, id=friend_id)
    comments = Comment.objects.filter(friend=friend).order_by('-timestamp')
    return render(request, 'slambook/friendsdetail.html', {'friend': friend, 'comments': comments})


def add_comment(request, friend_id):
    friend = get_object_or_404(Friends, id=friend_id)

    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = User.objects.get(username=request.session.get('username'))
        comment.friend = friend
        comment.save()
        # Convert timestamp to humanized format
        humanized_timestamp = timesince(comment.timestamp)
        return JsonResponse(
            {'success': True, 'text': comment.text, 'username': comment.user.username, 'timestamp': comment.timestamp,
             'timestamp_humanized': humanized_timestamp})
    else:
        return JsonResponse({'success': False, 'errors': form.errors})


def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user == comment.user:
        if request.method == 'POST':
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()

                # Convert timestamp to humanized format
                humanized_timestamp = timesince(comment.timestamp)

                return JsonResponse({'success': True,
                                     'text': comment.text,
                                     'timestamp': comment.timestamp.isoformat(),
                                     'timestamp_humanized': humanized_timestamp})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})
        else:
            form = CommentForm(instance=comment)

        return render(request,
                      'slambook/comment_form.html',
                      {'form': form, 'comment': comment})
    else:
        return JsonResponse({'success': False, 'errors': "You don't have permission to edit this comment."})
