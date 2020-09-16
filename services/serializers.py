from rest_framework import serializers

import services.models as models


class ItemSerializer(serializers.ModelSerializer):

    '''Serializer for Item model'''
    # owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = models.Item
        fields = '__all__'

    def create(self, validated_data):
        item = models.Item.objects.create(
            **validated_data,
        )
        return item

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
