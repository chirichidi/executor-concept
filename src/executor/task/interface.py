from abc import ABC

import importlib

# from typing import Self  # 3.11


class Task(ABC):
    def execute(self):
        pass

    def deserialize(self, data):
        pass

    @staticmethod
    def instantiate(data: dict):
        if "package" not in data:
            raise Exception("package not exist in task")
        package = data["package"]
        class_name = data["type"]
        params = data["params"]

        module = importlib.import_module(f"{package}")

        task: Task = getattr(module, class_name)()
        task.deserialize(params)

        return task

    def serialize(self):
        # ex) {"package": "executor.task.dummy", "type": "DummyTask", "params": {"message": "hello"}}
        task_data = {"package": self.__class__.__module__, "type": self.__class__.__qualname__, "params": {}}

        keys = self.__class__.__annotations__.keys()
        for key in keys:
            value = getattr(self, key)
            if isinstance(value, list) and isinstance(value[0], Task):
                value = list(map(lambda x: x.serialize(), value))
                task_data["params"][key] = value
            else:
                task_data["params"][key] = value

        return task_data
