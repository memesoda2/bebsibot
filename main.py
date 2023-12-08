#discord-base
import discord
from discord.ext import commands


import pytube



#ui
from discord import ui
from discord import app_commands

import asyncio
import json

with open("config.json") as f:
    try:
        data = json.load(f)
    except json.decoder.JSONDecodeError as e:
        print("Errore in config.json")
        print(e)
        exit(1)

prefix = "!"

auth_list = [598119406731657216, 673167077280055326]
is_auth = commands.check(lambda ctx: ctx.author.id in auth_list )

token_json = data["discord_token"]

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
intents.reactions = True




client = commands.Bot(command_prefix=prefix, intents=intents,case_insensitive=True)
client.remove_command('help')


@client.event
async def on_ready():
  slash_sync = await client.tree.sync()
  print(f"Synced app command (tree) {len(slash_sync)}.")
  print(f'Logged in as {client.user.name}')




@client.event
async def on_message(message):
	if "odio i froci" in message.content:
		await message.channel.send("Bravissimo! :smiley: ")
	elif "cyka blayd" in message.content:
		await message.channel.send("Python Blyad :flag_ru:")
	else:
		await client.process_commands(message)  # Add this line



@client.command()
async def help(ctx):
	command_list = []
	for command in client.commands:
		command_list.append(f"> Nome: {command.name}\n")
		message = "\n".join(command_list)
		await ctx.send(f'{message}')
	
#comandi

@client.event
async def on_member_join(member):
  if member.bot:
    role = discord.utils.get(member.guild.roles, id=1033424225584816250)
    await member.add_roles(role)
  if not member.bot:
    role = discord.utils.get(member.guild.roles, id=1034914089807400970)
    await member.add_roles(role)

@client.tree.command(name="reportbug", description="Segnala un bug") #slash command
async def report_bug(interaction: discord.Interaction):
  modal = BugModal
  await interaction.response.send_modal(BugModal())

class BugModal(ui.Modal, title='Report Bug'):
    bug_name = ui.TextInput(label='Bugged Command name',required=True,placeholder='Bugged command name...', max_length=50)
    answer = ui.TextInput(label='Description of the bug', style=discord.TextStyle.paragraph, max_length=300,placeholder='Bug description...')

    async def on_submit(self, interaction: discord.Interaction):
        channel = client.get_channel(1164195802047053894)
        embed = discord.Embed(title="Bug report ",color=discord.Color.green())
        embed.add_field(name="Bugged Command name", value=self.children[0].value)
        embed.add_field(name="Description of the bug", value=self.children[1].value)
        embed.add_field(name="User:", value=f"`{interaction.user}`")
        await channel.send(embed=embed)
        embed1 = discord.Embed(title="Bug report sent", color=discord.Color.green())
        await interaction.response.send_message(embeds=[embed1], ephemeral=True)



@client.command()
async def say(ctx, *, message):
    # Invia il messaggio dell'utente
    await ctx.send(message)


	    


@client.command()
async def hello(ctx):
  await ctx.send('Hello, world!')

@is_auth
@client.command()
async def update(ctx):
	embed = discord.Embed(title="Aggiornamento del bot...", color=0x2c2f33)
	embed.set_image(url="https://support.discord.com/hc/en-us/article_attachments/206303208/eJwVyksOwiAQANC7sJfp8Ke7Lt15A0MoUpJWGmZcGe-ubl_eW7zGLmaxMZ80A6yNch-rJO4j1SJr73Uv6Wwkcz8gMae8HeXJBOjC5NEap42dokUX_4SotI8GVfBaYYDldr3n3y_jomRtD_H5ArCeI9g.zGz1JSL-9DXgpkX_SkmMDM8NWGg.gif")
	embed.add_field(name = '**System info**', value = f':gear:', inline = False)
	embed.add_field(name = ':globe_with_meridians: **Ping**', value = f'{round(client.latency * 1000)}ms')
	await ctx.send(embed=embed, delete_after=4)
	await asyncio.sleep(5)
	exit(1)

@client.command() #sempre in ogni comando
async def ciao(ctx): #dopo def c'è il nome del comando
	await ctx.send("ciao")#invia il messagio nelle virgolette

@client.command()
async def bay(ctx):
	await ctx.send("Il soggetto baia è di classe keter in quanto mangia patatine tutto il giorno e si sega sui bambini maschi, questo soggetto è noto anche per la sua bravura a fare Plugin SL Sminchiati cosi tanto da farti esplodere il computer")









@client.command()
async def play(ctx, url: str):
	global filename
	if ctx.author.voice is None:
		await ctx.send("Non sei in un canale vocale")
	else:
		if ctx.guild.voice_client is not None and ctx.guild.voice_client.is_playing():
			await ctx.send(f"Aspetta che la canzone finisca, Usa il comando stop per far finire la canzone", color=discord.Colour.red())
		else:
			#else:
			try:
				if url.startswith("https://youtu.be/"):
					share_video_id = url.replace("https://youtu.be/", "")
					share_video_url = "youtube.com/watch?v=" + f"{share_video_id}"
					await ctx.send("Dowload in corso...")
					
					#find-video
					video = pytube.YouTube(share_video_url)
					
					#title-file
					number = random.randint(1, 100000)
					extension = "mp4"
					file_name = f"{number}.{extension}"
					#video.streams.get_highest_resolution().download(filename=file_name)
					
					#download
					video.streams.first().download(filename=file_name)
					
					#info
					video_length = video.length
					minutes, seconds = divmod(video_length, 60)
					
					artist = video.author
					
					#global
					
					filename = f"{file_name}"
	
					#video-info-embed
					await ctx.send(f"Ora in ascolto \n\n***Titolo: ***`{video.title}`\n\n`{artist}` \n\n `{minutes}:{seconds}`")
					#await msg.delete()
					#await msg.edit(embed=title_embed)
					await asyncio.sleep(0.5)
	
	
	
					# Play the video
					source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(f"{file_name}"))
					voice_channel = ctx.author.voice.channel
					voice = await voice_channel.connect()
					voice.play(source)
		
					#volume fix
					volume = 0.4
					voice_client = ctx.guild.voice_client
					voice_client.source.volume = volume
	
					# Wait for the video to finish playing
					while voice.is_playing():
						await asyncio.sleep(1)
	
					# Disconnect from the voice channel
					await voice.disconnect()
	
					# Delete the video file
					os.remove(f"{file_name}")
					await ctx.send("canzone finita")
					#pass
					#return
				else:
					#loading embed
					await ctx.send("dowload in corso...")
					
					#find-video
					video = pytube.YouTube(url)
					
					#title-file
					number = random.randint(1, 100000)
					extension = "mp4"
					file_name = f"{number}.{extension}"
					#video.streams.get_highest_resolution().download(filename=file_name)
					
					#download
					video.streams.first().download(filename=file_name)
					
					#info
					video_length = video.length
					minutes, seconds = divmod(video_length, 60)
					
					artist = video.author
					
					#global
					
					filename = f"{file_name}"
	
					#video-info-embed
					await ctx.send(f"Ora in ascolto* \n\n***Titolo: ***`{video.title}`\n\n`{artist}` \n\n `{minutes}:{seconds}`")
					#await msg.delete()
					#await msg.edit(embed=title_embed)
					await asyncio.sleep(0.5)
	
	
	
					# Play the video
					source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(f"{file_name}"))
					voice_channel = ctx.author.voice.channel
					voice = await voice_channel.connect()
					voice.play(source)
		
					#volume fix
					volume = 0.4
					voice_client = ctx.guild.voice_client
					voice_client.source.volume = volume
	
					# Wait for the video to finish playing
					while voice.is_playing():
						await asyncio.sleep(1)
	
					# Disconnect from the voice channel
					await voice.disconnect()
	
					# Delete the video file
					os.remove(f"{file_name}")
					await ctx.send("canzone finita")
					#pass
					#return
					#error
			except pytube.exceptions.PytubeError as e:
				if 'is age restricted' in str(e):
					await asyncio.sleep(1)
					#await ctx.send('the video is age-restricted.')
					error_embed_2 = discord.Embed(title="Errore", color=discord.Colour.red())
					await ctx.send(embed=error_embed_2)
					await asyncio.sleep(0.5)
				elif 'is streaming live' in str(e):
					await asyncio.sleep(1)
					error_embed_3 = discord.Embed(title="Errore", color=discord.Colour.red())
					await ctx.send(embed=error_embed_3)
					await asyncio.sleep(0.5)
				else:
					await asyncio.sleep(1)
					error_embed_4 = discord.Embed(title="***Errore sconosciuto.***", color=discord.Colour.red())
					await ctx.send(embed=error_embed_4)
					await asyncio.sleep(0.5)
			except Exception as e:
				if str(e) == "Already connected to a voice channel.":
					pass
				else:
					print(e)
					await ctx.send("errore sconosciuto")






@client.command()
async def stop(ctx):				
	global filename #global
	
	voice_client = ctx.guild.voice_client
	if voice_client and voice_client.is_connected():
		if voice_client.is_playing():
			try:
				await ctx.send("Ho terminato la canzone", ephemeral=True)
				voice_client.stop()
				await voice_client.disconnect()
				#await asyncio.sleep(2)
				os.remove(f"{filename}") #global
			except Exception as e:
				pass
		else:
			try:
				await ctx.send(':x: Il bot è stato disconesso')
				os.remove(f"{filename}") #global
				await voice_client.disconnect()
			except Exception as e:
				try:
					os.remove(f"{filename}")
				except Exception:
					pass
	else:
		await ctx.send("errore sconossiuto")


		

@client.command()
async def kick(ctx, member : discord.Member, *, reason = None):
	try:
		if member == None:
			await ctx.send("specifica un membro", delete_after=4)
		elif reason == None:
			if member == None:
				await ctx.send("specifica un membro", delete_after=4)
			else:
				await ctx.send("Ho espulso un membro", delete_after=4)
				await member.kick(reason=f"Sei stato bannato dal seguente server: {ctx.guild.name}")
		else:
			await ctx.send(f"Ho espulso un membro, motivo: {reason}", delete_after=4)
			await member.kick(reason=f"Sei stato bannato dal seguente server: {ctx.guild.name}, Motivo: '{reason}'")
	except Exception as e:
		if 'error code: 50013' in str(e):
			await ctx.send("Errore: Non ho il permesso di espellere questo utente", delete_after=4)
		else:
			await ctx.send(f"Errore: {e}", delete_after=4)


@client.command()
async def espelli(ctx, member: discord.Member,reason:str):
	try:
		if reason == None:
			await member.kick()
			await ctx.send(f"{member.mention} è stato espulso",delete_after=5)
		if not reason == None:
			await member.kick(reason=reason)
			await ctx.send(f"{member.mention} è stato espulso per {reason}",delete_after=5) 
		else:
			await ctx.send("errore",delete_after=3)
	except Exception as variabile_errore:
		await ctx.send(f"errore: \n{variabile_errore}",delete_after=3)
	

	

@client.event
async def on_command_error(ctx, error):
	if isinstance(error, discord.ext.commands.errors.CommandNotFound):
		await ctx.send("questo comando non esiste",delete_after=3)
	elif isinstance(error, discord.ext.commands.errors.MemberNotFound):
		await ctx.send("membro non trovato",delete_after=3)
	else:
		await ctx.send(f"errore sconosciuto \n{error}",delete_after=3)

client.run(token_json)
