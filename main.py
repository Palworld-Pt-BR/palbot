import nextcord
from nextcord.ext import commands
import settings
import os
import importlib.util

intents = nextcord.Intents.all()
bot = commands.Bot(
    command_prefix=settings.bot_prefix, intents=intents, help_command=None
)

@bot.event
async def on_ready():
    ascii_art = r"""
__________        .__ ___.           __   
\______   \_____  |  |\_ |__   _____/  |_ 
 |     ___/\__  \ |  | | __ \ /  _ \   __\
 |    |     / __ \|  |_| \_\ (  <_> )  |  
 |____|    (____  /____/___  /\____/|__|  
                \/         \/             
    """
    print(ascii_art)
    print(f"{bot.user} está pronto! Criado por koz")
    activity = nextcord.Activity(
        type=nextcord.ActivityType.playing, name=settings.bot_activity
    )
    await bot.change_presence(activity=activity)

# Error Handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Este comando não existe.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Você não tem as permissões necessárias para usar este comando.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Está faltando um parâmetro obrigatório.")
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send("Este comando está em recarga. Por favor, tente novamente mais tarde.")
    else:
        await ctx.send(f"Ocorreu um erro: {error}")

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")

def has_setup_function(module_name):
    module_spec = importlib.util.find_spec(module_name)
    if module_spec is None:
        return False
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return hasattr(module, "setup")

for entry in os.listdir("cogs"):
    if entry.endswith(".py"):
        module_name = f"cogs.{entry[:-3]}"
        if has_setup_function(module_name):
            bot.load_extension(module_name)
    elif os.path.isdir(f"cogs/{entry}"):
        for filename in os.listdir(f"cogs/{entry}"):
            if filename.endswith(".py"):
                module_name = f"cogs.{entry}.{filename[:-3]}"
                if has_setup_function(module_name):
                    bot.load_extension(module_name)

if __name__ == "__main__":
    bot.run(settings.bot_token)