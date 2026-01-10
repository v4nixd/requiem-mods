from disnake import (
    VoiceChannel,
    StageChannel,
    TextChannel,
    CategoryChannel,
    ForumChannel,
    MediaChannel,
)

type DiscordChannel = (
    VoiceChannel
    | StageChannel
    | TextChannel
    | CategoryChannel
    | ForumChannel
    | MediaChannel
)
