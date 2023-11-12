from django.conf import settings
import os
import subprocess

from django.utils.dateparse import parse_date
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView

from .models import ConvertedModel
from .serializers import ConvertedModelSerializer


class ConvertedModelListCreateView(ListCreateAPIView):
    serializer_class = ConvertedModelSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        queryset = ConvertedModel.objects.filter(user=self.request.user)
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date:
            start_date = parse_date(start_date)
            queryset = queryset.filter(timestamp__gte=start_date)

        if end_date:
            end_date = parse_date(end_date)
            queryset = queryset.filter(timestamp__lte=end_date)

        return queryset

    def perform_create(self, serializer):
        original_file = self.request.FILES.get('original_file')

        # Check if original_file is present in the request
        if not original_file:
            return Response("No file provided", status=status.HTTP_400_BAD_REQUEST)

        # Save original file in original_files/ directory
        original_files_dir = os.path.join('original_files')
        os.makedirs(original_files_dir, exist_ok=True)
        original_file_path = os.path.join(original_files_dir, original_file.name)

        with open(original_file_path, 'wb') as destination:
            for chunk in original_file.chunks():
                destination.write(chunk)

        try:
            # Create the directory for converted files if it doesn't exist
            converted_files_dir = os.path.join('converted_files')
            os.makedirs(converted_files_dir, exist_ok=True)

            # Define paths for conversion
            output_file = os.path.join(converted_files_dir, os.path.splitext(original_file.name)[0] + '.glb')

            blender_executable = "blender"
            blender_script = os.path.join('fileconverter', 'blender_script.py')

            # Convert the model using Blender
            try:
                subprocess.run([blender_executable, "--background", "--python", blender_script, original_file_path,
                                output_file], check=True)
            except subprocess.CalledProcessError:
                print(f"...")

            # Save the converted model in the database

            if not os.path.exists(output_file):
                raise Exception(f"Converted file not found: {output_file}")

            try:
                converted_model = ConvertedModel.objects.create(
                    user=self.request.user,
                    original_file=original_file_path,
                    converted_file=output_file,
                    converted_filename=os.path.basename(output_file)
                )
                serializer.instance = converted_model
            except Exception as e:
                print(f"Ошибка при создании модели: {e}")

        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ConvertedModelDetailView(RetrieveDestroyAPIView):
    queryset = ConvertedModel.objects.all()
    serializer_class = ConvertedModelSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
