# Python
import uuid
from datetime import datetime
from enum import Enum
# Libraries
from passlib.hash import bcrypt
from tortoise import models, fields

class Game(models.Model):
    game_id = fields.IntField(pk=True, unique=True)
    gameTitle = fields.CharField(max_length=50, unique=True)
    category = fields.CharField(max_length=50)
    platform = fields.CharField(max_length=50)
    status = fields.CharField(max_length=50, default="Wishlist")
    rating = fields.IntField(null=True)
    owner = fields.ForeignKeyField("models.user", related_name = "games")
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return f"<Game {self.gameTitle}>"