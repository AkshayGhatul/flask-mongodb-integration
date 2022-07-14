import os
import importlib
from .models import Model, __MODEL_DICT__

class MigrationUtils:
    @staticmethod
    def migrate(version):
        for file in os.listdir(os.path.dirname(__file__)):
            if file == f'migration_version_{version}.py':
                module_name = file[:file.find('.py')]
                module = importlib.import_module('core.migrations.' + module_name) 
        for name, class_def in __MODEL_DICT__.items():
            instance = class_def()
            for operation in instance.operations:
                print(operation)