from executor.task.interface import Task


class DummyTask(Task):
    message: str = None

    def __init__(self) -> None:
        super().__init__()

        self.message = None

    def execute(self):
        print(self.message)

    def deserialize(self, data):
        self.message = data["message"]
