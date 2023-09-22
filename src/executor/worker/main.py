import os
import sys
import socket
import getpass
import traceback

from datetime import datetime
import time


class Main:
    PROGRAM_NAME = "cookapps-bi-executor"

    def __init__(self, worker_params=None) -> None:
        if worker_params is None:
            worker_params = {}
        self.worker_params = worker_params

        self.set_env()

    def set_env(self):
        # set logger
        from scratchpad import Logger as scratchpadLogger
        from scratchpad import LoggerInterface
        from scratchpad import ConsoleLogger
        from scratchpad import CompositeLogger
        from scratchpad import SlackLogger

        logger_filter_pairs = []

        console_logger = ConsoleLogger({"appendNewLine": 1})
        logger_filter_pairs.append({"logger": console_logger, "filter": None})

        if socket.gethostname() in ["docker-desktop"]:
            slack_logger = SlackLogger(url="")
            logger_filter_pairs.append(
                {"logger": slack_logger, "filter": CompositeLogger.getSelectorLevel(["notice", "error", "critical"])}
            )

        compositLogger = CompositeLogger(
            config={
                "defaults": {
                    "program": self.PROGRAM_NAME,
                    "datetime": lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "hostname": socket.gethostname(),
                    "user": getpass.getuser(),
                },
                "loggerFilterPairs": logger_filter_pairs,
            }
        )

        scratchpadLogger.setLogger(compositLogger)
        self.logger: LoggerInterface = scratchpadLogger.getLogger()

        import redis

        self.redis = redis.Redis(host="localhost", port=6379, db=0)

    def run(self):
        try:
            argv = sys.argv
            _program = argv[0]

            if argv[1].split("=")[0].removeprefix("-").removeprefix("-") != "job":
                raise Exception("required job cli parameter")
            job = argv[1].split("=")[1]

            max_task_count = self.worker_params["max_task_count"] if "max_task_count" in self.worker_params else 100

            from executor.job.factory import JobQueueFactory

            # start_time = datetime.timestamp()
            current_task_count = 0

            while True:
                if current_task_count >= max_task_count:
                    break

                job_queue = JobQueueFactory.get_instance(job)
                task = job_queue.pop()
                if task is None:
                    self.logger.info({"type": "worker", "job": job, "message": "wait for task"})
                    time.sleep(1)
                    continue
                task.execute()
                self.logger.notice({"type": "worker", "job": job, "message": "finished", "task_data": task.serialize()})
            sys.exit(0)
        except Exception as _:
            self.logger.critical(
                {
                    "type": "exception",
                    "trace": traceback.format_exc(),
                }
            )
            sys.exit(-1)


if __name__ == "__main__":
    Main().run()
