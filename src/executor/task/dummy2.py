from executor.task.interface import Task


class Dummy2Task(Task):
    message: str = None

    def __init__(self) -> None:
        super().__init__()

        self.message = None

    def execute(self):
        print(self.message)

        from executor.task.dummy3 import Dummy3Task

        # do something
        # next_task = Dummy3Task()
        # next_task.message = "안녕하세요"

        # from executor.job.factory import JobQueueFactory

        # job_queue = JobQueueFactory.get_instance(JobQueueFactory.JOB_TASK_DUMMY_WORKER_QUEUE)
        # job_queue.push(next_task)

    def deserialize(self, data):
        self.message = data["message"]
