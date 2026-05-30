import os
import asyncio
import discord
from discord.ext import commands
import yt_dlp

# مصفوفة إعدادات البوتات والرومات الصوتية
BOTS_CONFIG = [
    {"token": os.getenv("BOT_TOKEN_1"), "channel_id": 1429240481568526428},
    {"token": os.getenv("BOT_TOKEN_2"), "channel_id": 1429240479014195392},
    {"token": os.getenv("BOT_TOKEN_3"), "channel_id": 1429240484349345904},
    {"token": os.getenv("BOT_TOKEN_4"), "channel_id": 1509723397221777589},
    {"token": os.getenv("BOT_TOKEN_5"), "channel_id": 1509723462925549750}
]

# إعدادات الـ اليوتيوب والـ الصوت
YTDL_OPTIONS = {
    'format': 'bestaudio/best', 'noplaylist': True, 'nocheckcertificate': True,
    'ignoreerrors': False, 'logtostderr': False, 'quiet': True, 'no_warnings': True,
    'default_search': 'auto', 'source_address': '0.0.0.0'
}
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

ytdl = yt_dlp.YoutubeDL(YTDL_OPTIONS)

# 🎛️ كلاس الأزرار التفاعلية المنفصلة
class MusicControlView(discord.ui.View):
    def __init__(self, voice_client):
        super().__init__(timeout=None)
        self.vc = voice_client

    # زر التكرار / العشوائي
    @discord.ui.button(emoji=discord.PartialEmoji(name="emoji", id=1510388832275529918), style=discord.ButtonStyle.secondary)
    async def shuffle_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🔀 ميزة التكرار/العشوائي قيد التطوير!", ephemeral=True)

    # زر خفض الصوت
    @discord.ui.button(emoji=discord.PartialEmoji(name="emoji", id=1510388789393100881), style=discord.ButtonStyle.secondary)
    async def volume_down(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.vc and self.vc.source:
            old_vol = int((self.vc.source.volume if hasattr(self.vc.source, 'volume') else 1.0) * 100)
            new_vol_float = max((old_vol / 100) - 0.1, 0.0)
            if hasattr(self.vc.source, 'volume'):
                self.vc.source.volume = new_vol_float
            new_vol = int(new_vol_float * 100)
            await interaction.response.send_message(f"*Volume changed from* ``{old_vol}%`` *to* ``{new_vol}%`` .")
        else:
            await interaction.response.send_message("❌ لا يوجد صوت يعمل حالياً!", ephemeral=True)

    # زر التشغيل المؤقت / الاستئناف
    @discord.ui.button(emoji=discord.PartialEmoji(name="emoji", id=1510387778494398664), style=discord.ButtonStyle.secondary)
    async def play_pause(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.vc.is_playing():
            self.vc.pause()
            await interaction.response.send_message("⏸️ تم إيقاف التشغيل مؤقتاً.", ephemeral=True)
        elif self.vc.is_paused():
            self.vc.resume()
            await interaction.response.send_message("▶️ تم استئناف التشغيل.", ephemeral=True)
        else:
            await interaction.response.send_message("❌ لا يوجد شيء يعمل حالياً.", ephemeral=True)

    # زر زيادة الصوت
    @discord.ui.button(emoji=discord.PartialEmoji(name="emoji", id=1510388484748349531), style=discord.ButtonStyle.secondary)
    async def volume_up(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.vc and self.vc.source:
            old_vol = int((self.vc.source.volume if hasattr(self.vc.source, 'volume') else 1.0) * 100)
            new_vol_float = min((old_vol / 100) + 0.1, 2.0)
            if hasattr(self.vc.source, 'volume'):
                self.vc.source.volume = new_vol_float
            new_vol = int(new_vol_float * 100)
            await interaction.response.send_message(f"*Volume changed from* ``{old_vol}%`` *to* ``{new_vol}%`` .")
        else:
            await interaction.response.send_message("❌ لا يوجد صوت يعمل حالياً!", ephemeral=True)

    # زر التخطي / الإيقاف النهائي
    @discord.ui.button(emoji="▶️", style=discord.ButtonStyle.secondary)
    async def skip_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.vc.is_playing() or self.vc.is_paused():
            self.vc.stop()
            await interaction.response.send_message("Server queue is empty.")
        else:
            await interaction.response.send_message("❌ لا يوجد شيء يعمل لتخطيه.", ephemeral=True)

async def run_bot(config, bot_index):
    token = config["token"]
    channel_id = config["channel_id"]
    
    if not token:
        print(f"❌ خطأ: لم يتم العثور على BOT_TOKEN_{bot_index}")
        return

    intents = discord.Intents.default()
    intents.message_content = True
    
    bot = commands.Bot(command_prefix=tuple(), intents=intents, help_command=None)

    async def connect_to_voice():
        try:
            channel = bot.get_channel(channel_id)
            if channel and isinstance(channel, discord.VoiceChannel):
                if not bot.voice_clients:
                    await channel.connect(self_deaf=True)
                    print(f"🔊 {bot.user.name} دخل الروم المخصص له بنجاح.")
        except Exception as e:
            print(f"❌ خطأ اتصال صوتي للبوت {bot_index}: {e}")

    @bot.event
    async def on_ready():
        print(f"✅ {bot.user.name} (بوت {bot_index}) جاهز ويعمل!")
        await connect_to_voice()

    @bot.event
    async def on_voice_state_update(member, before, after):
        if member.id == bot.user.id and after.channel is None:
            await asyncio.sleep(5)
            await connect_to_voice()

    @bot.event
    async def on_message(message):
        if message.author.bot:
            return

        # التأكد أن الرسالة كتبت في شات الروم الصوتي المخصص لهذا البوت
        if message.channel.id != channel_id:
            return

        msg_content = message.content.strip()

        # 🎵 أمر التشغيل: p [اسم أو رابط]
        if msg_content.startswith("p ") or msg_content == "p":
            search = msg_content[2:].strip()
            if not search:
                return

            voice_client = message.guild.voice_client if message.guild else None
            if not voice_client:
                await connect_to_voice()
                voice_client = bot.voice_clients[0] if bot.voice_clients else None
                if not voice_client:
                    return

            try:
                loop = asyncio.get_event_loop()
                data = await loop.run_in_executor(None, lambda: ytdl.extract_info(search, download=False))
                
                if 'entries' in data:
                    video = data['entries'][0]
                else:
                    video = data

                url = video['url']
                title = video['title']
                
                if voice_client.is_playing():
                    voice_client.stop()

                source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS))
                voice_client.play(source)

                embed_msg = f"**Playing song : {title}**\n*by : {message.author.mention}*"
                view = MusicControlView(voice_client)
                await message.channel.send(content=embed_msg, view=view)

            except Exception as e:
                await message.channel.send(f"❌ حدث خطأ أثناء تشغيل المقطع: {e}")

        # 🔊 أمر تعديل الصوت: v [رقم من 1 إلى 100]
        elif msg_content.startswith("v "):
            voice_client = message.guild.voice_client if message.guild else None
            if not voice_client or not voice_client.source:
                return await message.channel.send("❌ لا يوجد صوت يعمل حالياً!")

            try:
                vol_num = int(msg_content[2:].strip())
                if 1 <= vol_num <= 100:
                    old_vol = int((voice_client.source.volume if hasattr(voice_client.source, 'volume') else 1.0) * 100)
                    new_vol_float = vol_num / 100.0
                    
                    if hasattr(voice_client.source, 'volume'):
                        voice_client.source.volume = new_vol_float
                        
                    await message.channel.send(f"*Volume changed from* ``{old_vol}%`` *to* ``{vol_num}%`` .")
                else:
                    await message.channel.send("❌ يرجى كتابة رقم بين 1 و 100.")
            except ValueError:
                await message.channel.send("❌ يرجى كتابة رقم صحيح بعد الحرف v.")

    async with bot:
        await bot.start(token)

async def main():
    tasks = []
    for index, config in enumerate(BOTS_CONFIG, start=1):
        tasks.append(run_bot(config, index))
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())