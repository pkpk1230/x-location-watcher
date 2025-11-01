from discord_webhook import DiscordEmbed

def create_embed(platform, event_type, url, fields):
    colors = {
        "twitch": 0x9146FF,
        "kick": 0x00FF00,
        "x": 0x000000
    }

    titles = {
        "start": "🟣 配信が開始されました",
        "end": "🔴 配信が終了しました",
        "title_change": "✏️ タイトルが変更されました",
        "category_change": "🕹 カテゴリが変更されました",
        "profile_change": "📢 プロフィールが変更されました"
    }

    embed = DiscordEmbed(
        title=titles.get(event_type, "📢 状態変化を検知"),
        description=f"{url} にて {titles.get(event_type, '状態変化')} が検知されました。",
        url=url,
        color=colors.get(platform, 0xCCCCCC)
    )

    for name, value in fields.items():
        if value:
            embed.add_embed_field(name=name, value=value, inline=False)

    embed.set_footer(text=f"{platform.upper()}監視Botより")
    embed.set_timestamp()
    return embed
