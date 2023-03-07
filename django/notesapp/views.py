from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from notesapp.serializers import *


class AuthView(viewsets.ViewSet):
    """
    Auhorization methods
    """
    permission_classes = (AllowAny,)
    serializer_class = AuthorizationSerializer

    @action(methods=['POST'], detail=False, url_path='signup', url_name='Sign Up User', permission_classes=permission_classes)
    def signup(self, request):
        data = request.data
        serializer = self.serializer_class(data=data, context={"signup": True, "request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=False, url_path='signin', url_name='Sign In User', permission_classes=permission_classes)
    def signin(self, request):
        data = request.data
        serializer = self.serializer_class(data=data, context={"signup": False, "request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserView(viewsets.ViewSet):
    """
    User methods
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = UserDetailSerializer

    @action(methods=['GET'], detail=False, url_path='me', url_name='About User', permission_classes=[IsAuthenticated])
    def about_user(self, request, *args, **kwargs):
        return Response(self.serializer_class(instance=request.user, context={"request": request}).data, status=status.HTTP_200_OK)


class NoteView(viewsets.ModelViewSet):
    """
    Notes methods
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = NoteSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, 201)
    
    def list(self, request):
       notes = Note.objects.filter(user=request.user)
       return Response(self.serializer_class(instance=notes, many=True).data)
    
    def retrieve(self, request, pk=None):
        try:
            note = Note.objects.get(user=request.user, id=pk)
        except Note.DoesNotExist:
            return Response({"error": f"Object Note with pk {pk} does not exists"}, 404)
            
        return Response(self.serializer_class(instance=note).data)
    
    def update(self, request, pk=None):
        try:
            note = Note.objects.get(user=request.user, id=pk)
        except Note.DoesNotExist:
            return Response({"error": f"Object Note with pk {pk} does not exists"}, 404)
        serializer = self.serializer_class(note, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def destroy(self, request, pk=None):
        try:
            note = Note.objects.get(user=request.user, id=pk)
        except Note.DoesNotExist:
            return Response({"error": f"Object Note with pk {pk} does not exists"}, 404)
        note.delete()
        return Response()
