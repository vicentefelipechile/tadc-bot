# ==========================================================================
# ====================== Discord Bot (TADC) - Database =====================
# ==========================================================================

import sqlite3
from datetime import datetime

from discord import User
from sqlite3.dbapi2 import Connection
from sqlite3.dbapi2 import Cursor

from .user_enum import *


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
        self.user_info_db_init()
    
    
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
            user.name,
            user.discriminator,
            datetime.now(),
            user.created_at,
        ))
        
        self.MasterConnection.commit()
    
    
    def user_update(self, user: User) -> None:
        self.CursorConnection.execute(USER_UPDATE, (
            user.name,
            user.discriminator,
            user.name,
            user.id,
        ))
        
        self.MasterConnection.commit()
    
    
    # Usuario Info CRUD
    def user_info_db_init(self) -> None:
        self.CursorConnection.execute(USER_INFO_DATABASE)
        self.MasterConnection.commit()
        
    def user_info_add(self, user: User, info_name: str, info_string: str = None, info_number: int = None) -> None:
        self.CursorConnection.execute(USER_INFO_ADD, (
            user.id,
            info_name,
            info_string,
            info_number,
        ))
        
        self.MasterConnection.commit()
        
    def user_info_update(self, user: User, info_name: str, info_string: str = None, info_number: int = None) -> None:
        self.CursorConnection.execute(USER_INFO_UPDATE, (
            info_name,
            info_string,
            info_number,
            user.id,
        ))
        
        self.MasterConnection.commit()
    
    def user_info_get(self, user: User, info_name: str, ReturnString: bool = True, ReturnNumber: bool = True) -> tuple:
        if ReturnString:
            self.CursorConnection.execute(USER_INFO_GET_STRING, (
                user.id,
                info_name,
            ))
            
            return self.CursorConnection.fetchone()

        elif ReturnNumber:
            self.CursorConnection.execute(USER_INFO_GET_NUMBER, (
                user.id,
                info_name,
            ))
            
            return self.CursorConnection.fetchone()

        self.CursorConnection.execute(USER_INFO_GET, (
            user.id,
            info_name,
        ))
        
        return self.CursorConnection.fetchone()
        
    def user_info_exists(self, user: User, info_name: str) -> bool:
        self.CursorConnection.execute(USER_INFO_GET, (
            user.id,
            info_name,
        ))
        
        return self.CursorConnection.fetchone() is not None

    def ObtenerInfoUsuario(self, user: User, info: str = None) -> str:
        self.CursorConnection.execute(USER_INFO_GET, (user.id, info))
        return self.CursorConnection.fetchone()