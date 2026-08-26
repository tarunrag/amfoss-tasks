import discord
from discord.ext import commands
import random
import database

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='duel')
    async def duel(self, ctx, choice: str):
        valid_choices = ['rock', 'paper', 'scissors']
        choice = choice.lower()
        
        if choice not in valid_choices:
            await ctx.send("Invalid move! Draw your weapon using `!duel rock`, `!duel paper`, or `!duel scissors`.")
            return
            
        user = database.get_user(ctx.author.id, ctx.author.name)
        wager = 50
        
        if user[2] < wager:
            await ctx.send(f"You need at least {wager} Berries to challenge the bot to a duel!")
            return
            
        bot_choice = random.choice(valid_choices)
        win_conditions = {'rock': 'scissors', 'paper': 'rock', 'scissors': 'paper'}
        
        result_msg = f"The bot strikes with **{bot_choice}**!\n"
        
        if choice == bot_choice:
            result_msg += "It's a clash! A draw! No Berries lost or won."
        elif win_conditions[choice] == bot_choice:
            database.update_balance(ctx.author.id, wager)
            result_msg += f"⚔️ You won the clash! You earned **{wager} Berries**."
        else:
            database.update_balance(ctx.author.id, -wager)
            result_msg += f"💀 You were bested! The bot took **{wager} Berries** from your stash."
            
        await ctx.send(result_msg)

async def setup(bot):
    await bot.add_cog(Games(bot))