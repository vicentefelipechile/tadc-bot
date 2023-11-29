# Creacion de la base de datos de economia del servidor

ECONOMY_DATABASE: str = """
CREATE TABLE IF NOT EXISTS economia (
    eco_id              INTEGER PRIMARY KEY AUTOINCREMENT,
    eco_user_id         INTEGER NOT NULL, -- Llave foranea a la tabla de usuarios (usuario -> user_id)
    eco_created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    eco_money           INTEGER NOT NULL DEFAULT 0,
    eco_bank            INTEGER NOT NULL DEFAULT 0,
    eco_multiplier      INTEGER NOT NULL DEFAULT 1,
    eco_secured         BOOLEAN NOT NULL DEFAULT 0,
    eco_daily_last      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    eco_daily_streak    INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (eco_user_id) REFERENCES usuario (user_id),

    CONSTRAINT eco_money_not_negative CHECK (eco_money >= 0),
    CONSTRAINT eco_bank_not_negative CHECK (eco_bank >= 0),
    CONSTRAINT eco_multiplier_not_negative CHECK (eco_multiplier >= 0)
);
"""

ECONOMY_CREATE_USER: str = """
INSERT INTO
    economia (eco_user_id)
VALUES
    (?)
"""

ECONOMY_USER_GET: str = """
SELECT
    *
FROM
    economia
WHERE
    eco_user_id = ?
"""



# Acciones con el dinero
ECONOMY_USER_MONEY_GET: str = """
SELECT
    eco_money
FROM
    economia
WHERE
    eco_user_id = ?
"""

ECONOMY_USER_MONEY_SET: str = """
UPDATE
    economia
SET
    eco_money = ?
WHERE
    eco_user_id = ?
"""

ECONOMY_USER_MONEY_ADD: str = """
UPDATE
    economia
SET
    eco_money = eco_money + ?
WHERE
    eco_user_id = ?
"""

ECONOMY_USER_MONEY_ADD_MULTIPLIER: str = """
UPDATE
    economia
SET
    eco_money = (
        SELECT
            eco_multiplier * ?
        FROM
            economia
        WHERE
            eco_user_id = ?
    )
WHERE
    eco_user_id = ?
"""

ECONOMY_USER_MONEY_TO_BANK: str = """
UPDATE
    economia
SET
    eco_money = eco_money - ?,
    eco_bank = eco_bank + ?
WHERE
    eco_user_id = ?
"""
    
ECONOMY_USER_MONEY_FROM_BANK: str = """
UPDATE
    economia
SET
    eco_money = eco_money + ?,
    eco_bank = eco_bank - ?
WHERE
    eco_user_id = ?
"""



# Acciones en el banco
ECONOMY_USER_BANK_GET: str = """
SELECT
    eco_bank
FROM
    economia
WHERE
    eco_user_id = ?
"""

ECONOMY_USER_BANK_SET: str = """
UPDATE
    economia
SET
    eco_bank = ?
WHERE
    eco_user_id = ?
"""

ECONOMY_USER_BANK_ADD: str = """
UPDATE
    economia
SET
    eco_bank = eco_bank + ?
WHERE
    eco_user_id = ?
"""



# Acciones entre usuarios
ECONOMY_USER_MONEY_TRANSFER: str = """
UPDATE
    economia
SET
    eco_money = (
        SELECT
            eco_money - ?
        FROM
            economia
        WHERE
            eco_user_id = ?
    )
WHERE
    eco_user_id = ?;

UPDATE
    economia
SET
    eco_money = (
        SELECT
            eco_money + ?
        FROM
            economia
        WHERE
            eco_user_id = ?
    )
WHERE
    eco_user_id = ?;
"""

ECONOMY_USER_BANK_TRANSFER: str = """
UPDATE
    economia
SET
    eco_bank = (
        SELECT
            eco_bank - ?
        FROM
            economia
        WHERE
            eco_user_id = ?
    )
WHERE
    eco_user_id = ?;

UPDATE
    economia
SET
    eco_bank = (
        SELECT
            eco_bank + ?
        FROM
            economia
        WHERE
            eco_user_id = ?
    )
WHERE
    eco_user_id = ?;
"""