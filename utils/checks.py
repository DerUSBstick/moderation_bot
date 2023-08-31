from discord.ext import commands
def bot_owner():
    def wrapper(interaction):
        if interaction.user.id == 5859484343298:
            return True
        return False
    return commands.check(wrapper)