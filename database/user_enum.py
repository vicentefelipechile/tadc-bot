# ======================
# ==== Enumeraciones ===
# ======================

# Base de datos de usuarios
USER_DATABASE: str = """
    CREATE TABLE IF NOT EXISTS usuario (
        user_id             INTEGER PRIMARY KEY,
        user_nick           TEXT,
        user_discriminator  INTEGER DEFAULT 0,
        user_joined_at      DATETIME,
        user_created_at     DATETIME
    )
"""

USER_ADD: str = """
    INSERT INTO
        usuario (user_id, user_nick, user_discriminator, user_joined_at, user_created_at)
    VALUES
        (?, ?, ?, ?, ?)
"""

USER_UPDATE: str = """
    UPDATE
        usuario
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
        usuario
    WHERE
        user_id = ?
"""


# Base de datos de informacion de los usuarios, esta base de datos tiene una relacion de muchos a uno con la base de datos de usuarios
USER_INFO_DATABASE: str = """
    CREATE TABLE IF NOT EXISTS info_usuario (
        info_id             INTEGER PRIMARY KEY,
        info_user_id        INTEGER,
        info_name           TEXT,
        info_string         TEXT DEFAULT NULL,
        info_number         INTEGER DEFAULT NULL,
        FOREIGN KEY (info_user_id) REFERENCES usuario (user_id)
    )
"""

USER_INFO_ADD: str = """
    INSERT INTO
        info_usuario (info_user_id, info_name, info_string, info_number)
    VALUES
        (?, ?, ?, ?)
"""

USER_INFO_ADD_STRING: str = """
    INSERT INTO
        info_usuario (info_user_id, info_name, info_string)
    VALUES
        (?, ?, ?)
"""

USER_INFO_ADD_NUMBER: str = """
    INSERT INTO
        info_usuario (info_user_id, info_name, info_number)
    VALUES
        (?, ?, ?)
"""

USER_INFO_GET: str = """
    SELECT
        info_string,
        info_number
    FROM
        info_usuario
    WHERE
        info_user_id = ?
    AND
        info_name = ?
"""

USER_INFO_GET_STRING: str = """
    SELECT
        info_string
    FROM
        info_usuario
    WHERE
        info_user_id = ?
    AND
        info_name = ?
"""

USER_INFO_GET_NUMBER: str = """
    SELECT
        info_number
    FROM
        info_usuario
    WHERE
        info_user_id = ?
    AND
        info_name = ?
"""

USER_INFO_UPDATE: str = """
    UPDATE
        info_usuario
    SET
        info_name = ?,
        info_string = ?,
        info_number = ?
    WHERE
        info_id = ?
"""