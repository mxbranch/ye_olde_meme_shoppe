# libraries 

from discord.ext import commands
import discord
from dotenv import dotenv_values
from PIL import Image, ImageDraw, ImageFont
import os

# bot_main() - wrapper function for program

def bot_main():

    # load environmental variables
    env = dotenv_values(".env")

    # initialise bot
    bot = commands.Bot(command_prefix = "#")

    # load font for image macro creation
    font = ImageFont.truetype('res/impact.ttf', 60)

    # initial event function
    @bot.event
    async def on_ready():
        print("{} logged in.".format(bot.user))

    # ignore our own messages, parse any given commands
    @bot.event 
    async def on_message(message):
        if message.author == bot.user:
            return
        await bot.process_commands(message)

    # #meme top bottom (img)
    # Generates an image macro based on a locally stored file
    @bot.command()
    async def meme(ctx, top, bottom, img=None):

        # use default.png if no image is specified
        if img == None:
            img = "default"

        # try opening the requested image - if this doesn't happen throw error message
        try:
            image = Image.open("res/" + img  +".png")
        except:
            await ctx.send("Error: Incorrect Template")
            return

        # get the image's width and height for text positioning

        W, H = image.size

        # open the image as a drawing surface and write top and bottom text

        draw = ImageDraw.Draw(image)

        w = draw.textlength(top, font = font)
        draw.text(((W - w) / 2, 60 / 4), top, font = font, fill = (255, 255, 255), stroke_width = 4, stroke_fill = (0, 0, 0))
        w = draw.textlength(bottom, font = font)
        draw.text(((W - w) / 2, H - 60 * 1.5), bottom, font = font, fill = (255, 255, 255), stroke_width = 4, stroke_fill = (0, 0, 0))

        image.save("res/meme.png")
        image.close()

        # load the resulting file again and send it to discord

        image = discord.File('res/meme.png')

        await ctx.send(file=image)

        return

    # #memethat top bottom
    # Expects to be called as a reply to another message containing an image.
    # Generates an image macro based on the image it is replying to.
    @bot.command()
    async def memethat(ctx, top, bottom):
        
        # Check to see if the command has been invoked in a reply to an image
        try:

            message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            if str(message.attachments) == "[]":

                await ctx.send("Error: command must be used in reply to an image")
                return

            else:

                # if the image reply exists get the filename of the image
                filename = str(message.attachments).split("filename='")[1].split("' ")[0]
                # if it's a png save it, if it's a jpg convert it to png then save it
                if filename.endswith(".png"):
                    await message.attachments[0].save(fp = "res/temp.png")
                if filename.endswith(".jpg") or filename.endswith(".jpeg"):
                    await message.attachments[0].save(fp = "res/temp.jpg")
                    img = Image.open("res/temp.jpg")
                    img.save("res/temp.png")
                    img.close()
                    os.remove("res/temp.jpg")
                
                # if the image is too large resize it
                img = Image.open("res/temp.png")
                W, H = img.size
                if W > 800.0:
                    scale: float = 800.0 / W
                    scaleimg = img.resize((800, int(H*scale)))
                    scaleimg.save("res/temp.png")
                img.close()

        except:
            await ctx.send("Error: command must be used in reply to an image.")
            return
        
        # use the meme function to add text to the temp image
        # then post it as a message.
        await meme(ctx, top, bottom, "temp")


    # #addimage name
    # Expects to be invoked as a reply to a message with an image. 
    # Checks to see if name is available then downloads image into local storage.
    @bot.command()
    async def addimage(ctx, name):

        # Check if the requested name is free
        try:

            image = open("res/" + name + ".png")
            await ctx.send("Error: image id already used, try another")
            image.close()
            return

        except:

            # If requested name is free check that message was a reply w/ an image
            try:

                message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
                if str(message.attachments) == "[]":

                    await ctx.send("Error: command must be used in reply to an image")
                    return

                else:

                    # if the image reply exists get the filename of the image
                    filename = str(message.attachments).split("filename='")[1].split("' ")[0]

                    # if it's a png save it, if it's a jpg convert it to png then save it
                    if filename.endswith(".png"):
                        await message.attachments[0].save(fp = "res/"+name+".png")
                    if filename.endswith(".jpg") or filename.endswith(".jpeg"):
                        await message.attachments[0].save(fp = "res/"+name+".jpg")
                        img = Image.open("res/"+name+".jpg")
                        img.save("res/"+name+".png")
                        img.close()
                        os.remove("res/"+name+".jpg")
                    
                    # if the image is too large resize it
                    img = Image.open("res/"+name+".png")
                    W, H = img.size
                    if W > 800.0:
                        scale: float = 800.0 / W
                        scaleimg = img.resize((800, int(H*scale)))
                        scaleimg.save("res/"+name+".png")
                    img.close()

            except:
                await ctx.send("Error: command must be used in reply to an image.")
                return
            
            # confirmation message
            await ctx.send("Added image to database with name: " + name)

    # go bot go!
    bot.run(env['TOKEN'])

if __name__ == "__main__":
    bot_main()