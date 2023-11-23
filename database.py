# ==========================================================================
# ====================== Discord Bot (TADC) - Database =====================
# ==========================================================================

import sqlite3
from datetime import datetime

from discord import User
from sqlite3.dbapi2 import Connection
from sqlite3.dbapi2 import Cursor


# ======================
# ==== Enumeraciones ===
# ======================


USER_DATABASE: str = """
    CREATE TABLE IF NOT EXISTS users (
        user_id             INTEGER PRIMARY KEY,
        user_nick           TEXT,
        user_discriminator  INTEGER DEFAULT 0,
        user_joined_at      DATETIME,
        user_created_at     DATETIME
    )
"""

USER_ADD: str = """
    INSERT INTO
        users (user_id, user_nick, user_discriminator, user_joined_at, user_created_at)
    VALUES
        (?, ?, ?, ?, ?)
"""

USER_UPDATE: str = """
    UPDATE
        users
    SET
        user_name = ?,
        user_discriminator = ?,
        user_nick = ?
    WHERE
        user_id = ?
"""

USER_EXISTS: str = """
    SELECT
        user_id
    FROM
        users
    WHERE
        user_id = ?
"""


# ======================
# ====== Principal =====
# ======================


class DiscordDatabase:
    MasterConnection:   Connection = None
    CursorConnection:   Cursor = None
    
    def __init__(self) -> None:
        self.MasterConnection = sqlite3.connect("tadc_database.db")
        self.CursorConnection = self.MasterConnection.cursor()
        
        self.user_db_init()
    
    
    # Usuario CRUD
    def user_db_init(self) -> None:
        self.CursorConnection.execute(USER_DATABASE)
        self.MasterConnection.commit()
    
    def user_exists(self, user: User) -> bool:
        self.CursorConnection.execute(USER_EXISTS, (user.id,))
        
        return self.CursorConnection.fetchone() is not None
    
    def user_add(self, user: User) -> None:
        # Si el usuario ya existe entonces no hacer nada
        if self.user_exists(user):  return
        
        self.CursorConnection.execute(USER_ADD, (
            user.id,
            user.nick,
            user.discriminator,
            datetime.now(),
            user.created_at,
        ))
        
        self.MasterConnection.commit()
    
    
    def user_update(self, user: User) -> None:
        self.CursorConnection.execute(USER_UPDATE, (
            user.name,
            user.discriminator,
            user.nick,
            user.id,
        ))
        
        self.MasterConnection.commit()