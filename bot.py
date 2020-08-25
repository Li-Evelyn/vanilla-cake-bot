from Files.initialize import *


@bot.event
async def on_ready():
    guild = get(bot.guilds, name=GUILD)
    print(f"{bot.user} is connected to {guild.name} (id: {guild.id})")
    change_status.start()


@tasks.loop(minutes=10)
async def change_status():
    num = random.randint(0, 2)
    selection = random.randint(0, len(statuses[num]) - 1)
    name = statuses[num][selection]
    if num == 0:
        activity = discord.Activity(name=f"{name}", type=discord.ActivityType.watching)
    elif num == 1:
        activity = discord.Game(f"{name}")
    else:
        activity = discord.Activity(name=f"{name}", type=discord.ActivityType.listening)
    await bot.change_presence(activity=activity)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("i don't have enough information :confused: - did you enter all necessary arguments?")
    # TODO: catch more errors


@bot.command(name="rps", help="play classic rock-paper-scissors!")
async def rps(ctx, choice):
    await ctx.send(gaming.rps_classic(choice))


@bot.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        await channel.connect()

    await ctx.send(f"hey! i'm in <#{channel.id}> now! :wave:")


@bot.command(pass_context=True)
async def leave(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await ctx.send("okay, until next time! :wave:")
        await voice.disconnect()
    else:
        await ctx.send("i'm not currently in a voice channel :triumph:")


# TODO: add command to play music (and all other commands that come with it)

@bot.command(name="enter", help="manually add a track to the spreadsheet")
async def manual_entry(ctx, *specific):
    user_message = ctx.message
    if len(specific) < 2:
        await ctx.send("please enter a minimum of a title and an artist :triumph:")
        return

    # TODO: parse <link> formatting
    # if len(specific) >= 3 and specific[2].startswith("<") and specific[2].endswith(">"):
    #     print("hey")
    #     specific[2] = specific[2][1:-1]

    if MUSIC_CHANNEL in user_message.channel.name:
        discriminator = user_message.author.discriminator
        info_list = list(specific)
        info_list.insert(0, f"{discriminator}")
        activity = discord.Activity(name=f"{info_list[1]} by {info_list[2]}", type=discord.ActivityType.listening)
        async with user_message.channel.typing():
            await ctx.send(spreadsheet.update_spreadsheet(info_list))
        await bot.change_presence(activity=activity)
    else:
        await ctx.send("you're not supposed to use this command in this channel :triumph:")


# TODO: add command to rate the most recent sending of a track (params: title, rating)

@bot.event
async def on_message(message):

    activity = None
    discriminator = message.author.discriminator

    if message.author == bot.user:
        return

    if MUSIC_CHANNEL in message.channel.name:
        titles = []
        list_of_links = list(filter(lambda x: (spotify.is_spotify_link(x) or youtube.is_youtube_link(x)),
                                    message.content.strip().split()))
        for link in list_of_links:
            if spotify.is_spotify_link(link):
                info = spotify.echo_info(discriminator, link)
            elif youtube.is_youtube_link(link):
                info = youtube.echo_info(discriminator, link)
            titles.append(f"{info[1]} by {info[2]}")
            async with message.channel.typing():
                await message.channel.send(spreadsheet.update_spreadsheet(info))
        activity = discord.Activity(name=f"{', then '.join(titles)}", type=discord.ActivityType.listening)
    elif message.content.startswith("!rps "):
        activity = discord.Game(f"rock paper scissors with {message.author.display_name}")

    # change status
    if activity:
        await bot.change_presence(activity=activity)

    # print(message.author.activities[0].name)

    # process commands before on_message
    await bot.process_commands(message)

bot.run(TOKEN)
