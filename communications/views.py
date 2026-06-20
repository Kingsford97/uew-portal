from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Announcement, Event, Notification
from .forms import AnnouncementForm, EventForm, NotificationForm


# ============ ANNOUNCEMENT VIEWS ============

@login_required
def announcements(request):
    announcements = Announcement.objects.filter(is_published=True).order_by('-published_date')
    return render(request, 'communications/announcements.html', {'announcements': announcements})


@login_required
def add_announcement(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.author = request.user
            announcement.is_published = True
            announcement.published_date = timezone.now()
            announcement.save()
            messages.success(request, 'Announcement created successfully!')
            return redirect('communications:announcements')
    else:
        form = AnnouncementForm()
    return render(request, 'communications/add_announcement.html', {'form': form})


# ============ EVENT VIEWS ============

@login_required
def events(request):
    events = Event.objects.filter(is_active=True).order_by('date')
    return render(request, 'communications/events.html', {'events': events})


@login_required
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event created successfully!')
            return redirect('communications:events')
    else:
        form = EventForm()
    return render(request, 'communications/add_event.html', {'form': form})


# ============ NOTIFICATION VIEWS ============

@login_required
def notifications(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    unread_count = notifications.filter(is_read=False).count()
    return render(request, 'communications/notifications.html', {
        'notifications': notifications,
        'unread_count': unread_count
    })


@login_required
def send_notification(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notification sent successfully!')
            return redirect('communications:notifications')
    else:
        form = NotificationForm()
    return render(request, 'communications/send_notification.html', {'form': form})


@login_required
def mark_notification_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
    notification.mark_as_read()
    messages.success(request, 'Notification marked as read.')
    return redirect('communications:notifications')