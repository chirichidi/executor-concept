from executor.task.interface import Task

from typing import Optional

import boto3
import os


class MoveToS3(Task):
    aws_profile: Optional[str] = None
    aws_bucket: Optional[str] = None
    src_path: Optional[str] = None
    dest_path: Optional[str] = None

    def execute(self):
        session = boto3.Session(profile_name=self.aws_profile)
        s3 = session.resource("s3")
        s3.Bucket(self.aws_bucket).upload_file(Filename=self.src_path, Key=self.dest_path)

        os.remove(self.src_path)

    def deserialize(self, data):
        self.aws_profile = data["aws_profile"]
        self.aws_bucket = data["aws_bucket"]

        self.src_path = data["src_path"]
        self.dest_path = data["dest_path"]
