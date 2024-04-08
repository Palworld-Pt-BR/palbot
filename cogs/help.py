import nextcord
from nextcord.ext import commands
from nextcord.ui import Button, View
import util.constants as constants

class HelpView(View):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.current_page = 0

    async def generate_help_embed(self):
        embed = nextcord.Embed(
            title="Menu de Ajuda",
            description="Lista de todos os comandos disponíveis.",
            color=nextcord.Color.blue(),
        )
        embed.set_footer(
            text=f"{constants.FOOTER_TEXT}: Página {self.current_page + 1}",
            icon_url=constants.FOOTER_IMAGE,
        )

        commands = (
            self.bot.all_slash_commands
            if hasattr(self.bot, "all_slash_commands")
            else []
        )
        start = self.current_page * 9
        end = min(start + 9, len(commands))

        for command in commands[start:end]:
            embed.add_field(
                name=f"`/{command.name}`",
                value=command.description or "Sem descrição",
                inline=True,
            )
        return embed

    @nextcord.ui.button(label="Anterior", style=nextcord.ButtonStyle.blurple)
    async def previous_button_callback(self, button, interaction):
        if self.current_page > 0:
            self.current_page -= 1
            await self.update_help_message(interaction)

    @nextcord.ui.button(label="Próxima", style=nextcord.ButtonStyle.blurple)
    async def next_button_callback(self, button, interaction):
        if (self.current_page + 1) * 9 < len(
            self.bot.all_slash_commands
            if hasattr(self.bot, "all_slash_commands")
            else []
        ):
            self.current_page += 1
            await self.update_help_message(interaction)

    async def update_help_message(self, interaction):
        embed = await self.generate_help_embed()
        await interaction.response.edit_message(embed=embed, view=self)


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="Mostra uma lista de comandos disponíveis.")
    async def help(self, interaction: nextcord.Interaction):
        view = HelpView(self.bot)
        embed = await view.generate_help_embed()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    # Por favor, não remova a seção sobre mim. Eu passei muito tempo neste bot e eu ficaria grato se você deixasse ela.
    @nextcord.slash_command(description="Informações sobre o bot do Palworld.")
    async def about(self, interaction: nextcord.Interaction):

        embed = nextcord.Embed(
            title="Bot do Palworld", color=nextcord.Color.blue(), url=constants.TITLE_URL
        )
        embed.set_footer(text=constants.FOOTER_TEXT, icon_url=constants.FOOTER_IMAGE)
        embed.add_field(
            name="Sobre",
            value="O bot é um projeto de código aberto disponível [aqui](https://github.com/dkoz/palworld-bot). Você pode encontrar mais informações no nosso readme. Estou sempre procurando contribuições de código e suporte! Se houver algo errado com o bot em si, por favor, me avise",
            inline=False,
        )
        embed.add_field(
            name="Criador",
            value="Este bot foi criado por [Kozejin](https://kozejin.dev). Sinta-se à vontade para adicionar `koz#1337` no Discord se tiver alguma dúvida.",
            inline=False,
        )
        embed.add_field(
            name="Apoiar",
            value="Se desejar apoiar o bot, você pode se juntar ao nosso [Discord](https://discord.gg/3HUq8cJSrX).",
            inline=False,
        )

        discord_button = Button(
            label="Discord",
            url="https://discord.gg/3HUq8cJSrX",
            style=nextcord.ButtonStyle.link,
        )
        github_button = Button(
            label="GitHub",
            url="https://github.com/dkoz/palworld-bot",
            style=nextcord.ButtonStyle.link,
        )
        kofi_button = Button(
            label="Apoiar",
            url="https://ko-fi.com/kozejin",
            style=nextcord.ButtonStyle.link,
        )

        view = View()
        view.add_item(discord_button)
        view.add_item(github_button)
        view.add_item(kofi_button)

        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

def setup(bot):
    bot.add_cog(HelpCog(bot))