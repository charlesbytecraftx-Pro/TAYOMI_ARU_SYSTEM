from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Event
from .forms import EventForm
from django.db.models import Q

@login_required
def event_list(request):
    
    query = request.GET.get('q')
    
    if request.user.group:
        base_events = Event.objects.filter(
            Q(group=request.user.group) | Q(group__isnull=True)
        )
    else:
        base_events = Event.objects.filter(group__isnull=True)
    
    # Search Bar:
    if query:
        events = base_events.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(location__icontains=query)
        ).distinct().order_by('date', 'time')
    else:
        events = base_events.order_by('date', 'time')
        
    return render(request, 'events/event_list.html', {'events': events})

@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if event.group and request.user.group != event.group and not request.user.is_staff:
        messages.error(request, "Huna ruhusa ya kuona maelezo ya tukio hili.")
        return redirect('event_list')
    return render(request, 'events/event_detail.html', {'event': event})

@login_required
@user_passes_test(lambda u: u.is_staff)
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES) # request.FILES kwa ajili ya bango
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            if not form.cleaned_data.get('group'):
                event.group = None
            event.save()
            messages.success(request, "Tukio limeongezwa kikamilifu!")
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/add_event.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff)
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Tukio limefanyiwa marekebisho!")
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm(instance=event)
    return render(request, 'events/add_event.html', {
        'form': form, 
        'edit_mode': True, 
        'event': event
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        messages.success(request, "Tukio limefutwa kikamilifu!")
        return redirect('event_list')
    return render(request, 'events/event_confirm_delete.html', {'event': event})
