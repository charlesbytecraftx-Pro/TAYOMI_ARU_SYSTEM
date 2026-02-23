from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Group

@login_required
def group_list(request): 
    groups = Group.objects.all()
    return render(request, 'groups/group_list.html', {'groups': groups})

@login_required
def join_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if not group.members.filter(id=request.user.id).exists():
        group.members.add(request.user)
        messages.success(request, f"Hongera! Umejiunga na {group.name}")
    return redirect('group_list')

@login_required
def group_members_view(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    is_member = group.members.filter(id=request.user.id).exists()
    
    if request.user.is_staff or is_member:
        members = group.members.all()
        total_all_members = User.objects.count() if request.user.is_staff else None
        return render(request, 'groups/group_members.html', {
            'group': group,
            'members': members,
            'total_all_members': total_all_members
        })
    else:
        messages.error(request, "Lazima ujiunge na kundi kwanza.")
        return redirect('group_list')
