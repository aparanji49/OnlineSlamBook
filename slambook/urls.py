from django.urls import path
from . import views

app_name = 'slambook'
urlpatterns = [
    # slambook views
    path('', views.slambook_home, name='slambook_home'),
    path('themes/', views.slambook_themes, name='slambook_themes'),
    path('friends/', views.slambook_friends, name='slambook_friends'),
    path('questions/', views.slambook_questions, name='slambook_questions'),
    path('help/', views.slambook_help, name='slambook_help'),
    path('responses/', views.slambook_responses, name='slambook_responses'),
    path('receivedrequests/', views.slambook_received_requests, name='slambook_received_requests'),
    path('friends/<int:friend_id>', views.slambook_friend_detail, name='slambook_friend_detail'),
    path('questions/<int:question_id>', views.slambook_question_detail, name='slambook_question_detail'),
    path('friends/<int:friend_id>/form', views.slambook_friend_form_detail, name='slambook_friend_form_detail'),
    # path('responses/<int:friend_id>', views.slambook_friend_response, name="slambook_friend_response"),
    path('friends/add_friend', views.add_friend, name='add_friend'),
    path('friends/<int:friend_id>/edit', views.edit_friend, name='edit_friend'),
    path('friends/<int:friend_id>/delete', views.delete_friend, name='delete_friend'),
    path('questions/add_question', views.add_question, name='add_question'),
    path('questions/<int:question_id>/edit', views.edit_question, name='edit_question'),
    path('questions/<int:question_id>/delete', views.delete_question, name='delete_question'),
    path('friends/<int:friend_id>/comments/', views.comment_list, name='comment_list'),
    path('friends/<int:friend_id>/comment/add/', views.add_comment, name='add_comment'),
    path('friends/comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    # path('search_friends/', views.search_friends, name='search_friends'),
    # path('sort_friends/', views.sort_friends, name='sort_friends'),

]
