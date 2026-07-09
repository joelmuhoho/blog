from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
import time, os
from django.http import HttpResponse

from .forms import PostForm, CommentForm, UserForm
from .models import Post, Comment
from django.db.models import Q
from django.contrib.auth.models import User



def post_list(request):
    """
    Retrieves a list of published posts and renders the 'blog/post_list.html' template with the posts and their count.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered 'blog/post_list.html' template with the posts and their count.
    """

    posts = Post.objects.filter(
        published_date__lte=timezone.now()).order_by('-published_date')
    posts_count = str(posts.count())
    stuff_for_frontend = {'posts': posts, 'posts_count': posts_count, }
    return render(request, 'blog/post_list.html', stuff_for_frontend)


def search(request):
    """
    Searches for posts based on a user query and returns a rendered HTML template with the search results.

    Parameters:
        request (HttpRequest): The HTTP request object containing the user query.

    Returns:
        HttpResponse: The rendered HTML template with the search results.
    """
    user_query = str(request.GET.get('query', ''))
    search_result = Post.objects.filter(
        title__contains=user_query).order_by('-published_date')
    posts = search_result
    if search_result.count() == 0:
        posts = Post.objects.filter(
            published_date__lte=timezone.now()).order_by('-published_date')
        stuff_for_frontend = {'posts': posts}
        messages.warning(request, 'Results containing ' +
                         user_query + ' Not found, Sorry!')
        return render(request, 'blog/post_list.html', stuff_for_frontend)

    else:
        stuff_for_frontend = {'posts': posts}
        post_found = str(search_result.count())
        messages.success(request, 'About '+post_found+' results ')
        return render(request, 'blog/post_list.html', stuff_for_frontend)


def post_detail(request, pk):
    """
    Retrieves details of a specific post and related information for rendering on the post detail page.

    Parameters:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the post to retrieve.

    Returns:
        HttpResponse: The rendered post detail page with the post details and related information.
    """
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    author_name = post.author
    user_name = request.user
    author_posts = Post.objects.filter(author=author_name, published_date__isnull=False)
    author_posts_count = str(author_posts.count())
    author_details = User.objects.get(username=author_name)
    stuff_for_frontend = {'post': post, 'form': form,
                          'author_details': author_details,
                          'author_posts_count': author_posts_count,
                          'author_posts': author_posts,
                          'author_name': author_name,
                          'user_name': user_name}
    return render(request, 'blog/post_detail.html', stuff_for_frontend)


@login_required
def post_new(request):
    """
    Creates a new post based on the form data submitted.
    If the request method is 'POST', it validates the form, saves the post as a draft, and redirects to the post detail page.
    If the request method is not 'POST', it initializes a new form for creating a post and provides necessary information for rendering the post edit page.
    """
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if not form.is_valid():
            messages.error(request, form.errors)
            return render(request, 'blog/post_edit.html', {'form': form})
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        messages.info(
                request, 'Posted as Draft. Now Publish for Everyone to see')
        return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
        stuff_for_frontend = {'form': form}
        messages.info(request, 'Add New Post')
        return render(request, 'blog/post_edit.html', stuff_for_frontend)


@login_required
def post_edit(request, pk):
    """
    Updates an existing post based on the form data submitted.
    If the request method is 'POST', it validates the form, saves the post with updates, and redirects to the post detail page.
    If the request method is not 'POST', it initializes a form with the existing post data for editing and provides necessary information for rendering the post edit page.
    """
    post = get_object_or_404(Post, pk=pk)
    old_image_path=''
    if post.image:
        old_image_path = post.image.path
    if request.method == 'POST':
        # updating an existing form
        form = PostForm(request.POST, request.FILES, instance=post)
        if not form.is_valid():
            messages.error(request, form.errors)
            return render(request, 'blog/post_edit.html', {'form': form})

        # Delete the old image
        if post.image and 'image' in request.FILES:
            if os.path.exists(old_image_path):
                os.remove(old_image_path)

        post = form.save(commit=False)
        post.author = request.user
        post.edited_date = timezone.now()
        post.save()
        messages.success(request, 'Post Updated')
        return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
        stuff_for_frontend = {'form': form, 'post': post}
        messages.info(request, 'Edit Post')
    return render(request, 'blog/post_edit.html', stuff_for_frontend)


@login_required
def post_draft_list(request):
    """
    Retrieves a list of draft posts and renders the 'blog/post_draft_list.html' template with the draft posts.
    Parameters:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: The rendered 'blog/post_draft_list.html' template with the draft posts.
    """
    user_name = request.user
    user_id = User.objects.filter(username=user_name).first().pk
    post = Post.objects.filter(
        published_date__isnull=True, author=user_id).order_by('-created_date')
    stuff_for_frontend = {'posts': post}
    return render(request, 'blog/post_draft_list.html', stuff_for_frontend)


@login_required
def post_publish(request, pk):
    """
    Publishes a post with the given primary key if the user is logged in.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the post to be published.

    Returns:
        HttpResponseRedirect: A redirect to the post detail page with the published post.

    Raises:
        Http404: If the post with the given primary key does not exist.

    """
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    messages.success(request, 'Post Published Successfully. Everyone can see')
    return redirect('post_detail', pk=pk)


@login_required
def post_delete(request, pk):
    """
    Deletes a post with the given primary key if the user is logged in.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the post to be deleted.

    Returns:
        HttpResponseRedirect: A redirect to the homepage after deleting the post.

    """
    post = get_object_or_404(Post, pk=pk)
    old_image_path = ''
    if post.image:
        old_image_path = post.image.path
    post.delete()
    # Delete post image
    if old_image_path and os.path.exists(old_image_path):
        os.remove(old_image_path)
    messages.success(request, 'Post was Deleted Successfully')
    return redirect('/', pk=post.pk)


@login_required
def add_comment_to_post(request, pk):
    """
    Adds a comment to a post based on the request and post primary key.

    Parameters:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the post.

    Returns:
        HttpResponseRedirect: Redirects to the post detail page after adding the comment.
    """
    post = get_object_or_404(Post, pk=pk)
    print(post)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
        return render(request, 'blog/post_detail.html', {'form': form, 'post': post})


@login_required
def comment_remove(request, pk):
    """
    Deletes a comment with the given primary key if the user is logged in.

    Parameters:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the comment to be deleted.

    Returns:
        HttpResponseRedirect: Redirects to the post detail page after deleting the comment.
    """
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    messages.success(request, 'Comment was Deleted Successfully')
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_approve(request, pk):
    """
    Approves a comment with the given primary key if the user is logged in.

    Parameters:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the comment to be approved.

    Returns:
        HttpResponseRedirect: Redirects to the post detail page after approving the comment.
    """
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    messages.success(request, 'You Approved the Comment Successfully')
    return redirect('post_detail', pk=comment.post.pk)


def signup(request):
    """
    Sign up a new user.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered signup page with the form or a redirect to the homepage if the form is valid.
    """
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(request, new_user)
            messages.success(request, 'Welcome ' + new_user.username +
                             ' Your account ha been Created Successfully.')
            return redirect('/')
    else:
        form = UserForm()
    return render(request, 'registration/signup.html', {'form': form})


def userProfile(request):
    """
    Renders the user profile page.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered user profile page.
    """
    profile = request.user
    user_pk = User.objects.get(username=profile).pk
    try:
        user_posts = Post.objects.filter(author=user_pk).all()
    except Post.DoesNotExist:
        user_posts = []
    return render(request, 'blog/user_profile.html', {'profile': profile, 'user_posts': user_posts })

def user_posts(request):
    """
    Retrieves the posts created by the logged-in user and renders the 'blog/user_posts.html' template with the posts and related information.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered 'blog/user_posts.html' template with the user's posts, the count of posts, and the user object.
    """
    user= request.user
    user_pk = User.objects.get(username=user).pk
    user_posts = Post.objects.filter(author=user_pk)
    post_count = user_posts.count()
    stuff_for_frontend = {'user_posts': user_posts, 'post_count': post_count, 'user': user}
    return render(request, 'blog/user_posts.html', stuff_for_frontend )