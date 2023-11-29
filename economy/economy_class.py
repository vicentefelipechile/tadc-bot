# ==========================================================================
# ======================== Bot de mierda de Economia =======================
# ==========================================================================

import sqlite3
from datetime import datetime

from discord import User
from discord import Embed
from sqlite3.dbapi2 import Connection
from sqlite3.dbapi2 import Cursor
from sqlite3.dbapi2 import Error

from .economy_enum import *


PROFILE_EMBED: Embed = Embed(
    # description = "Aqui se muestra la informacion de tu perfil",
    color = 0x2d85c8,
    timestamp = datetime.now(),
    )



# ======================
# ====== Principal =====
# ======================

class ModuloEconomia:
    MasterConnection:   Connection = None
    CursorConnection:   Cursor = None
    
    def __init__(self) -> None:
        self.MasterConnection = sqlite3.connect("tadc_database.db")
        self.CursorConnection = self.MasterConnection.cursor()
        
        self.economy_db_init()
    
    
    def economy_db_init(self) -> None:
        self.CursorConnection.execute(ECONOMY_DATABASE)
        self.MasterConnection.commit()
    
    
    # CRUD Usuario
    def UserExists(self, user: User) -> bool:
        self.CursorConnection.execute(ECONOMY_USER_GET, (user.id,))
        
        return self.CursorConnection.fetchone() is not None
    
    def CreateUser(self, user: User) -> None:
        if self.UserExists(user):       return
        
        self.CursorConnection.execute(ECONOMY_CREATE_USER, (user.id,))
        self.MasterConnection.commit()
    
    
    # CRUD Dinero
    def GetMoney(self, user: User) -> int:
        if not self.UserExists(user):   return 0
        self.CursorConnection.execute(ECONOMY_USER_MONEY_GET, (user.id,))
        
        return self.CursorConnection.fetchone()[0]

    def SetMoney(self, user: User, money: int = 0) -> bool:
        if not self.UserExists(user):   return False
        
        try:
            self.CursorConnection.execute(ECONOMY_USER_MONEY_SET, (money, user.id))
            self.MasterConnection.commit()
        except Error:
            return False
        
        return True
    
    def AddMoney(self, user: User, money: int = 0) -> bool:
        if not self.UserExists(user):   return False
        
        try:
            self.CursorConnection.execute(ECONOMY_USER_MONEY_ADD, (money, user.id))
            self.MasterConnection.commit()
        except Error:
            return False
        
        return True
    
    def AddMoneyMultiplier(self, user: User, money: int = 0) -> bool:
        if not self.UserExists(user):   return False
        
        try:
            self.CursorConnection.execute(ECONOMY_USER_MONEY_ADD_MULTIPLIER, (money, user.id))
            self.MasterConnection.commit()
        except Error:
            return False
        
        return True

    # Perfil
    def GetProfile(self, user: User) -> Embed:
        if not self.UserExists(user):   return None
        
        try:
            self.CursorConnection.execute(ECONOMY_USER_GET, (user.id,))
            user_profile: tuple = self.CursorConnection.fetchone()
        except Error:
            return None
        
        PROFILE: Embed = PROFILE_EMBED.copy()
        PROFILE.title = f"Perfil de {user.name}"
        PROFILE.set_thumbnail(url=user.avatar)
        PROFILE.add_field(name="Digital Coins", value=f"{user_profile[3]}", inline=False)
        PROFILE.add_field(name="Banco Digital", value=f"{user_profile[4]}", inline=False)
        
        return PROFILE