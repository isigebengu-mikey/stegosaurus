from sys import stdout
import discord
from discord.ext import commands, tasks
import logging

logging.basicConfig(
    level=logging.INFO,
    format="S | [%(asctime)s] %(message)s",
    handlers=[logging.StreamHandler(stdout)],
)
logger = logging.getLogger()

intents = discord.Intents.default()


class Stegosaurus(commands.Bot):
    def __init__(self, command_prefix, help_command=None, description=None, **options):
        super().__init__(
            command_prefix,
            help_command=help_command,
            description=description,
            **options,
        )
        self.member_count = 0
        self.refresh_member_count.start()
        self.color = 0x5000FB

    def load_extension(self, name):
        logger.info(f"Loaded {name}")
        return super().load_extension(name)

    @tasks.loop(minutes=5, reconnect=True)
    async def refresh_member_count(self):
        self.member_count = 0
        for i in self.guilds:
            self.member_count += i.member_count


client = Stegosaurus(
    command_prefix=commands.when_mentioned_or("stego ", "stegosaurus ", "s"),
    intents=intents,
    case_insensitive=True,
)


@client.event
async def on_ready():
    logger.info(f"signed in as {client.user.name}")
    logger.info(f"id: {client.user.id}")
    logger.info(
        f"can see {len(client.guilds)} servers and {client.member_count} server members."
    )


@client.event
async def on_command(ctx):
    logger.info(f"{ctx.author.id} used command {ctx.command.name.lower()}.")


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    logger.error(f"error {error} occurred in {ctx.command.name.lower()}")
    raise error


@client.command()
@commands.is_owner()
async def reload(ctx: commands.Context, cog):
    try:
        client.unload_extension(f"cogs.{cog}")
    except commands.ExtensionNotLoaded:
        pass
    except Exception as e:
        return await ctx.send(e)
    try:
        client.load_extension(f"cogs.{cog}")
    except commands.ExtensionFailed as e:
        await ctx.send(e)
    return await ctx.send(f"Loaded `{cog}` successfully.")


client.load_extension("cogs.zero")
client.load_extension("cogs.crypt")
client.load_extension("jishaku")
client.run("token")
