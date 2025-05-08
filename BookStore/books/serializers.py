from rest_framework import serializers

class BookSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)

    