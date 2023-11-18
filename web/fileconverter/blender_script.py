import os
import sys

import bpy

# Получаем аргументы командной строки
input_file = sys.argv[-2]
output_file = sys.argv[-1]

# Определяем формат входного файла по расширению
input_ext = os.path.splitext(input_file)[1].lower()

# Удаление стандартного куба (если он существует)
if "Cube" in bpy.data.objects:
    bpy.data.objects['Cube'].select_set(True)
    bpy.ops.object.delete()


# Функция для импорта файла в зависимости от его формата
def import_model(filepath, extension):
    if extension == '.fbx':
        bpy.ops.import_scene.fbx(filepath=filepath)
    elif extension == '.obj':
        bpy.ops.import_scene.obj(filepath=filepath)
    elif extension in ['.gltf', '.glb']:
        bpy.ops.import_scene.gltf(filepath=filepath)
    else:
        raise Exception("Unsupported file format")


# Пытаемся импортировать модель
try:
    import_model(input_file, input_ext)
except Exception as e:
    print(f"Ошибка импорта модели: {e}")
    sys.exit(1)  # Выход с ошибкой


# Функция для оптимизации меша
def optimize_mesh(mesh):
    # Активируем объект для оптимизации
    bpy.context.view_layer.objects.active = mesh
    mesh.select_set(True)

    # Применяем оптимизацию
    bpy.context.object.sparkar_optimization.InvertedReducePercentage = 50
    bpy.ops.object.modifier_apply(modifier="SparkDecimateModifier")
    bpy.ops.object.spark_decimation()


# Оптимизируем каждый меш в сцене
try:
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            optimize_mesh(obj)
except Exception as e:
    print(f"Ошибка оптимизации модели: {e}")
    sys.exit(1)  # Выход с ошибкой

# Экспортируем модель в формат GLB
try:
    bpy.ops.export_scene.gltf(filepath=output_file, export_format='GLB')
except Exception as e:
    print(f"Ошибка экспорта модели: {e}")
    sys.exit(1)  # Выход с ошибкой

# Закрыть Blender
bpy.ops.wm.quit_blender()
