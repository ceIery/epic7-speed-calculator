import ocr
import calc
import discord
from discord.ext import commands
import config
import traceback
from PIL import Image
from io import BytesIO
import requests

bot = commands.Bot(command_prefix='.')

formats = [".jpg", ".png"]


"""
Main speed command
"""
@bot.command(pass_context=True)
async def speed(ctx, base, url=None):
    # in case the bot ever tries to reply to itself
    if ctx.message.author == bot.user:
        return
    # Check if command triggered
    if len(ctx.message.attachments) > 0:
        url = ctx.message.attachments[0].url

    print("input url:", url)

    # Validate attachments
    if url is not None:
        valid = False
        for i in formats:
            if i in url:
                valid = True
        if not valid:
            print("not a supported link")
            print("-----")
            await send_error(ctx,
                             "File not supported. Accepted formats: jpg, png")
            return

    # No attachment provided
    else:
        print("no input url found")
        print("-----")
        return

    # Handle image
    try:
        # Download image
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
        }

        response = requests.get(url, headers=headers)
        img = Image.open(BytesIO(response.content))

        # urllib.request.urlretrieve(url, "temp/" + filename)
        # path = "temp/" + filename

        # Process image for OCR
        img = ocr.preprocessing(img)

        # Run OCR on image
        percents = ocr.get_percents(img)

        # Calculate speeds
        speeds = calc.get_speeds(percents, base)
        await make_embed(ctx, percents, speeds)

    # Download/image processing failed
    except Exception as e:
        traceback.print_exc()
        await send_error(ctx,
                         "Unknown exception occurred")
    print('------')


"""
Creates the embed sent to the user, given the percentages and values of speed
"""
@bot.event
async def make_embed(ctx, percents, speeds):
    embed = discord.Embed(title="Speed Calculator")
    embed.set_footer(text="±10 speed")

    for i in range(0, len(speeds)):
        embed.add_field(name=str(speeds[i]) + " speed",
                        value=(str(percents[i]) + "%"))
    await ctx.send(embed=embed)


"""
Creates error embed sent to user
"""
@bot.event
async def send_error(ctx, msg):
    embed = discord.Embed(title=msg, colour=0xF44336)
    await ctx.send(embed=embed)


"""
Outputs to console when bot is logged in
"""
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


# Start bot
bot.run(config.BOT_TOKEN)
