import unittest
import autoloader  # pylint: disable=unused-import


class TestExecutor(unittest.TestCase):
    def test_job_queue(self):
        # given
        from executor.job.queue import MemoryJobQueue

        job_queue = MemoryJobQueue()

        # when
        from executor.task.dummy import DummyTask

        task = DummyTask()
        job_queue.push(task)

        # then
        popped = job_queue.pop()
        self.assertEqual({}, popped)

    def test_combined_task(self):
        # given
        from executor.task.combined import CombinedTask

        from executor.task.dummy import DummyTask
        from executor.task.dummy2 import Dummy2Task

        sub_task1 = DummyTask()
        sub_task1.message = "hello"
        sub_task2 = Dummy2Task()
        sub_task2.message = "world"

        # when
        combined_task = CombinedTask()
        combined_task.tasks = [sub_task1, sub_task2]

        from executor.job.factory import JobQueueFactory

        job_queue = JobQueueFactory.get_instance(JobQueueFactory.JOB_TASK_DUMMY_WORKER_QUEUE)
        job_queue.push(combined_task)

        # then
        popped_task: CombinedTask = job_queue.pop()
        popped_task.execute()
        self.assertEqual("hello", popped_task.tasks[0].message)
        self.assertEqual("world", popped_task.tasks[1].message)

    def test_job_queue_factory(self):
        # given
        from executor.job.factory import JobQueueFactory

        # when
        job_queue = JobQueueFactory.get_instance(JobQueueFactory.JOB_TASK_DUMMY_WORKER_QUEUE)

        # then
        from executor.job.queue import RedisJobQueue

        self.assertTrue(isinstance(job_queue, RedisJobQueue))

    def test_decode_task(self):
        # given
        from executor.task.dummy import DummyTask

        dummy_task = DummyTask()
        dummy_task.message = "hello world"

        from executor.job.factory import JobQueueFactory

        job_queue = JobQueueFactory.get_instance(JobQueueFactory.JOB_TASK_DUMMY_WORKER_QUEUE)
        job_queue.push(dummy_task)

        # when

        task: DummyTask = job_queue.pop()

        # then
        task.execute()
        self.assertEqual(task.message, "hello world")
