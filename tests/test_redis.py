import unittest
import autoloader  # pylint: disable=unused-import
import redis


class TestRedis(unittest.TestCase):
    def test_hash_type(self):
        # given
        client = redis.Redis(host="localhost", port=6379, db=0)

        # when
        client.hset(name="test/hash", mapping={"111": "123"})

        # then
        a = client.hget("test/hash", "111")
        self.assertEqual(a.decode("utf-8"), "123")
        client.delete("test/hash")

    def test_list_type(self):
        # given
        client = redis.Redis(host="localhost", port=6379, db=0)
        keys = [1, 2]

        import json

        value1 = json.dumps({"task_name": "dummy1"})
        value2 = json.dumps({"task_name": "dummy2"})

        # when
        client.rpush(keys[0], value1)
        client.rpush(keys[1], value2)

        # then
        (key, value) = client.blpop(keys, 5)
        self.assertEqual(b"1", key)
        self.assertEqual({"task_name": "dummy1"}, json.loads(value))

        (key, value) = client.blpop(keys, 5)
        self.assertEqual(b"2", key)
        self.assertEqual({"task_name": "dummy2"}, json.loads(value))

        try:
            (key, value) = client.blpop("", 1)
            self.assertEqual(1, 2)
        except TypeError as _:
            self.assertEqual(1, 1)
