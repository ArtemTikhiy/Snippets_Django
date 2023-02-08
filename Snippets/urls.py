from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views

urlpatterns = [
    path('', views.index_page, name='home'),
    path('snippets/add', views.add_snippet_page, name='snippet-add'),
    path('snippets/list', views.snippets_page, name='snippet-list'),
    path('snippet/<int:snippet_id>', views.snippet_detail, name='snippet-detail'),
    path('snippet/<int:snippet_id>/delete', views.snippet_delete, name="snippet-delete"),
    path('snippet/<int:snippet_id>/change', views.snippet_change, name="snippet-change"),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout, name='logout'),
    path('snippets/my_snippets', views.snippets_my_snippets, name='snippet-my-snippets'),
    path('create_user/', views.create_user, name='create-user'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
