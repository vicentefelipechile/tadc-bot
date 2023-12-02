# Creacion de la base de datos de economia del servidor

ECONOMY_DATABASE: str = """
CREATE TABLE IF NOT EXISTS economia (
    eco_id              INTEGER PRIMARY KEY AUTOINCREMENT,
    eco_user_id         INTEGER NOT NULL,
    eco_created_at      DATETIME NOT NULL DEFAULT (datetime('now', 'localtime')),
    eco_money           INTEGER NOT NULL DEFAULT 0,
    eco_bank            INTEGER NOT NULL DEFAULT 0,
    eco_multiplier      INTEGER NOT NULL DEFAULT 1,
    eco_secured         BOOLEAN NOT NULL DEFAULT 0,
    eco_daily_last      DATETIME NOT NULL DEFAULT (datetime('now', 'localtime')),
    eco_daily_streak    INTEGER NOT NULL DEFAULT 0,
    eco_work_last       DATETIME NOT NULL DEFAULT (datetime('now', 'localtime')),
    eco_work_streak     INTEGER NOT NULL DEFAULT 0,

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


# Acciones de trabajo
ECONOMY_USER_WORK_ACTION: str = """
UPDATE
    economia
SET
    eco_work_last = datetime('now', 'localtime'),
    eco_work_streak = eco_work_streak + 1
WHERE
    eco_user_id = ?
"""

ECONOMY_USER_WORK_LASTTIME: str = """
SELECT
    strftime('%s', 'now', 'localtime') - strftime('%s', eco_work_last)
FROM
    economia
WHERE
    eco_user_id = ?
"""


# Sistema de inventario (Relacion muchos a muchos)
ECONOMY_ITEM_DB: str = """
CREATE TABLE IF NOT EXISTS item (
    item_id             INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name           TEXT NOT NULL,
    item_description    TEXT NOT NULL,
    item_price          INTEGER NOT NULL DEFAULT 0,
    item_image          TEXT NOT NULL DEFAULT 'https://i.imgur.com/0l7Y8p7.png',
    item_sellable       BOOLEAN NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS inventario (
    inv_id              INTEGER PRIMARY KEY AUTOINCREMENT,
    inv_user_id         INTEGER NOT NULL,
    inv_item_id         INTEGER NOT NULL,

    FOREIGN KEY (inv_user_id) REFERENCES usuario (user_id),
    FOREIGN KEY (inv_item_id) REFERENCES item (item_id),
);
"""

ECONOMY_USER_ITEM_GET: str = """
SELECT
    *
FROM
    inventario
WHERE
    inv_user_id = ?
ORDER BY
    inv_item_id
"""

ECONOMY_USER_ITEM_ALREADY: str = """
SELECT
    (SELECT count(*) FROM inventario WHERE inv_user_id = ? AND inv_item_id = ?) > 0
"""

ECONOMY_USER_ITEM_AFFORD: str = """
SELECT
    (SELECT eco_money FROM economia WHERE eco_user_id = ?) >= (SELECT item_price FROM item WHERE item_id = ?)
"""

ECONOMY_USER_ITEM_BUY: str = """
INSERT INTO
    inventario (inv_user_id, inv_item_id)
VALUES
    (?, ?);
    
UPDATE
    economia
SET
    eco_money = eco_money - (SELECT item_price FROM item WHERE item_id = ?)
WHERE
    eco_user_id = ?;
"""

ECONOMY_USER_ITEM_SELL: str = """
DELETE FROM
    inventario
WHERE
    inv_user_id = ?
    AND inv_item_id = ?;

UPDATE
    economia
SET
    eco_money = eco_money + (SELECT round(item_price * 0.5) FROM item WHERE item_id = ?)
WHERE
    eco_user_id = ?;
"""

ECONOMY_USER_ITEM_SELL_ALL: str = """
DELETE FROM
    inventario
WHERE
    inv_user_id = ?;

UPDATE
    economia
SET
    eco_money = eco_money + (
        SELECT
            sum(round(item_price * 0.5))
        FROM
            item
        WHERE
            item_id IN (
                SELECT
                    inv_item_id
                FROM
                    inventario
                WHERE
                    inv_user_id = ?
            )
            AND item_sellable = 1
    )
WHERE
    eco_user_id = ?;
"""

ECONOMY_USER_ITEM_DELETE: str = """
DELETE FROM
    inventario
WHERE
    inv_user_id = ?
    AND inv_item_id = ?;
"""

ECONOMY_USER_ITEM_GIFT: str = """
INSERT INTO
    inventario (inv_user_id, inv_item_id)
VALUES
    (?, ?);

DELETE FROM
    inventario
WHERE
    inv_user_id = ?
    AND inv_item_id = ?;
"""