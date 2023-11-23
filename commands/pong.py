from discord.ext.commands import Bot

async def pong(bot) -> str:
    return f"Pong! {round(bot.latency * 1000)}ms"