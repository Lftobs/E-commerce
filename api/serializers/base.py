from rest_framework import serializers

class ApiOverviewSerializer(serializers.Serializer):
    app_name = serializers.CharField()
    routes = serializers.DictField()
