import discord
import random
import sqlite3
from discord.commands import Option
from discord import Embed

Regel = "Rate eine Zahl zwischen 1 und 100"
Token = open("Token.txt")
Zufall = random.randint(1, 100)
Versuche = 0
got4 = 0
get4 = 0
conn = sqlite3.connect("Score.db")
c = conn.cursor()
bot = discord.Bot(
    activity=discord.Activity(type=discord.ActivityType.playing, name="/rate")
)


@bot.event
async def on_ready():
    Token.close()
    print(f"{bot.user} is ready and online!")
    print(Zufall)


@bot.slash_command(name="rate", description="Rate eine Zahl")
async def rate(ctx, zahl: discord.Option(discord.SlashCommandOptionType.integer)):
    user = ctx.author
    user_id = user.id
    global Zufall, got4, Versuche
    if zahl < Zufall:
        await ctx.respond("Zu Klein")
        Versuche = Versuche + 1
        if Versuche == 5:
            if Zufall > 50:
                await ctx.send("Die Zahl ist größer als 50")
            else:
                await ctx.send("Die Zahl ist kleiner als 50")
    if zahl > Zufall:
        await ctx.respond("Zu Groß")
        Versuche = Versuche + 1
        if Versuche == 5:
            if Zufall > 50:
                await ctx.send("Die Zahl ist größer als 50")
            else:
                await ctx.send("Die Zahl ist kleiner als 50")
    if zahl == Zufall:
        for row in c.execute(f"SELECT score FROM score WHERE id='{user_id}'"):
            got = f"{row}"
            got1 = got.replace(")", "")
            got2 = got1.replace(",", "")
            got3 = got2.replace("(", "")
            got4 = int(got3)
        c.execute(f"DELETE FROM score WHERE id='{user_id}'")
        c.execute(f"INSERT INTO score VALUES ({user_id}, {got4 + 1})")
        conn.commit()
        await ctx.respond("Richtig!!")
        Versuche = Versuche + 1
        await ctx.send(f"Du hast {Versuche} mal Geraten")
        Versuche = 0
        Zufall = random.randint(1, 100)
        await ctx.send("Neue Zahl")
        print(Zufall)


@bot.slash_command(name="regeln", description="erklärt die Regeln")
async def regeln(ctx):
    await ctx.respond(Regel)


@bot.slash_command(name="github", description="Zeigt die GitHub Page vom Bot")
async def github(ctx):
    await ctx.respond("Hier ist meine Github Page: https://github.com/Kokoio01/Zahlenspielbot")


@bot.slash_command(name="score", description="Zeigt den Score an")
async def score(ctx, user: Option(discord.User, "User", required=False)):
    member = user or ctx.author
    member_id = member.id
    global get4
    for row in c.execute(f"SELECT score FROM score WHERE id='{member_id}'"):
        get = f"{row}"
        get1 = get.replace(")", "")
        get2 = get1.replace(",", "")
        get3 = get2.replace("(", "")
        get4 = int(get3)
    pfp = member.display_avatar.url
    if get4 == 0:
        score1 = discord.Embed(title="Score", color=0x000000)
        score1.add_field(name=member, value="hat noch nie gespielt", inline=True)
        score1.set_thumbnail(url=pfp)
        await ctx.respond(embed=score1)
    else:
        score2 = discord.Embed(title="Score", color=0x2ec27e)
        score2.add_field(name=member, value=f"hat {get4} mal gewonnen", inline=True)
        score2.set_thumbnail(url=pfp)
        await ctx.respond(embed=score2)

bot.run(Token.read())
close()
