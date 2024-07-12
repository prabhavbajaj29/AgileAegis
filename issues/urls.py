# issues/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.issue_create_view, name='issue_create'),
    path('success/<int:issue_id>/', views.issue_success_view, name='issue_success'),
    path('edit/<int:issue_id>/', views.issue_edit_view, name='issue_edit'),
    path('delete/<int:issue_id>/', views.issue_delete_view, name='issue_delete'),
    path('', views.issue_list_view, name='issue_list'),
    path('kanban/', views.kanban_board_view, name='kanban_board'),  # Ensure this is correct
    path('update_issue_status/<int:issue_id>/', views.update_issue_status, name='update_issue_status'),
    path('dashboard/', views.issue_dashboard, name='issue_dashboard'),
]
