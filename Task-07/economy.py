cat << 'EOF' > cogs/economy.py
import discord
from discord.ext import commands
import time
import random
import database

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='bounty')
    async def bounty(self, ctx):
        user = database.get_user(ctx.author.id, ctx.author.name)
        await ctx.send(f"🏴‍☠️ {ctx.author.name}, your current Berry bounty is **{user[2]} Berries**.")

    @commands.command(name='setsail')
    async def setsail(self, ctx):
        user = database.get_user(ctx.author.id, ctx.author.name)
        current_time = time.time()
        last_daily = user[3]
        cooldown = 86400
        
        if current_time - last_daily < cooldown:
            remaining = int((cooldown - (current_time - last_daily)) / 3600)
            await ctx.send(f"⚓ You're still recovering! Wait {remaining} hours before setting sail again.")
            return
            
        reward = 500
        database.update_balance(ctx.author.id, reward)
        database.update_cooldown(ctx.author.id, 'last_daily', current_time)
        await ctx.send(f"⛵ You raided a merchant ship at dawn and claimed **{reward} Berries**!")

    @commands.command(name='trade')
    async def trade(self, ctx, member: discord.Member, amount: int):
        if amount <= 0:
            await ctx.send("You must trade a positive amount of Berries!")
            return
            
        sender = database.get_user(ctx.author.id, ctx.author.name)
        if sender[2] < amount:
            await ctx.send("You don't have enough Berries for this trade.")
            return
            
        database.get_user(member.id, member.name)
        database.update_balance(ctx.author.id, -amount)
        database.update_balance(member.id, amount)
        await ctx.send(f"🤝 {ctx.author.name} transferred **{amount} Berries** to {member.name}.")

    @commands.command(name='worstgeneration')
    async def worstgeneration(self, ctx):
        top_users = database.get_top_users(5)
        if not top_users:
            await ctx.send("The Grand Line is currently empty.")
            return
            
        leaderboard = "**🏆 The Worst Generation (Top 5 Richest Pirates) 🏆**\n"
        for i, (username, balance) in enumerate(top_users, 1):
            leaderboard += f"{i}. **{username}** - {balance} Berries\n"
        await ctx.send(leaderboard)

    @commands.command(name='raid')
    async def raid(self, ctx, member: discord.Member):
        if ctx.author.id == member.id:
            await ctx.send("You can't raid your own crew!")
            return
            
        attacker = database.get_user(ctx.author.id, ctx.author.name)
        defender = database.get_user(member.id, member.name)
        
        current_time = time.time()
        last_rob = attacker[4]
        cooldown = 3600
        
        if current_time - last_rob < cooldown:
            remaining = int((cooldown - (current_time - last_rob)) / 60)
            await ctx.send(f"🛡️ Your crew needs rest. Wait {remaining} minutes before raiding again.")
            return
            
        if defender[2] < 50:
            await ctx.send("This pirate's stash is too small to be worth raiding.")
            return
            
        database.update_cooldown(ctx.author.id, 'last_rob', current_time)
        
        success = random.choice([True, False])
        if success:
            stolen = int(defender[2] * random.uniform(0.1, 0.3))
            database.update_balance(member.id, -stolen)
            database.update_balance(ctx.author.id, stolen)
            await ctx.send(f"⚔️ Success! You raided {member.name}'s crew and made off with **{stolen} Berries**!")
        else:
            penalty = 50
            if attacker[2] >= penalty:
                database.update_balance(ctx.author.id, -penalty)
                await ctx.send(f"🚨 Raid failed! You lost **{penalty} Berries** retreating.")
            else:
                await ctx.send(f"🚨 Raid failed! {member.name}'s crew fought back and you fled empty-handed.")

async def setup(bot):
    await bot.add_cog(Economy(bot))
EOF