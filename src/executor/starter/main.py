#! /usr/bin/env python
import os
import sys
import getpass
import socket
import traceback
import json

from datetime import datetime

from executor.job.factory import JobQueueFactory


def set_error_handler(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    message = {
        "type": "unhandled exception",
        "trace": traceback.format_exception(exc_type, exc_value, exc_traceback),
    }


sys.excepthook = set_error_handler


class Main:
    PROGRAM_NAME = "executor"

    def __init__(self, program_params=None) -> None:
        if program_params is None:
            program_params = {}
        self.program_params = program_params

        self.set_env()

    def parse_config(self, file, env_section):
        from executor.config.Loader import load

        return load(file, env_section)

    def set_env(self):
        # set path
        src_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
        sys.path.append(src_path)

        dir_list = os.listdir(src_path)
        for item in dir_list:
            path = src_path + "/" + item
            if not os.path.isdir(path):
                continue
            if item.startswith("."):
                continue
            if path in sys.path:
                continue
            sys.path.append(item)

        # set logger
        from scratchpad import Logger as scratchpadLogger
        from scratchpad import LoggerInterface
        from scratchpad import ConsoleLogger
        from scratchpad import CompositeLogger
        from scratchpad import SlackLogger
        from scratchpad import LineLogger
        from scratchpad import ScribeLogger

        console_logger = ConsoleLogger({"appendNewLine": 1})
        notification_filter = CompositeLogger.getSelectorLevel(["notice", "error", "critical"])
        logger_filter_pairs = []

        logger_filter_pairs.append({"logger": console_logger, "filter": None})
        if socket.gethostname() in ["docker-desktop"]:
            slack_logger = SlackLogger(
                url="url"
            )
            line_logger = LineLogger(token="token")
            logger_filter_pairs.append({"logger": slack_logger, "filter": notification_filter})
            logger_filter_pairs.append({"logger": line_logger, "filter": notification_filter})

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(("127.0.0.1", 1463))
        if result == 0:
            scribe_logger = ScribeLogger({"category": self.PROGRAM_NAME})
            logger_filter_pairs.append({"logger": scribe_logger, "filter": None})

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

        self.logger.notice({"type": "test"})
        
        import redis

        self.redis = redis.Redis(host="127.0.0.1", port=6379, db=0)

      

    def run(self):
        try:
            argv = sys.argv
            _program = argv[0]

            for parameter in argv[1:]:
                key = parameter.split("=")[0].removeprefix("-").removeprefix("-")
                value = parameter.split("=")[1]

                match key:
                    case "job":
                        match value:
                            case "JOB_TASK_DUMMY_WORKER_QUEUE":
                                from executor.task.dummy import DummyTask

                                # 임시 태스크 생성
                                task = DummyTask()
                                task.message = "hello world"

                                job_queue = JobQueueFactory.get_instance(value)
                                job_queue.push(task)
                                break
                            case "JOB_TASK_EXPORT_WORKER_QUEUE":
                                break
                            case "JOB_TASK_ALARM_WOREKR_QUEUE":
                                pass
                            case _:
                                raise Exception("not matched job task")
                    case _:
                        raise Exception("not matched cli key")

        except Exception as _:
            self.logger.critical(
                {
                    "type": "exception",
                    "trace": traceback.format_exc(),
                }
            )
            sys.exit()


if __name__ == "__main__":
    Main().run()
