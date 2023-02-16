from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_page, name='home'),
    path('snippets/add', views.add_snippet_page, name='snippet-add'),
    path('snippets/list', views.snippets_page, name='snippet-list'),
    path('snippet/<int:snippet_id>', views.snippet_detail, name='snippet-detail'),
    path('snippet/<int:snippet_id>/delete', views.snippet_delete, name="snippet-delete"),
    path('snippet/<int:snippet_id>/change', views.snippet_change, name="snippet-change"),
    path('comment/add', views.add_comment, name='comment-add'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout, name='logout'),
    path('snippets/my_snippets', views.snippets_my_snippets, name='snippet-my-snippets'),
    path('create_user/', views.create_user, name='create-user'),
    path('users/<str:snippet_user>', views.user_page, name='user-page'),
    path('users_rating', views.users_rating, name='users-rating'),
    path('snippet/<int:snippet_id>/thumbs_up', views.snippet_thumbs_up, name="snippet-thumbs-up"),
    path('snippet/<int:snippet_id>/thumbs_down', views.snippet_thumbs_down, name="snippet-thumbs-down"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
