import os
import subprocess

from django.conf import settings
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

        if not original_file:
            return Response("No file provided", status=status.HTTP_400_BAD_REQUEST)

        # Создание экземпляра модели напрямую сохранит файл в нужном месте
        converted_model = ConvertedModel.objects.create(
            user=self.request.user,
            original_file=original_file
        )

        # Получение абсолютного пути к файлу
        original_file_path = converted_model.original_file.path

        try:
            # Конвертация файла
            converted_files_dir = os.path.join(settings.MEDIA_ROOT, 'converted_files')
            os.makedirs(converted_files_dir, exist_ok=True)
            output_file_name = os.path.splitext(original_file.name)[0] + '.glb'
            output_file_path = os.path.join(converted_files_dir, output_file_name)

            blender_executable = "blender"
            blender_script = os.path.join('fileconverter', 'blender_script.py')

            try:
                subprocess.run([blender_executable, "--background", "--python", blender_script, original_file_path,
                                output_file_path], check=True)
            except subprocess.CalledProcessError:
                print(f"...")

            if not os.path.exists(output_file_path):
                raise Exception(f"Converted file not found: {output_file_path}")

            # Обновление экземпляра модели с конвертированным файлом
            converted_model.converted_file = 'converted_files/' + output_file_name
            converted_model.converted_filename = output_file_name
            converted_model.save()

        except Exception as e:
            converted_model.delete()  # Удаляем запись при неудачной конвертации
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer.instance = converted_model


class ConvertedModelDetailView(RetrieveDestroyAPIView):
    queryset = ConvertedModel.objects.all()
    serializer_class = ConvertedModelSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
