from discord.ext import commands
import discord

class Zero(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @commands.command('zencode')
    async def zencode(self,ctx:commands.Context,text:str,enctext):
        if len(text)*8 + len(enctext) >= 1014:
            return await ctx.send("that text is too long!")
        binarystr = ''.join(format(ord(i), '08b') for i in enctext)
        #binarystr = ' '.join(format(ord(l), 'b') for l in enctext)
        zwsp = '​'
        zwj = '‍'
        zwnj = '‌'
        zwstring = binarystr.replace('1',zwsp)
        zwstring = zwstring.replace('0',zwj)
        zwstring = zwstring.replace(' ',zwnj)
        final = text + zwstring
        embed=discord.Embed(color=self.bot.color)
        embed.set_author(name=ctx.author.display_name,icon_url=ctx.author.avatar_url)
        embed.add_field(name="your text:",value=f"```{final}```")
        await ctx.send(embed=embed)

    @commands.command('zdecode')
    async def zdecode(self, ctx:commands.Context, *, text):
        zwsp = '​'
        zwj = '‍'
        zwnj = '‌'
        encstr = text
        dec = ''
        for n, i in enumerate(encstr):
            if i == zwsp:
                dec += '1'
            elif i == zwj:
                dec += '0'
            elif i == zwnj:
                dec += ' '
        final = ''
        nt = dec.split(' ')
        for c in nt:
            for i in range(0, len(c), 8):
                ntext = c[i:i+8]
                if i == ' ':
                    continue
                final += chr(int(ntext, 2))
            final += " "
        embed=discord.Embed(color=self.bot.color)
        embed.set_author(name=ctx.author.display_name,icon_url=ctx.author.avatar_url)
        embed.add_field(name="original text:",value=f"```{text}```")
        embed.add_field(name="hidden text:",value=f"```{final}```")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Zero(bot))
