import discord
from discord.ext import commands
from discord.ext.commands import Context

from utils import Color, ValidUserID

# Here we name the cog and create a new class for the cog.
class Moderation(commands.Cog, name = "moderation"):
	def __init__(self, bot) -> None:
		self.bot = bot

	@commands.hybrid_command(name = "ban", description = "Bans a user.")
	@commands.has_permissions(ban_members = True)
	async def ban(self, context: Context, member: discord.Member, *, reason = "No Reason Given") -> None:
		"""
		Bans a user
		
		:param context: The hybrid command context.
		"""
		try:
			await member.ban(reason = reason)
			embed = discord.Embed(
				description = "User has been banned successfully!",
				color = Color.FELIX
			)
			await member.send(f"You have been banned from **{context.guild.name}**! \n ```{reason}```")
		except:
			embed = discord.Embed(
				description = "There was an error trying to ban this user.",
				color = Color.RED
			)
		await context.send(embed = embed)
	
	@commands.hybrid_command(name = "unban", description = "Unbans a user.")
	@commands.has_permissions(ban_members = True)
	async def unban(self, context: Context, user_id: ValidUserID) -> None:
		"""
		Unbans a user
		
		:param context: The hybrid command context.
		"""
		try:
			await context.guild.unban(discord.Object(id = user_id))
			user = await self.bot.fetch_user(user_id)
			embed = discord.Embed(
				description = "User has been unbanned successfully!",
				color = Color.FELIX
			)
			await user.send(f"You have been unbanned from **{context.guild.name}**!")
		except:
			embed = discord.Embed(
				description = "There was an error trying to unban this user.",
				color = Color.RED
			)
		await context.send(embed = embed)
		
	@commands.hybrid_command(name = "kick", description = "Kicks a user.")
	@commands.has_permissions(kick_members = True)
	async def kick(self, context: Context, member: discord.Member, *, reason = "No reason given") -> None:
		"""
		Kicks a user
		
		:param context: The hybrid command context.
		"""
		try:
			await member.kick(reason = reason)
			embed = discord.Embed(
				description = "User has been kicked successfully!",
				color = Color.FELIX
			)
			await member.send(f"You have been kicked from **{context.guild.name}**! \n ```{reason}```")
		except:
			embed = discord.Embed(
				description = "There was an error trying to kick this user.",
				color = Color.RED
			)
		await context.send(embed = embed)
			
	@commands.hybrid_command(name = "setnick", description = "Changes your nickname.")
	async def setnick(self, context: Context, *, new_nickname: str) -> None:
		"""
		Changes your nickname.
		
		:param context: The hybrid command context.
		"""
		try:
			await context.author.edit(nick = new_nickname)
			embed = discord.Embed(
				description = f"Nickname has been changed to `{new_nickname}` successfully!",
				color = Color.FELIX
			)
		except Exception as e:
			embed = discord.Embed(
				description = f"There was an error trying to change nickname, with reason(s)\n``{e}``",
				color = Color.RED
			)
		await context.send(embed = embed)
		
# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(Moderation(bot))
