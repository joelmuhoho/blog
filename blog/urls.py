from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # 127.0.0.1:8000 ==> local
    # mydjangoblog.com ==> online
    path('', views.post_list, name='post_list'),

    # 127.0.0.1:8000/post/3 ==> local
    # mydjangoblog.com/post/3 ==> online
    path('post/<int:pk>/', views.post_detail, name='post_detail'),

    # 127.0.0.1:8000/post/new ==> local
    # mydjangoblog.com/post/new ==> online
    path('post/new/', views.post_new, name='post_new'),

    # 127.0.0.1:8000/post/3/edit ==> local
    # mydjangoblog.com/post/3/edit ==> online
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),

    # 127.0.0.1:8000/post/3/delete ==> local
    # mydjangoblog.com/post/3/delete ==> online
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),

    # 127.0.0.1:8000/drafts ==> local
    # mydjangoblog.com/drafts ==> online
    path('drafts/', views.post_draft_list, name='post_draft_list'),

    # 127.0.0.1:8000/post/3/publish ==> local
    # mydjangoblog.com/post/3/publish ==> online
    path('post/<int:pk>/publish/', views.post_publish, name='post_publish'),

    # 127.0.0.1:8000/post/3/comment ==> local
    # mydjangoblog.com/post/3/comment ==> online
    path('post/<int:pk>/comment/', views.add_comment_to_post,
         name='add_comment_to_post'),

    # 127.0.0.1:8000/comment/3/remove ==> local
    # mydjangoblog.com/comment/3/remove ==> online
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),

    # 127.0.0.1:8000/comment/3/approve ==> local
    # mydjangoblog.com/comment/3/approve ==> online
    path('comment/<int:pk>/approve/',
         views.comment_approve, name='comment_approve'),

    # 127.0.0.1:8000/signup ==> local
    # mydjangoblog.com/signup ==> online
    path('signup/', views.signup, name='signup'),

    # 127.0.0.1:8000/search ==> local
    # mydjangoblog.com/search ==> online
    path('post/search/', views.search, name='search'),

    # 127.0.0.1:8000/profile ==> local
    # mydjangoblog.com/profile ==> online
    path('profile/', views.userProfile, name='profile'),


    # 127.0.0.1:8000/profile ==> local
    # mydjangoblog.com/profile ==> online
    path('user_posts/', views.user_posts, name='user_posts'),


]
if settings.DEBUG:urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)