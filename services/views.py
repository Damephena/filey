from rest_framework import viewsets, status, generics, permissions
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

import services.serializers as serializers
import services.models as models
from utils.permissions import IsFileOwnerOrAccessible, IsFileOwnerOrReadOnly


class ItemViewset(viewsets.ModelViewSet):

    '''
    list:
        Get only files belonging to particular `user`.
        Or get all files in database as an admin user type.
    create:
        Upload a file.
    read:
        Retrieve a file.
    update:
        Update an existing file.
    partial_update:
        Make patch update to an existing file.
    delete:
        Delete a file.
    '''
    serializer_class = serializers.ItemSerializer
    parser_classes = [MultiPartParser]
    permission_classes = [IsFileOwnerOrReadOnly]
    filterset_fields = ['name', 'created_at']
    search_fields = ['$name', '$created_at']
    ordering_fields = ['name', 'created_at']

    def get_queryset(self):

        '''Filter objects belonging to `user`. Allow all if `user.is_admin` is True'''
        if self.request.user.is_staff:
            return models.Item.objects.all()
        return models.Item.objects.filter(owner=self.request.user)

    def get_parsers(self):

        '''To enable file uploads via Swagger API endpoint'''
        if getattr(self, 'swagger_fake_view', False):
            return [MultiPartParser]
        return super().get_parsers()


class DownloadView(generics.RetrieveAPIView):

    '''Returns URL to downloadable file if `is_accessible` or `owner`'''
    serializer_class = serializers.ItemSerializer
    queryset = models.Item.objects.all()
    lookup_field = 'pk'
    permission_classes = [IsFileOwnerOrAccessible, permissions.AllowAny]

    def retrieve(self, request, pk):
        try:
            query = models.Item.objects.get(id=pk, is_accessible=True)
        except models.Item.DoesNotExist:
            return Response('Invalid file ID or denied file access.')

        file = query.file.url
        return Response(data=file, status=status.HTTP_200_OK)
