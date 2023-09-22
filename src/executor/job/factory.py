import json

from executor.config import Loader
from executor.job.queue import JobQueue
from collections import defaultdict
from typing import DefaultDict


class JobQueueFactory:
    JOB_TASK_DUMMY_WORKER_QUEUE = "JOB_TASK_DUMMY_WORKER_QUEUE"
    JOB_TASK_EXPORT_WORKER_QUEUE = "JOB_TASK_EXPORT_WORKER_QUEUE"
    JOB_TASK_S3_UPLOAD_WORKER_QUEUE = "JOB_TASK_S3_UPLOAD_WORKER_QUEUE"

    queues: DefaultDict[str, JobQueue] = defaultdict()

    @staticmethod
    def get_instance(queue_id: str):
        match queue_id:
            case JobQueueFactory.JOB_TASK_DUMMY_WORKER_QUEUE:
                from executor.job.queue import RedisJobQueue

                JobQueueFactory.queues[queue_id] = RedisJobQueue(
                    {
                        "name": JobQueueFactory.JOB_TASK_DUMMY_WORKER_QUEUE,
                        "host": "localhost",
                        "port": "6379",
                        "keys": [JobQueueFactory.JOB_TASK_DUMMY_WORKER_QUEUE],
                    }
                )
            case JobQueueFactory.JOB_TASK_EXPORT_WORKER_QUEUE:
                config = Loader.load("env", "redis")
                startup_nodes = list(
                    map(
                        (lambda x: {"host": x.split(":")[0], "port": x.split(":")[1]}),
                        json.loads(config["startup_nodes"]),
                    )
                )

                from executor.job.queue import RedisJobQueue

                JobQueueFactory.queues[queue_id] = RedisJobQueue(
                    {
                        "name": JobQueueFactory.JOB_TASK_EXPORT_WORKER_QUEUE,
                        "host": "localhost",
                        "port": "6379",
                        "keys": [JobQueueFactory.JOB_TASK_EXPORT_WORKER_QUEUE],
                    }
                )
            case JobQueueFactory.JOB_TASK_S3_UPLOAD_WORKER_QUEUE:
                config = Loader.load("env", "redis")
                startup_nodes = list(
                    map(
                        (lambda x: {"host": x.split(":")[0], "port": x.split(":")[1]}),
                        json.loads(config["startup_nodes"]),
                    )
                )

                from executor.job.queue import RedisJobQueue

                JobQueueFactory.queues[queue_id] = RedisJobQueue(
                    {
                        "name": JobQueueFactory.JOB_TASK_S3_UPLOAD_WORKER_QUEUE,
                        "host": "localhost",
                        "port": "6379",
                        "keys": [JobQueueFactory.JOB_TASK_S3_UPLOAD_WORKER_QUEUE],
                    }
                )
            case _:
                raise Exception("not exist job in executor")

        return JobQueueFactory.queues[queue_id]
