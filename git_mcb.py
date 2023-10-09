import youtube_dl
import ffmpeg
import discord
from discord.ext import commands
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='&', intents=intents)
@bot.command()
async def play(ctx, *, query):
    if ctx.author.voice is None or ctx.author.voice.channel is None:
        await ctx.send("Вы должны находиться в голосовом канале, чтобы использовать эту команду.")
        return

    voice_channel = ctx.author.voice.channel
    voice_client = await voice_channel.connect()

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)
        url = info['formats'][0]['url']
        voice_client.play(discord.FFmpegPCMAudio(url))

    await ctx.send(f'Сейчас играет: {info["title"]}')

@bot.command()
async def leave(ctx):
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()
        await ctx.send("Я покидаю голосовой канал.")
bot.run("")