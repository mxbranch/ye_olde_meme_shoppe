# ye_olde_meme_shoppe

A discord bot which can generate old-fashioned "top and bottom text" style image macros from a collection of built-in images or from any image that was sent on a server.

## Prerequisites

- [discord.py](https://github.com/Rapptz/discord.py)
- [Pillow](https://github.com/python-pillow/Pillow)
- [python-dotenv](https://github.com/theskumar/python-dotenv)

## Commands

- `#meme top bottom (template)`
  - Generates an image macro from the given template file.
- `#memethat top bottom`
  - When used as a reply to a message with an image attachment generates a macro using that image.
- `#addimage id`
  - When used as a reply to a message with an image attachment this command downloads the image and adds it as a template with the given id.

## Example Output

![Image of a sunrise with "Nature is beautiful" written on it](/res/example.png)

## Warning

This bot is not ready for use on public servers! Only use it on servers with people you trust as it Can and Will download images without any regard for the safety of you or others! You Have Been Warned.
