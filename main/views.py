from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from .models import Book, Section, Collaboration
from user.models import UserProfile
from .serializers import BookSerializer, SectionSerializer, CollaborationSerializer, BookDetailSerializer, SectionDetailSerializer, CollaborationDetailSerializer
from .permissions import IsAuthorOrCollaboratorWithEditPermission, IsAuthor

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    # Handle Action
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return BookDetailSerializer
        return BookSerializer

    # Handle Premission
    def get_permissions(self):
        permission_classes = []
        
        if self.action in ['create', 'update', 'partial_update']:
            permission_classes = [IsAuthor]
        return [permission() for permission in permission_classes]

    # Handle Create
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    # Handle Actions
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return SectionDetailSerializer
        return SectionSerializer

    # Handle Permissions
    def get_permissions(self):
        if self.action == 'create':
            print("workk")
            permission_classes = [IsAuthor]
        else:
            permission_classes = [IsAuthorOrCollaboratorWithEditPermission]
        return [permission() for permission in permission_classes]

class CollaborationViewSet(viewsets.ModelViewSet):
    queryset = Collaboration.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    # Handle Actions
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CollaborationDetailSerializer
        return CollaborationSerializer
    
    # Handle Premissions
    def get_permissions(self):
        permission_classes = []

        if self.action in ['create', 'update', 'partial_update']:
            permission_classes = [IsAuthor]
        return [permission() for permission in permission_classes]

    # Handle Create
    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user')
        book_id = request.data.get('book')
        can_edit = request.data.get('can_edit', False)

        book = Book.objects.get(id=book_id)

        try:
            user_profile = UserProfile.objects.get(user_id=user_id)
        except:
            return Response({'message': 'User profile role is not defined.'}, status=status.HTTP_403_FORBIDDEN)
        
        if user_profile.role == 'Collaborator':
            if self.request.user.id == book.author.id:
                serializer = CollaborationSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'message': 'Collaboration created successfully.'}, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'User does not have permission to add the collaborator.'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'message': 'Only collaborators role user can add in book as a collaborator.'}, status=status.HTTP_403_FORBIDDEN)