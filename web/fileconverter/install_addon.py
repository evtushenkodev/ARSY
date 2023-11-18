import sys

import bpy

# Путь к аддону
addon_path = '/web/Spark-AR-toolkit.zip'

# Установка аддона
bpy.ops.preferences.addon_install(filepath=addon_path)

# Активация аддона
bpy.ops.preferences.addon_enable(module='Meta-Spark-Toolkit')

if "Meta-Spark-Toolkit" in bpy.context.preferences.addons:
    print("Meta Spark Toolkit активирован")
else:
    print("Meta Spark Toolkit не активирован")
    sys.exit(1)

# Сохранение настроек, чтобы аддон оставался активным
bpy.ops.wm.save_userpref()
