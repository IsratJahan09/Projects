from django.urls import include, path

from blog.views import login, logout, my_posts, signup, post_list, update_profile, user_profile, create_post, post_detail, post_like, post_dislike

urlpatterns = [
    path('', post_list, name='post_list'),
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', logout, name='logout'),
    path('profile/', user_profile, name='profile'),
    path('update_profile/', update_profile, name='update_profile'),
    path('create/', create_post, name='create_post'),
    path('post_detail/<int:post_id>/', post_detail, name='post_detail'),
    path('post/<int:post_id>/like/', post_like, name='post_like'),
    path('post/<int:post_id>/dislike/', post_dislike, name='post_dislike'),
    path('my_posts/', my_posts, name='my_posts'),

    
]