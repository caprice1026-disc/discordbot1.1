import discord
import discord.ext.commands
import os 
import requests

#トークンを自身のものに書き換える
TOKEN = ("discordbot_TOKEN")
Alchemy_key = ("alchemy_key")

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)
prefix = "/"
#鯖設定するなら　guild = discord.guild(id=)
class confomationview(discord.ui.View):
    def __init__(self, interaction: discord.Interaction, timeout=60, text=""):
        super().__init__(timeout=timeout)
        self.send_embed = discord.Embed(title="新作の宣伝です！", description=text)
        self.send_embed.set_author(
           name=interaction.user.display_name, 
           icon_url=interaction.user.display_avatar.url, 
        ).set_footer(
           text=f"transfar from {interaction.user.display_name}",
           icon_url=interaction.user.display_avatar.url,
        )
        #チャンネルID書き換えること
        self.channel = client.get_channel(channel_id)
    @discord.ui.button(label="OK", style=discord.ButtonStyle.success)
    async def ok(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.channel.send(embed=self.send_embed)
        pass
    @discord.ui.button(label="NG", style=discord.ButtonStyle.gray)
    async def ng(self, button: discord.ui.Button, interaction: discord.Interaction):
        pass
    
@client.event
async def on_ready():
    print("起動完了")
    await tree.sync()


@tree.command(name="promotion",description="アクティブクリエイターが宣伝するためのコマンドです。")
@discord.app_commands.describe(role="誰に送るかを指定。",text="送りたい文章を書き込んでください。")
async def promotion(interaction: discord.Interaction,role: discord.Role,text: str):
    #フォローアップ関数をそのうち実装予定
    rolename = role
    view = confomationview(interaction=interaction, text=text,)
    #Interaction.response.send_message()
    await interaction.response.send_message(f"{rolename}へ{text}  と送信してよいですか？", ephemeral=True)
    await interaction.followup.send(view=view, ephemeral=True) 

@tree.command(name="roleee",description="ロール所持者を出力するコマンドです。")
async def roleee(interaction: discord.Interaction,role: discord.Role):
    #ロールの名前を取得
    rolename = role
    #ロールのメンバーを取得
    members = rolename.members
    #メンバーの名前を取得
    membername = [member.name for member in members]
    #メンバーの名前を改行で区切って出力
    await interaction.response.send_message(f"{membername}", ephemeral=True)

"""ここから先はまだ完成していないコマンドです。2000時以上の文章を送信するとエラーを吐くのでどっか別の場所に出力しようね。

@tree.command(name="holder",description="NFT所持者を出力するコマンドです。")
async def holder(interaction: discord.Interaction,token: str):
    url = f"{Alchemy_key}/getOwnersForCollection?contractAddress={token}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    await interaction.response.send_message(f"{response.text}", ephemeral=True)

"""


client.run(TOKEN)