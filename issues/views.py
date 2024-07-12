from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .forms import IssueCreateForm
from .models import Issue
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.db.models import Count
import json
from .models import Issue


@login_required
def issue_create_view(request):
    if request.method == 'POST':
        form = IssueCreateForm(request.POST)
        if form.is_valid():
            # Save the form and get the instance
            issue = form.save()
            # Redirect to the success view with the issue_id
            return redirect('issue_success', issue_id=issue.id)
        else:
            print(form.errors)  # Check form errors in console
    else:
        form = IssueCreateForm()
    return render(request, 'issues/issue_create.html', {'form': form})


@login_required
def issue_success_view(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    return render(request, 'issues/issue_success.html', {'issue': issue})


@login_required
def issue_edit_view(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    error_message = None  # Initialize the error message

    if request.method == 'POST':
        form = IssueCreateForm(request.POST, instance=issue)
        if form.is_valid():
            try:
                form.save()
                return redirect('issue_list')
            except ValueError as e:
                error_message = str(e)
    else:
        form = IssueCreateForm(instance=issue)

    return render(request, 'issues/issue_edit.html', {
        'form': form,
        'error_message': error_message
    })


@login_required
def issue_delete_view(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    if request.method == 'POST':
        issue.delete()
        return redirect('issue_list')  # Assuming you have an issue list view
    return render(request, 'issues/issue_delete.html', {'issue': issue})


@login_required
def issue_list_view(request):
    issues = Issue.objects.all()
    return render(request, 'issues/issue_list.html', {'issues': issues})


@login_required
def kanban_board_view(request):
    if request.method == 'POST':
        issue_id = request.POST.get('issue_id')
        new_status = request.POST.get('new_status')

        if issue_id and new_status:
            issue = get_object_or_404(Issue, id=issue_id)
            issue.status = new_status
            issue.save()
            return JsonResponse({
                'success': True,
                'message': 'Issue status updated successfully.'
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'Issue ID or new status not provided.'
            })

    else:
        issues = Issue.objects.all()
        return render(request, 'issues/kanban_board.html', {'issues': issues})


@require_POST
def update_issue_status(request, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    new_status = request.POST.get('new_status')

    if new_status in [
            'Pending Implementation', 'In Progress', 'Ready for UAT',
            'Ready to Deploy', 'Done'
    ]:
        issue.status = new_status
        issue.save()
        return JsonResponse({
            'success': True,
            'message': 'Issue status updated successfully.'
        })

    return JsonResponse({'success': False, 'message': 'Invalid status.'})


def issue_dashboard(request):
    # Query issues grouped by assignee and status, and count them
    issues_by_assignee = Issue.objects.values(
        'assignee__username', 'status').annotate(total=Count('id'))

    # Prepare data for Chart.js
    data = {}
    for issue in issues_by_assignee:
        assignee = issue['assignee__username']
        status = issue['status']
        if assignee not in data:
            data[assignee] = {'labels': [], 'data': []}
        data[assignee]['labels'].append(status)
        data[assignee]['data'].append(issue['total'])

    # Prepare data to pass to template
    context = {'data': data}

    return render(request, 'issues/dashboard.html', context)
