from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from blog.models import signUpModel, Post, Category, Tag, Comment
from django.contrib.auth.hashers import make_password, check_password
from .forms import PostForm
from django.core.paginator import Paginator

# Create your views here.

# Decorator to check if user is logged in
def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            messages.error(request, 'You must be logged in to access this page')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

def post_list(request):
    postss = Post.objects.all().order_by('-created_at')
    paginator = Paginator(postss, 2)  # Show 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/post_list.html', {'page_obj': page_obj})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.views += 1
    post.save()
    comments = post.comments.all().order_by('-created_at')
    if request.method == 'POST':
        if not request.session.get('user_id'):
            messages.error(request, 'You must be logged in')
            return redirect('login')
        content = request.POST.get('content')
        user_id = request.session.get('user_id')
        user = signUpModel.objects.get(id=user_id)
        if content:
            post.comments.create(
                user=user,
                content=content
            )
            messages.success(request, 'Comment added successfully')
            return redirect('post_detail', post_id=post.id)
        else:
            messages.error(request, 'Comment cannot be empty')

    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments})


def post_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.likes += 1
    post.save()
    return redirect('post_detail', post_id=post.id)

def post_dislike(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.dislikes += 1
    post.save()
    return redirect('post_detail', post_id=post.id)

def login(request):
    if request.method == 'POST':
        user_name = request.POST.get('username')
        password = request.POST.get('password')
        if not user_name or not password:
            messages.error(request, 'Both fields are required')
            return redirect('login')
        try:
            user = signUpModel.objects.get(username=user_name)
            if check_password(password, user.password):

                request.session['user_id'] = user.id
                request.session['username'] = user.username

                messages.success(request, 'Login successful')
                return redirect('post_list')

            else:
                messages.error(request, 'Incorrect password')
                return redirect('login')
        except signUpModel.DoesNotExist:
            messages.error(request, 'Email not registered')
            return redirect('login')
      
    return render(request, 'user/login.html')


def logout(request):
    request.session.flush()
    messages.success(request, 'Logged out successfully')
    return redirect('post_list')


def signup(request):
    if request.method == 'POST':
        e_mail = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not e_mail or not username or not password or not confirm_password:
            messages.error(request, 'All fields are required')
            return redirect('signup')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')
        else:
            if signUpModel.objects.filter(email=e_mail).exists():
                messages.error(request, 'Email already registered')
                return redirect('signup')
            elif signUpModel.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken')
                return redirect('signup')
            else:
                if len(password) < 6:
                    messages.error(request, 'Password must be at least 6 characters long')
                    return redirect('signup')
                
                new_user = signUpModel.objects.create(
                    email=e_mail,
                    username=username, 
                    password=make_password(password)
                    )
                new_user.save()
                messages.success(request, 'Account created successfully. Please log in.')
                return redirect('login')
    return render(request, 'user/signup.html')


def user_profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    user = signUpModel.objects.get(id=user_id)
    return render(request, 'user/profile.html', {'user': user})


def update_profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    user = signUpModel.objects.get(id=user_id)
    if request.method == 'POST':
        new_email = request.POST.get('email')
        new_username = request.POST.get('username')
        new_password = request.POST.get('password')
        
        if new_email == user.email and new_username == user.username and not new_password:
            messages.info(request, 'No changes detected')
            return redirect('update_profile')
        
        if not new_email or not new_username:
            messages.error(request, 'Email and Username cannot be empty')
            return redirect('update_profile')

        if new_email != user.email and signUpModel.objects.filter(email = new_email).exists():
            messages.error(request, 'Email already in use')
            return redirect('update_profile')

        if new_username != user.username and signUpModel.objects.filter(username =new_username).exists():
            messages.error(request, 'Username already taken')
            return redirect('update_profile')

        user.email = new_email
        user.username = new_username

        if new_password:
            if len(new_password) < 6:
                messages.error(request, 'Password must be at least 6 characters long')
                return redirect('update_profile')
            if check_password(new_password, user.password):
                messages.info(request, 'New password cannot be the same as the old password')
                return redirect('update_profile')
            user.password = make_password(new_password)
        
        user.save()
        messages.success(request, 'Profile updated successfully')
        return redirect('profile')

    return render(request, 'blog/updateprofile.html', {'user': user})


@login_required
def create_post(request):
    categories = Category.objects.all()
    tags = Tag.objects.all()
    if request.method == 'POST':
       title = request.POST.get('title')
       content = request.POST.get('content')
       category_id = request.POST.get('category')
       tag_ids = request.POST.getlist('tags')
       user_id = request.session.get('user_id')

       category_obj = Category.objects.get(id=category_id)
       user = signUpModel.objects.get(id=user_id)

       new_post = Post.objects.create(
            title=title,
            content=content,
            author=user,
            category=category_obj
         )
       new_post.tags.set(tag_ids)
       new_post.save()
       messages.success(request, 'Post created successfully')
       return redirect('post_list')
    
    return render(request, 'blog/create_post.html', {'categories': categories, 'tags': tags})


def my_posts(request):
    user_id = request.session.get('user_id')
    user = signUpModel.objects.get(id=user_id)
    posts = Post.objects.filter(author=user).order_by('-created_at')
    return render(request, 'user/mypost.html', {'posts': posts})