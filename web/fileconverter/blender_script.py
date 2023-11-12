import bpy
import sys
import os

# Получаем аргументы командной строки
input_file = sys.argv[-2]
output_file = sys.argv[-1]

# Определяем формат входного файла по расширению
input_ext = os.path.splitext(input_file)[1].lower()


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

# Экспортируем модель в формат GLB
try:
    bpy.ops.export_scene.gltf(filepath=output_file, export_format='GLB')
except Exception as e:
    print(f"Ошибка экспорта модели: {e}")
    sys.exit(1)  # Выход с ошибкой

# Закрыть Blender
bpy.ops.wm.quit_blender()
