from abc import ABC

import json

from executor.task.interface import Task


class JobQueue(ABC):
    def push(self, task: Task, priority=0):
        pass

    def pop(self) -> Task:
        pass


class RedisJobQueue(JobQueue):
    def __init__(self, config: dict = None) -> None:
        super().__init__()

        if config is None:
            config = {}

        if ("host" not in config or "port" not in config) and ("cluster" not in config):
            raise Exception("not exist redis host info")

        if "cluster" in config and "startup_nodes" in config["cluster"]:
            password = None
            if "password" in config["cluster"]:
                password = config["cluster"]["password"]
            from rediscluster import RedisCluster

            self.client = RedisCluster(
                startup_nodes=config["cluster"]["startup_nodes"],
                decode_responses=True,
                password=password,
                max_connections_per_node=100,
                skip_full_coverage_check=True,
            )
        else:
            from redis import Redis

            self.client = Redis(host=config["host"])

        self.config: dict = config

    def push(self, task: Task, priority=0):
        task_data = task.serialize()
        key_count = len(self.config["keys"])
        key = self.config["keys"][key_count - priority - 1]
        value = json.dumps(task_data)
        self.client.rpush(key, value)

    def pop(self) -> Task:
        keys: list[str] = self.config["keys"]
        timeout = 3 if "timeout" not in self.config else self.config["timeout"]

        try:
            (_, task_data) = self.client.blpop(keys, timeout)
            task_data = json.loads(task_data)
            decoded = Task.instantiate(task_data)
        except TypeError as _:
            decoded = None
        except Exception as _:
            # TODO unexpected exception. logger
            decoded = None

        return decoded


class MemoryJobQueue(JobQueue):
    queue = []

    def push(self, task_data: dict, priority=0):
        self.queue.append({})

    def pop(self):
        return self.queue.pop()
