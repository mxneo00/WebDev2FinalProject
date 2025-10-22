# Python
from datetime import datetime
# Libraries
from passlib.hash import bcrypt, argon2
from tortoise import models, fields

class User(models.Model):
    user_id = fields.IntField(pk=True, unique=True)
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
        # password_bytes = raw_password.encode("utf-8")[:72]
        # self.digest = bcrypt.hash(password_bytes)
        self.digest = argon2.hash(raw_password)

    def verify_password(self, raw_password: str) -> bool:
        """Verifies a password against the stored digest."""
        #return bcrypt.verify(raw_password, self.digest)
        return argon2.verify(raw_password, self.digest)

    def __str__(self):
        return f"<User {self.username}>"
    
    class Meta:
        table = "users"
        app = "models"