import discord
import pyowm
import asyncio
import random
import json
import os
import random as r
from discord.ext import commands
from discord import Embed

PREFIX = '/'

client = commands.Bot( command_prefix = PREFIX )
client.remove_command( 'help' )
# .say

@client.event 
async def on_ready():
	print( 'BOT connected' )
	await client.change_presence( status = discord.Status.online, activity = discord.Game( 'SecretCrew' ) )

@client.command()
async def say(ctx, *, arg):
    author = ctx.message.author
    await ctx.send( f'{arg}')

@client.command()
@commands.has_any_role( 679793624921538780, 561535200639713330, 692474167160864769  )
async def saya(ctx, *, arg):
    await ctx.message.delete()
    author = ctx.message.author
    await ctx.send( f'{arg}')
 

# Kick
@client.command()
@commands.has_any_role( 679793624921538780, 561535200639713330, 692474167160864769, 672845763545399318  )
async def kick(ctx,member: discord.Member = None, reason = None): 

    if member is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))

    elif reason is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: причину!**'))

    else:

        channel_log = client.get_channel(687158028348293121) #Айди канала логов

        await member.kick( reason = reason )
        await ctx.send(embed = discord.Embed(description = f'**:shield: Пользователь {member.mention} был исключен.\n:book: По причине: {reason}**', color=0xfa0105))
        await asyncio.sleep(10)
        await ctx.channel.purge(limit=1)
        await channel_log.send(embed = discord.Embed(description = f'**:shield: Пользователь {member.mention} был выгнан.\n:book: По причине: {reason}**', color=0xfa0105,timestamp=ctx.message.created_at)) 



# Ban
@client.command()
@commands.has_any_role( 679793624921538780, 561535200639713330, 692474167160864769, 672845763545399318  )
async def ban(ctx,member: discord.Member = None, reason = None): 

    if member is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))

    elif reason is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: причину!**'))

    else:
        
        channel_log = client.get_channel(687158028348293121) #Айди канала логов

        await member.ban( reason = reason )
        await ctx.send(embed = discord.Embed(description = f'**:shield: Пользователь {member.mention} был заблокирован.\n:book: По причине: {reason}**', color=0xfa0105)) 
        await asyncio.sleep(10)
        await ctx.channel.purge(limit=1)
        await channel_log.send(embed = discord.Embed(description = f'**:shield: Пользователь {member.mention} был заблокирован.\n:book: По причине: {reason}**', color=0xfa0105,timestamp=ctx.message.created_at)) 


# Clear chat
@client.command()
@commands.has_any_role( 679793624921538780, 561535200639713330, 692474167160864769, 672845763545399318, 679503121126654017  ) #1-призрак, 2-админ, 3-модер, 4-смотрящий
async def clear(ctx,amount : int):
    
    channel_log = client.get_channel(687158028348293121) #Айди канала логов

    await ctx.channel.purge( limit = amount )
    await ctx.send(embed = discord.Embed(description = f'**:heavy_check_mark: Удалено {amount} сообщений.**', color=0xc9761d))
    await asyncio.sleep(5)
    await ctx.channel.purge(limit=1)
    emb = discord.Embed(description=f'**:wastebasket:  Удалено {amount} сообщений.**', color=0xc9761d,timestamp=ctx.message.created_at)
    emb.set_footer(text='Очистил: {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
    await channel_log.send(embed=emb)



# Help
@client.command()
@commands.has_any_role( 679793624921538780, 561535200639713330, 692474167160864769, 672845763545399318, 679503121126654017  )
async def helpa( ctx ):
	await ctx.message.delete() # - удаляет команду
	emb = discord.Embed( title = 'Навигация по командам <3' )
	emb.add_field( name = 'Очистка', value = 'Команда для очистки чата, пример искользования ```/clear 2```' )
	emb.add_field( name = f'{PREFIX}Бан', value = 'Команда для бана участника на сервере, пример использования ```/ban @user <причина>```' )
	emb.add_field( name = f'{PREFIX}Кик', value = 'Команда с помощью которой можно выгнать участника с сервера, пример использования ```/kick @user```' )
	emb.add_field( name = f'{PREFIX}Помощь', value = 'Помощь по командам сервера' )
	await ctx.send( embed = emb )

# Error
@kick.error 
async def kick_error(ctx, error):

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name}, стоп, стоп, стоп! У вас недостаточно прав для использования данной команды!**', color=0xd4bd18))


#---
@ban.error 
async def ban_error(ctx, error):

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name}, стоп, стоп, стоп! У вас недостаточно прав для использования данной команды!**', color=0xd4bd18)) 


#---
@clear.error 
async def clear_error(ctx, error):

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name}, стоп, стоп, стоп! У вас недостаточно прав для использования данной команды!**', color=0xd4bd18))

    if isinstance( error, commands.MissingRequiredArgument  ): 
        await ctx.send(embed = discord.Embed(description = f'**:grey_exclamation: {ctx.author.name}, обязательно укажите количевство сообщений.**', color=0xc9761d)) 


# Работа с несуществующими командами

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound ):
        await asyncio.sleep(5)
        await ctx.channel.purge(limit=1) 
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name}, ошибочка... такой команды нет на сервере.**', color=0xc56202))
        await asyncio.sleep(5)
        await ctx.channel.purge(limit=1) 

#info 

@client.command()
async def info(ctx):
    await ctx.message.delete()
    embed=discord.Embed(title="**Информация о SecretCrew**", description="**SecretCrew** предназначен - для: \n ***общения, развлечения, знакомств, фильмов, игр, музыки*** **и многого многого другого.** \n На сервере есть система ***__Жалоб__*** чтобы узнать подробнее, напишите в чат ``/help`` \n И бот вам обязательно ответит! \n **Главные администраторы сервера показаны ниже -** \n <@519558988304482304>, \n <@512971928471076864>, \n <@497155059772293151>.", color=0xbbd3e0 )

    embed.set_footer( text = "SecretCrew! BOT", icon_url = client.user.avatar_url )
    #embed.set_author(name="Stishok")
    await ctx.author.send(embed=embed)

# Вход
@client.event
async def on_member_join(member):
  embed = discord.Embed(title="**Привет! Я очень рад тебя видеть на сервере** ***__SecretCrew!__***", description="Надеюсь тебе тут понравится! \n Для того чтобы ***__не много__*** ознакомится с сервером, напиши в чат ``/info``, я тебе автоматически отвечу! \n Ну и обязательно прочитай ***<#680092681040298033>*** нашего сервера во избежании нарушения **__Правил__** \n ***Приятного времяпровождения <3***", color=0xbbd3e0)
  await member.send(embed=embed)





# Helpmee

info_b = ['информация про сервер', 'информация', 'что за сервер?', 'информация?']

oos_s = ['кто администратор?', 'кто основатель?', 'кто создатель?', 'кто администраторы?', 'кто администрация?', 'кто админ?']

partners = ['партнерство?', 'может быть партнёрство?', 'партнёрство?', 'что насчёт партнерства?']

eco_s = ['экономика', 'работа']


@client.event

async def on_message(message):
	await client.process_commands(message)
	msg = message.content.lower()

	if msg in eco_s:
		await message.author.send('**Обязательно вводить команды в канале** <#680015762286575633> \n Для того чтобы узнать список работ, введите команду ``!worklist`` \n Для того чтобы пойти на выбранную вами работу, команда ``!work Работа`` \n Для того чтобы посмотреть список ролей в магазине, команда ``!shop`` \n Для того чтобы купить понравившиюся роль в магазине, команда ``!buy @Role`` \n Чтобы испытать свою удачу, команда ``!br 1 (сумма)`` или же ``!betroll 1``.')

	if msg in info_b:
		await message.author.send('**Чтобы ознакомится с сервером, пропиши -** ``/info``')

	if msg in partners:
		await message.author.send('**По поводу партнёрства, можно обратится в к администрации сервера. Исключительно в личные сообщения!**')

	if msg in oos_s:
		await message.author.send('**Администрация сервера SecretCrew -** \n <@512971928471076864>, \n <@519558988304482304>, \n <@497155059772293151>.')
		


#embed = discord.Embed(description="Администрация данного сервера -** \n <@512971928471076864>, \n <@519558988304482304>, \n <@497155059772293151>", color=0x02130)
		#await member.send(embed=embed)

# Команды кстом
@client.command()
@commands.has_any_role( 682312156687237187  )

async def neews( ctx ):

	await ctx.message.delete() # - удаляет команду

	emb = discord.Embed( title="**Основные новости сервера!**", description="@everyone \n Дорогие участники **SecretCrew!** \n Перейдём сразу к новостям - Актив на сервере сильно упал, администрация искренне просит извенения перед вами! \n Мы понимаем, то что на сервере чего-то не хватает, но вопрос именно для вас.. \n Что именно не хватает серверу для хорошего и более менее стабильного актива!? \n Ваши предложиния ждём в канале <#561530003859308554> ! \n Будем рассматривать каждое предложение, и с большой вероятностью его одобрим. \n **Так же** \n У нас сейчас работает лишь один администратор, но ему одному трудно \n Вообщем я вас спросил, жду ваших **__креативныx__** идей! \n \n Желаю всем удачи!", color=0xfa0105 )
	await ctx.send( embed = emb )
#await ctx.send(embed=emb, delete_after=10)- удаляет сообщния бота

# userinfo
@client.command()
async def userinfo(ctx, Member: discord.Member = None ):
    if not Member:
        Member = ctx.author
    roles = (role for role in Member.roles )
    emb = discord.Embed(title='Информация о пользователе.{}'.format(Member.name), description=f"Участник зашёл на сервер: {Member.joined_at.strftime('%b %#d, %Y')}\n\n "
                                                                                      f"Имя: {Member.name}\n\n"
                                                                                      f"Никнейм: {Member.nick}\n\n"
                                                                                      f"Статус:  {Member.status}\n\n"
                                                                                      f"ID: {Member.id}\n\n"
                                                                                      f"Высшая роль: {Member.top_role}\n\n"
                                                                                      f"Аккаунт создан: {Member.created_at.strftime('%b %#d, %Y')}", 
                                                                                      color=0xff0000, timestamp=ctx.message.created_at)

    emb.set_thumbnail(url= Member.avatar_url)
    emb.set_footer(icon_url= Member.avatar_url)
    emb.set_footer(text='Спросил: {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
    await ctx.send(embed=emb)

# Servinfo
@client.command()
async def serverinfo(ctx, member: discord.Member = None):
    if not member:
        member = ctx.author

    guild = ctx.guild
    embed = discord.Embed(title=f"{guild.name}", description=f"Сервер создали {guild.created_at.strftime('%b %#d, %Y')}\n\n"
                                                             f"Регион {guild.region}\n\nГлава сервера {guild.owner}\n\n"
                                                             f"Людей на сервере {guild.member_count}\n\n",  color=0xff0000,timestamp=ctx.message.created_at)

    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text=f"ID: {guild.id}")

    embed.set_footer(text=f"ID Пользователя: {ctx.author.id}")
    await ctx.author.send(embed=embed)


# Репорт

@client.command()
async def report(ctx,member: discord.Member = None,*,arg = None):
    channel = client.get_channel(695368571429191891) #Айди канала жалоб await ctx.author.send(embed=embed)

    if member is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))

    elif arg is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: причину!**'))

    else:

        await ctx.send(embed = discord.Embed(description =f'**:shield: На пользователя {member.mention} была отправлена жалоба.\n:bookmark_tabs: По причине: {arg}**', color=0x355ddf))
        await channel.send(embed = discord.Embed(description =f'**:shield: На пользователя {member.mention} была отправлена жалоба.\n:bookmark_tabs: По причине: {arg}\n:bust_in_silhouette: Автор жалобы: {ctx.author.mention}**', color=0x355ddf,timestamp=ctx.message.created_at))
        emb.set_footer(icon_url= Member.avatar_url)
        emb.set_footer(text='Подал: {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
        await ctx.send(embed=emb)

# Шар

@client.command(aliases = ["8ball"])
async def sc(ctx, *, arg):

    message = ['Ежжии, Джан, переспроси вопросик', 'Канешнааа (нет)', 'Слушай, я врать не буду, думаю что Да', 'Можешь не сомневатся!', 'Думаю не стоит'] 
    s = random.choice( message )
    await ctx.send(embed = discord.Embed(description = f'**:crystal_ball: На заборах написано:** {s}', color=0x7a14a7))
    return

# Работа с ошибками шара

@sc.error 
async def sc_error(ctx, error):

    if isinstance( error, commands.MissingRequiredArgument ): 
        await ctx.send(embed = discord.Embed(description = f'Пожалуйста, укажите сообщение.', color=0x7a14a7))  


#helpa
@client.command()
async def help( ctx ):
    await ctx.message.delete() # - удаляет команду
    emb = discord.Embed( title = 'Навигация по командам SecretCrew', color=0x2b7ad8 )
    emb.add_field( name = 'Знаток', value = 'Команда для решения вопроса. Пример - ``/sc Я сэкс символ?``' )
    emb.add_field( name = 'Жалоба', value = 'Команда для того чтобы пожаловаться на пользователя. Пример - ``/report @User Причина``' )
    emb.add_field( name = 'Сказать ботом', value = 'Команда с помощью которой вы сможете написать текст, но он будет написан ботом, пример использования ``/say Текст``' )
    emb.add_field( name = 'Информация', value = 'Так же вы можете узнать небольшую информацию про сервер. Напишите в чат ``/info`` и бот вам автоматически ответит!' )
    emb.add_field( name = 'О себе и не только', value = 'Вы можете узнать информацию о себе или о каком-либо из пользователей. Прописав команду ``/userinfo``. Или написав команду ``/serverinfo`` Будет небольшая информация про сервер')
    emb.add_field( name = 'Экономика', value = 'Чтобы посмотреть команды для заработка, покупки роли и дополнительной информации касаемо ***__Экономике__***, \n Введите в чат слово **"Экономика"**')
    await ctx.author.send(embed=emb)

#ping









# Token

token = os.environ.get('BOT_TOKEN')

# 2d2f33 - темный цвет тона

# embed.set_footer( text = "Собственность сервера VERSE!", icon_url = client.user.avatar_url ) - снизу написАНА