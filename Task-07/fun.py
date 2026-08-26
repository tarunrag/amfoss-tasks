import discord
from discord.ext import commands
import aiohttp
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='roast')
    async def roast(self, ctx, member: discord.Member):
        roasts = [
            "you're the reason the Going Merry sank.",
            "your bounty is so low, they don't even want you dead or alive.",
            "you couldn't even beat Buggy the Clown in a Davy Back Fight.",
            "you're weaker than a Celestial Dragon's resolve.",
            "even Spandam has more courage than you."
        ]
        await ctx.send(f"Ahoy {member.mention}, {random.choice(roasts)}")

    @commands.command(name='logpose')
    async def logpose(self, ctx):
        url = "https://api.api-onepiece.com/v2/characters/en"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        character = random.choice(data)
                        
                        name = character.get('name', 'Unknown Pirate')
                        bounty = character.get('bounty', 'Unknown')
                        fruit = character.get('fruit', {}).get('name', 'None') if character.get('fruit') else 'None'
                        
                        intel = f"🧭 **Log Pose Intel Retrieved!** 🧭\n\n"
                        intel += f"**Target Detected:** {name}\n"
                        intel += f"**Reported Bounty:** {bounty}\n"
                        intel += f"**Devil Fruit Power:** {fruit}"
                        
                        await ctx.send(intel)
                    else:
                        await self.fallback_logpose(ctx)
        except Exception:
            await self.fallback_logpose(ctx)

    async def fallback_logpose(self, ctx):
        intel = [
            "The One Piece is real!",
            "Beware, a Yonko's territory lies ahead.",
            "A legendary Devil Fruit has just spawned nearby."
        ]
        await ctx.send(f"🧭 The Log Pose points to a rumor...\n**{random.choice(intel)}**")

async def setup(bot):
    await bot.add_cog(Fun(bot))