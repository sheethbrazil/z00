import discord
from discord.ext import commands
from discord import app_commands
import datetime
import os
import asyncio  # تم استيرادها لتعويض السليب القديم بشكل صحيح

# ==========================================
# ⚙️ الإعدادات الأساسية (الآيديات والروابط)
# ==========================================
TOKEN = os.getenv('TOKEN')

GUILD_ID = 808381236913242142
WELCOME_ROOM_ID = 808764019644301332
BOOST_ROOM_ID = 1337462631191150663  # 💥 تم إضافة آيدي روم البوست الجديد هنا
AUTO_ROLE_ID = 808382007012360213
COUNTING_ROOM_ID = 1374375983351861309

# رومات اللوحات (Panels)
APP_PANEL_ROOM = 1337804280836391016
TICKET_PANEL_ROOM = 808382081843462145
TICKET_CATEGORY_ID = 808382030051934238
ADMIN_PANEL_ROOM = 1503055195058475099

# رومات استقبال طلبات التقديم
APP_ROOMS = {
    "Staff Team": 1474171233586380881,
    "Lady": 1501924691173048360,
    "Developer Team": 1503053396679069757,
    "Events Team": 1503053543215464558
}

# رتب الإشعارات
ROLES_DICT = {
    "Another Notfications": 1207045205006745652,
    "Ajr Notfications": 1207044847236554832,
    "Event notification": 1362599311443230780,
    "Live Notfications": 1207044785001599046,
    "Updates Notfications": 1207044658048274543
}

# الروابط والصور
LOGO_URL = "https://i.postimg.cc/4xKM6832/tsmym-bdwn-nwan-1.png"
APP_BANNER = "https://i.postimg.cc/pdKskrFL/unwatermarked-Gemini-Generated-Image-wkmrxdwkmrxdwkmr.png"
TICKET_BANNER = "https://i.postimg.cc/8zZkyRqK/Gemini-Generated-Image-au70bfau70bfau70-(1).png"
MAIN_PANEL_IMG = "https://i.postimg.cc/8e98118b/image_ead976.png"

# متغيرات مساعدة
current_count = 0
app_counter = 1

# ==========================================
# 🤖 إعدادات البوت الأساسية
# ==========================================
class iMLKqBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        self.add_view(ApplicationView())
        self.add_view(TicketPanelView())
        self.add_view(MainPanelView())
        self.add_view(AdminPanelView())
        await self.tree.sync()

bot = iMLKqBot()

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user.name}')
    print(f'🚀 iMLKq System is Online and Ready!')

# ==========================================
# 🛡️ أوامر الإدارة للرومات وروم العد
# ==========================================
@bot.event
async def on_message(message):
    global current_count
    if message.author.bot: return

    # نظام العد
    if message.channel.id == COUNTING_ROOM_ID:
        try:
            num = int(message.content)
            if num == current_count + 1:
                current_count += 1
                await message.add_reaction("✅")
            else:
                await message.delete()
                await message.channel.send(f"{message.author.mention} لقد سكبت العدد **{current_count + 1}** ❌", delete_after=5)
        except ValueError:
            pass 

    # أوامر التحكم بالرومات
    if message.content in ["#قفل", "#فتح", "#اخفاء", "#اظهار"]:
        if not message.author.guild_permissions.manage_channels:
            return await message.reply("❌ لا تملك صلاحية إدارة الرومات.")
        
        role = message.guild.default_role
        if message.content == "#قفل":
            await message.channel.set_permissions(role, send_messages=False)
            await message.reply("🔒 تم قفل الروم.")
        elif message.content == "#فتح":
            await message.channel.set_permissions(role, send_messages=True)
            await message.reply("🔓 تم فتح الروم.")
        elif message.content == "#اخفاء":
            await message.channel.set_permissions(role, view_channel=False)
            await message.reply("👻 تم إخفاء الروم.")
        elif message.content == "#اظهار":
            await message.channel.set_permissions(role, view_channel=True)
            await message.reply("👁️ تم إظهار الروم.")

    await bot.process_commands(message)

# ==========================================
# 👋 نظام الترحيب ونظام البوست (Boost)
# ==========================================
@bot.event
async def on_member_join(member):
    if member.guild.id != GUILD_ID: return
    channel = bot.get_channel(WELCOME_ROOM_ID)
    role = member.guild.get_role(AUTO_ROLE_ID)
    if role: 
        try: await member.add_roles(role)
        except: pass

    embed = discord.Embed(
        title="Welcome to iMLKq Community",
        description=f"مرحباً بك {member.mention} في سيرفر **أبو ملك**\n\n"
                    f"نتمنى لك وقتاً ممتعاً معنا!\n"
                    f"• أنت العضو رقم: **{len(member.guild.members)}**\n\n"
                    f"🔗 **روابط هامة:**\n"
                    f"<#808764166802374716> | القوانين\n"
                    f"<#808382090525540383> | الشات العام",
        color=discord.Color.from_str("#39baf7"),
        timestamp=datetime.datetime.now()
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_footer(text="iMLKq System", icon_url=LOGO_URL)
    
    if channel: await channel.send(content=member.mention, embed=embed)

@bot.event
async def on_member_update(before, after):
    if before.premium_since is None and after.premium_since is not None:
        channel = bot.get_channel(BOOST_ROOM_ID)  # 🛠️ تم التعديل ليجلب روم البوست بدلاً من الترحيب
        if channel:
            embed = discord.Embed(
                title="🎉 شكر خاص لداعم السيرفر! 🎉",
                description=f"شكراً لك {after.mention} على دعمك لسيرفر **أبو ملك** بـ بوست! 🚀\nدعمك يعني لنا الكثير ويساعدنا نتطور أكثر ونقدم الأفضل.",
                color=discord.Color.from_str("#ff73fa"),
                timestamp=datetime.datetime.now()
            )
            embed.set_thumbnail(url=after.display_avatar.url)
            embed.set_image(url="https://i.postimg.cc/1zcYzXb8/nitro-boost.gif")
            embed.set_footer(text="iMLKq Boosters", icon_url=LOGO_URL)
            await channel.send(content=f"{after.mention} 💖", embed=embed)

# ==========================================
# 🌟 البانل الرئيسي (Main Panel)
# ==========================================
class MainPanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Server Rules", style=discord.ButtonStyle.blurple, emoji="📜", custom_id="main_rules")
    async def btn_rules(self, interaction: discord.Interaction, button: discord.ui.Button):
        rules_text = (
            "**أولاً: ضوابط السلوك العام والأخلاقيات**\nالاحترام المتبادل، منع التمييز والكراهية، ويحظر الخوض في النقاشات الجدلية السياسية والدينية.\n\n"
            "**ثانياً: ضوابط المحتوى والمنشورات**\nيُحظر المحتوى غير اللائق، ويمنع الترويج العشوائي (Spam & Advertising) ونشر البرمجيات الخبيثة.\n\n"
            "**ثالثاً: ضوابط القنوات**\nاستخدام القنوات للغرض المخصص، منع الإزعاج المتعمد والإشارة العشوائية للإدارة، ومنع استخدام الـ Soundboards بشكل مزعج.\n\n"
            "**رابعاً: الخصوصية والأمان الشخصي**\nحماية البيانات الشخصية ومنع تسريبها، ومنع تسجيل المحادثات دون إذن.\n\n"
            "**خامساً: الإدارة وإنفاذ اللوائح**\nالقرارات الإدارية نهائية وملزمة، ويُحظر استخدام حسابات بديلة للتهرب من العقوبات."
        )
        embed = discord.Embed(title="iMLKq Server Rules", description=rules_text, color=discord.Color.from_str("#39baf7"))
        embed.set_thumbnail(url=LOGO_URL)
        await interaction.response.send_message(embed=embed, view=RulesSubView(), ephemeral=True)

    @discord.ui.button(label="Social Media", style=discord.ButtonStyle.green, emoji="🌐", custom_id="main_social")
    async def btn_social(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="وسائل التواصل الاجتماعي",
            description="أهلاً وسهلاً بك. يمكنك الوصول إلى جميع الحسابات الرسمية لأبو ملك عن طريق الأزرار بالأسفل.",
            color=discord.Color.dark_theme()
        )
        embed.set_thumbnail(url=LOGO_URL)
        await interaction.response.send_message(embed=embed, view=SocialMediaView(), ephemeral=True)

    @discord.ui.button(label="Roles", style=discord.ButtonStyle.grey, emoji="⭐", custom_id="main_roles")
    async def btn_roles(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="Notification Roles",
            description="الجميع مهتم بأشياء مختلفة للتأكد من أنك فقط تأخذ رتب ذات صلة بك، ويمكنك اختيار الإشعارات التي ترغب في الاشتراك فيها. ما عليك سوى الضغط على الزر في الأسفل.",
            color=discord.Color.dark_theme()
        )
        embed.set_thumbnail(url=LOGO_URL)
        await interaction.response.send_message(embed=embed, view=RolesView(), ephemeral=True)

    @discord.ui.button(label="Apply", style=discord.ButtonStyle.grey, emoji="📝", custom_id="main_apply")
    async def btn_apply(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"📝 للتقديم على فِرق السيرفر، يرجى التوجه إلى روم التتقديمات: <#{APP_PANEL_ROOM}>", ephemeral=True)

class RulesSubView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(label="Discord Terms of Service", url="https://discord.com/terms", row=1))
        self.add_item(discord.ui.Button(label="Discord Community Guidelines", url="https://discord.com/guidelines", row=1))

    @discord.ui.button(label="Public Chat Rules", style=discord.ButtonStyle.blurple, emoji="💬", custom_id="rules_public", row=0)
    async def btn_public(self, interaction: discord.Interaction, button: discord.ui.Button):
        txt = (
            "📜 **القوانين للشات العام:**\n\n"
            "• **الحدود:** 350 حرفاً كحد أقصى، 15 إيموجي، 10 منشن.\n"
            "• **اللغة:** العربية والإنجليزية فقط، وتُمنع اللغات غير المفهومة.\n"
            "• **المواضيع:** يُمنع الخوض في المواضيع العاطفية، الدينية، والعرقية.\n"
            "• **السلوك:** يُحظر تشويه مظهر الشات أو استخدام الألفاظ المهينة.\n"
            "• **الإدارة:** يُمنع عمل منشن للإدارة العليا أو انتحال صفتهم."
        )
        await interaction.response.send_message(txt, ephemeral=True)

    @discord.ui.button(label="Kick Chat Rules", style=discord.ButtonStyle.blurple, emoji="🟣", custom_id="rules_kick", row=0)
    async def btn_kick(self, interaction: discord.Interaction, button: discord.ui.Button):
        txt = (
            "🟣 **قوانين شات منصة Kick:**\n\n"
            "• **مواعيد البث:** يُمنع نشر مواعيد البث أو التوقعات.\n"
            "• **سياق الحديث:** يقتصر الحديث على محتوى البث أو أبو ملك فقط.\n"
            "• **آداب الإدارة:** يُمنع الجدال مع الإدارة أو التشكيك في كلامهم.\n"
            "• **المظهر:** يُمنع استخدام الستيكرات أو تشويه الشات بالهبد والسطاوة.\n"
            "• **الاحترام:** يُحظر الإساءة لأي ستريمر أو صانع محتوى آخر."
        )
        await interaction.response.send_message(txt, ephemeral=True)

class SocialMediaView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(label="Kick", emoji="<:kick:1503044549239636030>", url="https://kick.com/imlkq"))
        self.add_item(discord.ui.Button(label="Instagram", emoji="<:insta:1503044441177587896>", url="https://www.instagram.com/imlkq1/"))
        self.add_item(discord.ui.Button(label="X", emoji="<:xlogo:1503044767863279626>", url="https://x.com/imlkq1"))
        self.add_item(discord.ui.Button(label="Snapchat", emoji="<:snap:1503045897871954110>", url="https://www.snapchat.com/@iimlkq"))
        self.add_item(discord.ui.Button(label="YouTube", emoji="<:yt:1503044363733958789>", url="https://www.youtube.com/@iMLKq1"))
        self.add_item(discord.ui.Button(label="WhatsApp", emoji="<:wa:1503044934079352952>", url="https://www.whatsapp.com/channel/0029VaeFkY9FXUuV971StZ0W"))

class RolesView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        for role_name, role_id in ROLES_DICT.items():
            self.add_item(RoleButton(role_name, role_id))
    
    @discord.ui.button(label="Get All Roles", style=discord.ButtonStyle.blurple, custom_id="roles_get_all", row=3)
    async def get_all(self, interaction: discord.Interaction, button: discord.ui.Button):
        roles = [interaction.guild.get_role(rid) for rid in ROLES_DICT.values() if interaction.guild.get_role(rid)]
        await interaction.user.add_roles(*roles)
        await interaction.response.send_message("✅ تم إعطائك جميع رتب الإشعارات.", ephemeral=True)

    @discord.ui.button(label="Remove All Roles", style=discord.ButtonStyle.red, custom_id="roles_rem_all", row=3)
    async def rem_all(self, interaction: discord.Interaction, button: discord.ui.Button):
        roles = [interaction.guild.get_role(rid) for rid in ROLES_DICT.values() if interaction.guild.get_role(rid)]
        await interaction.user.remove_roles(*roles)
        await interaction.response.send_message("🗑️ تم إزالة جميع رتب الإشعارات.", ephemeral=True)

class RoleButton(discord.ui.Button):
    def __init__(self, name, r_id):
        super().__init__(label=name, style=discord.ButtonStyle.grey, custom_id=f"role_{r_id}")
        self.r_id = r_id

    async def callback(self, interaction: discord.Interaction):
        role = interaction.guild.get_role(self.r_id)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"➖ تم إزالة رتبة **{role.name}**", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"➕ تم إعطائك رتبة **{role.name}**", ephemeral=True)


# ==========================================
# 📝 نظام التقديمات (Applications)
# ==========================================
class AppModal(discord.ui.Modal):
    def __init__(self, department):
        super().__init__(title=f"Application: {department}")
        self.department = department
        
        if department == "Staff Team":
            self.add_item(discord.ui.TextInput(label="الاسم - العمر - الدولة؟"))
            self.add_item(discord.ui.TextInput(label="ساعات التواجد يومياً؟"))
            self.add_item(discord.ui.TextInput(label="كيف تتعامل مع عضو يخالف القوانين؟", style=discord.TextStyle.paragraph))
            self.add_item(discord.ui.TextInput(label="لماذا اخترت إدارة iMLKq؟", style=discord.TextStyle.paragraph))
        elif department == "Lady":
            self.add_item(discord.ui.TextInput(label="الاسم (أو اللقب) - العمر؟"))
            self.add_item(discord.ui.TextInput(label="متوسط تفاعلك اليومي؟"))
            self.add_item(discord.ui.TextInput(label="كيف تتصرفين لو أزعجك عضو؟", style=discord.TextStyle.paragraph))
            self.add_item(discord.ui.TextInput(label="أفكار لتنشيط الرومات؟", style=discord.TextStyle.paragraph))
        elif department == "Developer Team":
            self.add_item(discord.ui.TextInput(label="الاسم - العمر؟"))
            self.add_item(discord.ui.TextInput(label="لغات البرمجة التي تتقنها؟"))
            self.add_item(discord.ui.TextInput(label="أمثلة على أعمالك أو بوتاتك؟", style=discord.TextStyle.paragraph))
            self.add_item(discord.ui.TextInput(label="قدرتك على حل البقز والمشاكل؟"))
        elif department == "Events Team":
            self.add_item(discord.ui.TextInput(label="الاسم - العمر؟"))
            self.add_item(discord.ui.TextInput(label="أنواع الفعاليات التي تجيد إدارتها؟"))
            self.add_item(discord.ui.TextInput(label="هل المايك واضح ومناسب للفعاليات?"))
            self.add_item(discord.ui.TextInput(label="كيف تتصرف إذا لم يكن هناك تفاعل؟", style=discord.TextStyle.paragraph))

    async def on_submit(self, interaction: discord.Interaction):
        global app_counter
        room_id = APP_ROOMS.get(self.department)
        admin_channel = bot.get_channel(room_id)
        
        embed = discord.Embed(title=f"New Application | Number : [ {app_counter} ]", color=discord.Color.gold())
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
        embed.add_field(name="القسم المطلوب:", value=f"**{self.department}**", inline=False)
        embed.add_field(name="صاحب الطلب:", value=f"{interaction.user.mention} (ID: {interaction.user.id})", inline=False)
        
        for item in self.children:
            embed.add_field(name=item.label, value=item.value, inline=False)
        
        embed.set_footer(text="iMLKq System", icon_url=LOGO_URL)
        
        await admin_channel.send(embed=embed, view=AdminActionView(interaction.user, self.department))
        app_counter += 1
        await interaction.response.send_message("✅ تم إرسال طلبك بنجاح للإدارة المختصة.", ephemeral=True)

class ApplicationView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(
        placeholder="Apply Here",
        custom_id="imlkq_app_select",
        options=[
            discord.SelectOption(label="Staff Team", emoji="🛡️"),
            discord.SelectOption(label="Lady", emoji="🌸"),
            discord.SelectOption(label="Developer Team", emoji="💻"),
            discord.SelectOption(label="Events Team", emoji="🎉")
        ]
    )
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        await interaction.response.send_modal(AppModal(select.values[0]))

class AdminActionView(discord.ui.View):
    def __init__(self, applicant, dept):
        super().__init__(timeout=None)
        self.applicant = applicant
        self.dept = dept

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green, emoji="✅", custom_id="app_accept")
    async def btn_accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.user.guild_permissions.administrator: return await interaction.response.send_message("❌ للإدارة فقط.", ephemeral=True)
        for child in self.children: child.disabled = True
        try: await self.applicant.send(f"🎉 تهانينا! تم قبول طلبك للانضمام إلى فريق **{self.dept}**.")
        except: pass
        await interaction.message.edit(content=f"✅ تم القبول بواسطة {interaction.user.mention}", view=self)
        await interaction.response.send_message("تم تنفيذ الإجراء.", ephemeral=True)

    @discord.ui.button(label="Reject", style=discord.ButtonStyle.red, emoji="❌", custom_id="app_reject")
    async def btn_reject(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.user.guild_permissions.administrator: return await interaction.response.send_message("❌ للإدارة فقط.", ephemeral=True)
        for child in self.children: child.disabled = True
        try: await self.applicant.send(f"❌ نعتذر، تم رفض طلبك للانضمام إلى فريق **{self.dept}**.")
        except: pass
        await interaction.message.edit(content=f"❌ تم الرفض بواسطة {interaction.user.mention}", view=self)
        await interaction.response.send_message("تم تنفيذ الإجراء.", ephemeral=True)


# ==========================================
# 📩 نظام التذاكر (Tickets)
# ==========================================
class TicketPanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Open Ticket", style=discord.ButtonStyle.grey, emoji="📩", custom_id="imlkq_open_ticket")
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        category = bot.get_channel(TICKET_CATEGORY_ID)
        ticket_channel = await interaction.guild.create_text_channel(
            name=f"ticket-{interaction.user.name}",
            category=category,
            overwrites={
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True),
                interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }
        )
        await interaction.response.send_message(f"✅ تم فتح تذكرتك: {ticket_channel.mention}", ephemeral=True)
        
        embed = discord.Embed(
            description="Welcome to your ticket. Please wait for the staff to assist you.",
            color=discord.Color.from_str("#39baf7")
        )
        embed.set_footer(text="iMLKq Support", icon_url=LOGO_URL)
        await ticket_channel.send(content=f"{interaction.user.mention} Welcome", embed=embed, view=TicketControlView())

class TicketControlView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close", style=discord.ButtonStyle.red, emoji="🔒", custom_id="imlkq_close_ticket")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.user.guild_permissions.manage_channels:
            return await interaction.response.send_message("❌ للإدارة فقط.", ephemeral=True)
        await interaction.response.send_message("🔒 سيتم إغلاق التذكرة خلال 5 ثوانٍ...")
        
        await asyncio.sleep(5)
        await interaction.channel.delete()


# ==========================================
# 🛠️ بانل الإدارة (Admin Control Panel)
# ==========================================
class AdminPanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Ban", style=discord.ButtonStyle.red, emoji="🔨", custom_id="admin_ban")
    async def btn_ban(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.user.guild_permissions.ban_members: return await interaction.response.send_message("❌ لا تملك صلاحية.", ephemeral=True)
        await interaction.response.send_modal(AdminActionModal("Ban Member", "ban"))

    @discord.ui.button(label="Kick", style=discord.ButtonStyle.red, emoji="👢", custom_id="admin_kick")
    async def btn_kick(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.user.guild_permissions.kick_members: return await interaction.response.send_message("❌ لا تملك صلاحية.", ephemeral=True)
        await interaction.response.send_modal(AdminActionModal("Kick Member", "kick"))

    @discord.ui.button(label="Timeout", style=discord.ButtonStyle.grey, emoji="⏳", custom_id="admin_timeout")
    async def btn_timeout(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.user.guild_permissions.moderate_members: return await interaction.response.send_message("❌ لا تملك صلاحية.", ephemeral=True)
        await interaction.response.send_modal(AdminActionModal("Timeout Member (Minutes)", "timeout"))

    @discord.ui.button(label="Remove Timeout", style=discord.ButtonStyle.green, emoji="✅", custom_id="admin_untimeout")
    async def btn_untimeout(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.user.guild_permissions.moderate_members: return await interaction.response.send_message("❌ لا تملك صلاحية.", ephemeral=True)
        await interaction.response.send_modal(AdminActionModal("Remove Timeout", "untimeout"))

    @discord.ui.button(label="Say", style=discord.ButtonStyle.blurple, emoji="💬", custom_id="admin_say")
    async def btn_say(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.user.guild_permissions.manage_messages: return await interaction.response.send_message("❌ لا تملك صلاحية.", ephemeral=True)
        await interaction.response.send_modal(AdminMessageModal("Send Message", "say"))

    @discord.ui.button(label="Broadcast", style=discord.ButtonStyle.blurple, emoji="📢", custom_id="admin_bc")
    async def btn_bc(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.user.guild_permissions.administrator: return await interaction.response.send_message("❌ لا تملك صلاحية.", ephemeral=True)
        await interaction.response.send_modal(AdminMessageModal("Broadcast Announcement", "bc"))

class AdminActionModal(discord.ui.Modal):
    def __init__(self, title, action):
        super().__init__(title=title)
        self.action = action
        self.user_id = discord.ui.TextInput(label="User ID", placeholder="123456789...")
        self.reason = discord.ui.TextInput(label="Reason / Duration", placeholder="السبب (أو مدة التايم اوت بالدقائق)", required=False)
        self.add_item(self.user_id)
        self.add_item(self.reason)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            member = interaction.guild.get_member(int(self.user_id.value))
            if not member: return await interaction.response.send_message("❌ العضو غير موجود.", ephemeral=True)

            if self.action == "ban":
                await member.ban(reason=self.reason.value)
                await interaction.response.send_message(f"✅ تم حظر {member.mention}", ephemeral=True)
            elif self.action == "kick":
                await member.kick(reason=self.reason.value)
                await interaction.response.send_message(f"✅ تم طرد {member.mention}", ephemeral=True)
            elif self.action == "timeout":
                duration = int(self.reason.value) if self.reason.value.isdigit() else 10
                await member.timeout(discord.utils.utcnow() + datetime.timedelta(minutes=duration))
                await interaction.response.send_message(f"✅ تم إسكات {member.mention} لمدة {duration} دقائق.", ephemeral=True)
            elif self.action == "untimeout":
                await member.timeout(None)
                await interaction.response.send_message(f"✅ تم فك الإسكات عن {member.mention}", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ حدث خطأ: {e}", ephemeral=True)

class AdminMessageModal(discord.ui.Modal):
    def __init__(self, title, action):
        super().__init__(title=title)
        self.action = action
        
        if action in ["say", "bc"]:
            self.channel_id = discord.ui.TextInput(
                label="Channel ID (آيدي الروم)", 
                placeholder="مثال: 147152900810282519"
            )
            self.add_item(self.channel_id)
            
        self.msg = discord.ui.TextInput(
            label="Message (الرسالة)", 
            style=discord.TextStyle.paragraph
        )
        self.add_item(self.msg)

    async def on_submit(self, interaction: discord.Interaction):
        ch = interaction.guild.get_channel(int(self.channel_id.value))
        if not ch:
            return await interaction.response.send_message("❌ لم يتم العثور على الروم، تأكد من الآيدي الصحيح.", ephemeral=True)

        if self.action == "say":
            await ch.send(self.msg.value)
            await interaction.response.send_message(f"✅ تم إرسال الرسالة بنجاح إلى {ch.mention}.", ephemeral=True)
        elif self.action == "bc":
            embed = discord.Embed(title="📢 iMLKq Announcement", description=self.msg.value, color=discord.Color.gold())
            embed.set_footer(text="iMLKq System", icon_url=LOGO_URL)
            await ch.send(content="@everyone", embed=embed)
            await interaction.response.send_message(f"✅ تم إرسال الإعلان بنجاح إلى {ch.mention}.", ephemeral=True)


# ==========================================
# 🛠️ أمر تثبيت جميع اللوحات بضغطة زر
# ==========================================
@bot.tree.command(name="setup_panels", description="أمر إداري لإرسال جميع اللوحات للرومات المخصصة")
async def setup_panels(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("❌ هذا الأمر مخصص للإدارة فقط.", ephemeral=True)

    await interaction.response.defer(ephemeral=True)

    main_embed = discord.Embed(
        description="شكراً لانضمامك في خادم **أبو ملك (iMLKq Community)** الرسمي.\nيمكنك مشاهدة جميع القوانين والأنظمة، ولا ننسى أيضًا أنه يمكنك أخذ رتبة من رتب الإشعارات عن طريق الأزرار الموجودة بالأسفل.",
        color=discord.Color.from_str("#39baf7")
    )
    main_embed.set_image(url=MAIN_PANEL_IMG)
    await interaction.channel.send(embed=main_embed, view=MainPanelView())

    app_room = bot.get_channel(APP_PANEL_ROOM)
    if app_room:
        app_embed = discord.Embed(
            title="iMLKq Team Application",
            description="**من خلال المنيو بالاسفل بإمكانك 📝**\n**التقديم على فريق العمل لـ**\n**iMLKq Team**\n\n• Staff Team 🛡️\n• Lady 🌸\n• Developer Team 💻\n• Events Team 🎉",
            color=discord.Color.gold()
        )
        app_embed.set_thumbnail(url=LOGO_URL)
        app_embed.set_image(url=APP_BANNER)
        await app_room.send(embed=app_embed, view=ApplicationView())

    ticket_room = bot.get_channel(TICKET_PANEL_ROOM)
    if ticket_room:
        t_embed = discord.Embed(
            description="Welcome to the ticket system, here you can open a ticket and get help from the staff team. Please read the rules before opening a ticket.",
            color=discord.Color.from_str("#39baf7")
        )
        t_embed.set_thumbnail(url=LOGO_URL)
        t_embed.set_image(url=TICKET_BANNER)
        await ticket_room.send(embed=t_embed, view=TicketPanelView())

    admin_room = bot.get_channel(ADMIN_PANEL_ROOM)
    if admin_room:
        admin_embed = discord.Embed(
            title="⚙️ Admin Control Panel",
            description="استخدم الأزرار بالأسفل لإدارة السيرفر بسرعة وسهولة.",
            color=discord.Color.dark_theme()
        )
        admin_embed.set_thumbnail(url=LOGO_URL)
        await admin_room.send(embed=admin_embed, view=AdminPanelView())

    await interaction.followup.send("✅ تم إرسال جميع اللوحات بنجاح!")

bot.run(TOKEN)