import discord
from discord.ext import commands
from discord.commands import ApplicationContext, Option
from alttprbot.alttprgen import generator
from alttprbot.exceptions import SahasrahBotException
from alttprbot.alttprgen.spoilers import generate_spoiler_game
from alttprbot.alttprgen import smvaria
from alttprbot.alttprgen.randomizer import smdash

async def autocomplete_alttpr(interaction: discord.Interaction, value=str):
    return await generator.ALTTPRPreset().search(value)

async def autocomplete_alttprmystery(interaction: discord.Interaction, value=str):
    return await generator.ALTTPRMystery().search(value)

async def autocomplete_sm(interaction: discord.Interaction, value=str):
    return await generator.SMPreset().search(value)

async def autocomplete_smz3(interaction: discord.Interaction, value=str):
    return await generator.SMZ3Preset().search(value)

async def autocomplete_ctjets(interaction: discord.Interaction, value=str):
    return await generator.CTJetsPreset().search(value)

class Generator(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.slash_command()
    async def alttpr(
        self,
        ctx: ApplicationContext,
        preset: Option(str, description="The preset you want generate.", required=True, autocomplete=autocomplete_alttpr),
        race: Option(str, description="Is this a race? (default no)", choices=["yes", "no"], required=False, default="no"),
        hints: Option(str, description="Enable hints? (default no)", choices=["yes", "no"], required=False, default="no"),
        allow_quickswap: Option(str, description="Allow quickswap? (default yes)", choices=["yes", "no"], required=False, default="yes")
    ):
        """
        Generates an ALTTP Randomizer game on https://alttpr.com
        """
        await ctx.defer()
        seed = await generator.ALTTPRPreset(preset).generate(
            hints=hints == "yes",
            spoilers="off" if race == "yes" else "on",
            tournament=race == "yes",
            allow_quickswap=allow_quickswap == "yes"
        )
        if not seed:
            raise SahasrahBotException('Could not generate game.  Maybe preset does not exist?')
        embed = await seed.embed(emojis=self.bot.emojis)

        await ctx.respond(embed=embed)

    @commands.slash_command()
    async def alttprfestive(
        self,
        ctx: ApplicationContext,
        preset: Option(str, description="The preset you want generate.", required=True, autocomplete=autocomplete_alttpr),
        race: Option(str, description="Is this a race? (default no)", choices=["yes", "no"], required=False, default="no"),
        hints: Option(str, description="Enable hints? (default no)", choices=["yes", "no"], required=False, default="no"),
        allow_quickswap: Option(str, description="Allow quickswap? (default yes)", choices=["yes", "no"], required=False, default="yes")
    ):
        """
        Generates an Festive™ ALTTP Randomizer game on https://alttpr.com/festive
        """
        await ctx.defer()
        seed = await generator.ALTTPRPreset(preset).generate(
            hints=hints == "yes",
            spoilers="off" if race == "yes" else "on",
            tournament=race == "yes",
            allow_quickswap=allow_quickswap == "yes",
            endpoint_prefix="/festive"
        )
        if not seed:
            raise SahasrahBotException('Could not generate game.  Maybe preset does not exist?')
        embed = await seed.embed(emojis=self.bot.emojis)

        await ctx.respond(embed=embed)

    @commands.slash_command()
    async def alttprspoiler(
        self,
        ctx: ApplicationContext,
        preset: Option(str, description="The preset you want generate.", required=True, autocomplete=autocomplete_alttpr),
        festive: Option(str, description="Use the festive randomizer? (default no)", choices=["yes", "no"], required=False, default="no"),
    ):
        """
        Generates an ALTTP Randomizer Spoiler Race on https://alttpr.com
        """
        await ctx.defer()
        spoiler = await generate_spoiler_game(preset, festive=festive == "yes")

        embed = await spoiler.seed.embed(emojis=self.bot.emojis)
        embed.insert_field_at(0, name="Spoiler Log URL", value=spoiler.spoiler_log_url, inline=False)

        await ctx.respond(embed=embed)

    @commands.slash_command()
    async def alttprmystery(
        self,
        ctx: ApplicationContext,
        weightset: Option(str, description="The weightset you want to use.", required=True, autocomplete=autocomplete_alttprmystery),
        race: Option(str, description="Is this a race? (choosing no never masks settings) (default yes)", choices=["yes", "no"], required=False, default="yes"),
        mask_settings: Option(str, description="Mask settings? (default yes)", choices=["yes", "no"], required=False, default="yes"),
    ):
        """
        Generates an ALTTP Randomizer Mystery game on https://alttpr.com
        """
        await ctx.defer()
        mystery = await generator.ALTTPRMystery(weightset).generate(
            spoilers="mystery" if mask_settings else "off",
            tournament=race == "yes"
        )

        embed = await mystery.seed.embed(emojis=ctx.bot.emojis, name="Mystery Game")

        if mystery.custom_instructions:
            embed.insert_field_at(0, name="Custom Instructions", value=mystery.custom_instructions, inline=False)

        await ctx.respond(embed=embed)

    @commands.slash_command()
    async def sm(
        self,
        ctx: ApplicationContext,
        preset: Option(str, description="The preset you want generate.", required=True, autocomplete=autocomplete_sm),
        race: Option(str, description="Is this a race? (default no)", choices=["yes", "no"], required=False, default="no"),
    ):
        """
        Generates an Super Metroid Randomizer game on https://sm.samus.link
        """
        await ctx.defer()
        seed = await generator.SMPreset(preset).generate(tournament=race == "yes")
        embed = await seed.embed()
        await ctx.respond(embed=embed)

    @commands.slash_command()
    async def smz3(
        self,
        ctx: ApplicationContext,
        preset: Option(str, description="The preset you want generate.", required=True, autocomplete=autocomplete_smz3),
        race: Option(str, description="Is this a race? (default no)", choices=["yes", "no"], required=False, default="no")
    ):
        """
        Generates an ALTTP Super Metroid Combo Randomizer game on https://samus.link
        """
        await ctx.defer()
        seed = await generator.SMZ3Preset(preset).generate(tournament=race == "yes")
        embed = await seed.embed()
        await ctx.respond(embed=embed)

    @commands.slash_command()
    async def smvaria(
        self,
        ctx: ApplicationContext,
        skills: Option(str, description="The skills preset you want to use.", required=True),
        settings: Option(str, description="The settings preset you want generate.", required=True),
        race: Option(str, description="Is this a race? (default no)", choices=["yes", "no"], required=False, default="no")
    ):
        """
        Generates an Super Metroid Varia Randomizer game on https://varia.run
        """
        await ctx.defer()
        seed = await smvaria.generate_preset(
            settings=settings,
            skills=skills,
            race=race == "yes"
        )
        await ctx.respond(embed=seed.embed())

    @commands.slash_command()
    async def smdash(
        self,
        ctx: ApplicationContext,
        mode: Option(str, description="The mode you want to generate.", choices=['mm', 'full', 'sgl20', 'vanilla'], required=True),
        race: Option(str, description="Is this a race? (default no)", choices=["yes", "no"], required=False, default="no")
    ):
        """
        Generates an Super Metroid Varia Randomizer game on https://varia.run
        """
        await ctx.defer()
        url = await smdash.create_smdash(mode=mode, encrypt=race == "yes")
        await ctx.respond(url)

    @ commands.slash_command()
    async def ctjets(self, ctx: ApplicationContext, preset: Option(str, description="The preset you want to generate.", required=True, autocomplete=autocomplete_ctjets)):
        """
        Generates a Chrono Trigger: Jets of Time randomizer game on http://ctjot.com
        """
        await ctx.defer()
        seed_uri = await generator.CTJetsPreset(preset).generate()
        await ctx.respond(seed_uri)


def setup(bot):
    bot.add_cog(Generator(bot))