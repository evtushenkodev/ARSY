from rest_framework import serializers
from .models import ConvertedModel


class ConvertedModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConvertedModel
        fields = ('id', 'user', 'original_file', 'converted_file', 'converted_filename', 'timestamp')
        read_only_fields = ('id', 'user', 'converted_file', 'converted_filename', 'timestamp')

    def validate_original_file(self, value):
        ext = value.name.split('.')[-1].lower()
        if ext not in ['fbx', 'obj', 'gltf', 'glb']:
            raise serializers.ValidationError(
                "Unsupported file format. Supported formats are .fbx, .obj, .gltf, or .glb")
        return value
