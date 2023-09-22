from executor.task.interface import Task


class CombinedTask(Task):
    tasks: list[Task] = []

    def __init__(self) -> None:
        super().__init__()

    def execute(self):
        for task in self.tasks:
            task.execute()

    def deserialize(self, data):
        for task_data in data["tasks"]:
            self.tasks.append(Task.instantiate(task_data))
