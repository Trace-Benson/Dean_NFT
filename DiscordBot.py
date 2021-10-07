import discord
from discord.ext import commands
from Leaderboard import Leaderboard
from Arena import Arena


with open("key.txt", "r") as f:
    token = f.read()

bot = commands.Bot(command_prefix="!")
stick_csv_path = "cryptostykz_v3.csv"
#token = "ODkzMTUxNjA0MjcyOTI2NzIx.YVXSQA.v1wSt6knVE9UUhyMgSQz5FrCoHg"
client = discord.Client()
leaderboard = Leaderboard()
arena = Arena(["cryptostykz_v3.csv"])

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to the server.")


@bot.command(name="ping",
             brief="Test if the bot is communicating with the server",
             description="Should reply with \"pong\"")
async def ping_cmd(ctx):
    await ctx.send("pong")


@bot.command(name="fight",
             brief="Fights 2 CryptoStkz against eachother",
             description="To fight #175 against #300 use the command:\n!fight #175 #300")
async def fight_cmd(ctx, s1, s2):
    valid = False
    msg = ""
    if arena.verify_stick(s1):
        if arena.verify_stick(s2):
            valid = True
        else:
            msg += f"Invalid stick number: \"{s2}\""
    else:
        msg += f"Invalid stick number: \"{s1}\""

    if valid:
        msg = f">>> **{s1} vs {s2}**\n"
        s1_r = arena.get_stick(s1)["rarity"]
        s2_r = arena.get_stick(s2)["rarity"]
        msg += f"{s1} has a rarity of **{s1_r}** and {s2} has a rarity of **{s2_r}**\n"
        rounds = arena.fight_sticks(s1, s2)
        for round, winner in enumerate(rounds):
            msg += f"Round {round + 1} goes to {winner}\n"
        msg += f"{arena.match_winner(rounds)} won the match!"
        leaderboard.update_leaderboard(rounds, [s1, s2])
    await ctx.send(msg)


@bot.command(name="rfight",
             brief="Fight two random CryptoStykz",
             description="""Randomly select two different CryptoStykz to fight each other""")
async def rfight_cmd(ctx):
    fighters = arena.random_fighers()
    await fight_cmd(ctx, fighters[0], fighters[1])




@bot.command(name="specs",
             brief="Display the rarity of each component of a CryptoStyk",
             description="""Sends a message back to you containing the rarity of each component of a CryptoStyk given its number
                            !specs #119""")
async def specs_cmd(ctx, snum):
    if arena.verify_stick(snum):
        stick = arena.get_stick(snum)
        msg = f">>> **CryptoStykz {snum}**\n"
        msg += f"Overall rarity: **{stick['rarity']}**\n"
        msg += f"Background: {stick['bg']}\n"
        msg += f"Body: {stick['body']}\n"
        msg += f"Miscellaneous: {stick['misc']}\n"
        msg += f"Hand: {stick['hand']}"
        await ctx.send(msg)
    else:
        await ctx.send(f"Invalid stick number \"{snum}\"")


@bot.command(name="leaders",
             brief="Display the top 5 Cryptostykz with the most wins",
             description="""The bot will reply with a message containing the leaderboard with the top 5 highest ranked
                            Cryptostykz with the most matches won""")
async def leaderboard_cmd(ctx):
    leaderboard.make_leaderboard()
    with open(leaderboard.png_name, "rb") as f:
        image = discord.File(f)
        await ctx.send(file=image)


@bot.command(name="tfight")
async def test_fight_cmd(ctx):
    await fight_cmd(ctx, "#1", "#5")
    await fight_cmd(ctx, "#1", "#2")
    await fight_cmd(ctx, "#2", "#5")
    await fight_cmd(ctx, "#1", "#6")
    await fight_cmd(ctx, "#2", "#6")
    await leaderboard_cmd(ctx)


bot.run(token)

