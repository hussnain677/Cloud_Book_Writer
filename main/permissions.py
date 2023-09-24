from rest_framework import permissions
from django.shortcuts import get_object_or_404
from .models import Section

class IsAuthorOrCollaboratorWithEditPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'create':
            return IsAuthor().has_permission(request, view)
        elif view.action in ['update', 'partial_update']:
            # For update actions, check if the user can_edit the associated book
            section_pk = request.parser_context['kwargs']['pk']
            print(section_pk)
            section = get_object_or_404(Section, id=section_pk)
            return section.book.collaborators.filter(pk=request.user.pk, collaboration__can_edit=True).exists()
        else:
            # For other actions like list and retrieve, allow read-only access
            return True

class IsAuthor(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        user_profile = user.userprofile if hasattr(user, 'userprofile') else None

        # Check if the user is an Author
        return user_profile and user_profile.role == 'Author'
