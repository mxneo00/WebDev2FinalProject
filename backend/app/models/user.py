# Python
import uuid
from datetime import datetime
from enum import Enum
# Libraries
from passlib.hash import bcrypt
from tortoise import models, fields

class User(models.Model):
    user_id = fields.UuidField(pk=True, unique=True)
    username = fields.CharField(max_length=50, unique=True)
    email = fields.CharField(max_length=255, unique=True)
    digest = fields.CharField(max_length=128)
    fname = fields.CharField(max_length=50)
    lname = fields.CharField(max_length=50)
    activated_at = fields.DatetimeField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    def set_password(self, raw_password: str):
        """Hashes and stores the given password."""
        self.digest = bcrypt.hash(raw_password)

    def verify_password(self, raw_password: str) -> bool:
        """Verifies a password against the stored digest."""
        return bcrypt.verify(raw_password, self.digest)

    def __str__(self):
        return self.username