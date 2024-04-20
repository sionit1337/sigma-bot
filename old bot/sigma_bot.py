import disnake as discord
from disnake.ext import commands

import random

from asyncio import sleep

from psutil import cpu_percent, virtual_memory

from numexpr import evaluate

from googleapiclient.discovery import build

import base64 as b64

import openai
import craiyon

import gtts
import qrcode

import yt_dlp as ytdlp

import json

import sqlite3

with open("config.json", "r", encoding="utf-8") as cfg:
    config = json.load(cfg)


con = sqlite3.connect("database.db")
curs = con.cursor()

curs.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        balance INTEGER NOT NULL DEFAULT 500,
        level INTEGER NOT NULL DEFAULT 0,
        exp INTEGER NOT NULL DEFAULT 0)
    """)

curs.execute("""CREATE TABLE IF NOT EXISTS shop (
    item_id INTEGER PRIMARY KEY,
    description TEXT NOT NULL,
    price INTEGER NOT NULL)
    """)

con.commit()
con.close()


openai.api_key = config["OpenAI_Key"]

intents = discord.Intents.all()

bot = commands.InteractionBot(intents=intents)

Red = 0xff0000

Green = 0x00ff00

Yellow = 0xffbb00

Blocklist = [999692841498451988]


def get_ai_response(ai_prompt: str):
    with open("gpt_history.txt", "r", encoding="utf-8") as history:
        history_content = history.read()

    if len(history_content) >= 4097:
        with open("gpt_history.txt", "w", encoding="utf-8") as history:
            history.write("")

            return "История была очищена"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Ты Sigma Bot, был создан sionit_1337. Ты находишься на дискорд-сервере 『Σ』Syndicate Sigma и общаешься исключительно на русском"},
            {"role": "system", "content": history_content},
            {"role": "user", "content": ai_prompt}
        ],
        n=1,
        max_tokens=999,
        temperature=.7
    )

    with open("gpt_history.txt", "a", encoding="utf-8") as history:
        history.write(f"{ai_prompt} \n{str(response.choices[0].message.content)} \n")

    return str(response.choices[0].message.content)


async def random_ping():
    guild = bot.get_guild(983767050302398514)
    channel = bot.get_channel(1146345841997656064)
    role = guild.get_role(1144206523879411803)

    while True:
        await sleep(random.randint(60, 14400))
        await channel.send(f"{role.mention}")

        print("Бот выполнил рандомный пинг")


@bot.event
async def on_ready():
    channel = bot.get_channel(1153915482445991937)

    print(f"{bot.user} готов к работе!")
    await channel.send(embed=discord.Embed(title="Бот запущен!", color=Green))

    motd = ["???", "зафлуди сиониту консоль", "Minecraft", "догони меня кирпич", "Bag Generator 3000"]
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.playing, name=random.choice(motd)))

    bot.loop.create_task(random_ping())


@bot.event
async def on_member_join(member):
    server = bot.get_guild(983767050302398514)
    channel = server.get_channel(1140674136390254652)

    await channel.send(embed=discord.Embed(title="Новый участник", description=f"К нам зашел {member.mention}! Поприветствуйте его!", color=Green))


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.author.id in Blocklist:
        return

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    amnt = random.randint(1, 5)
    user_id = message.author.id

    cursor.execute("SELECT level, exp FROM users WHERE user_id = ?", (user_id,))

    user_data = cursor.fetchone()

    if user_data:
        user_level = user_data[0]
        user_exp = user_data[1]

        randomizator = random.randint(1, 3)
        if randomizator == 3:
            cursor.execute("UPDATE users SET exp = exp + ? WHERE user_id = ?", (amnt, user_id))

        if int(user_exp) >= (int(user_level) * 10):
            cursor.execute("UPDATE users SET level = level + 1 WHERE user_id = ?", (user_id,))
            cursor.execute("UPDATE users SET exp = 0 WHERE user_id = ?", (user_id,))

            lvl_up_channel = bot.get_channel(1140893934202134588)
            await lvl_up_channel.send(embed=discord.Embed(title="Повышение уровня", description=f"<@{user_id}> повысил свой уровень до {user_level + 1}!", color=Green))

    conn.commit()
    conn.close()

    if message.content.startswith(f"{bot.user.mention} "):
        content = message.content.removeprefix(f"{bot.user.mention} ")

        response_msg = await message.channel.send(embed=discord.Embed(title="ChatGPT думает...", color=Yellow))

        response = get_ai_response(ai_prompt=content)

        print(f"{len(response)} \n{content} \n{response}")

        if content.lower() == "очистить":
            with open("gpt_history.txt", "w", encoding="utf-8") as history:
                history.write("")

            await response_msg.edit(embed=discord.Embed(title="История сообщений была очищена", color=Yellow))

        else:
            if len(response) < 2000:
                await response_msg.edit(embed=discord.Embed(title="Результат:", description=f"{response}", color=Green))

            else:
                with open("response.txt", "w", encoding="utf-8") as file:
                    file.write(response)

                file = discord.File("response.txt", filename="answer.txt")

                await response_msg.edit(embed=discord.Embed(title="Ошибка", description=f"Ответ превышает максимально допустимый размер сообщений ({len(response)}/2000), поэтому я его отправил в виде файла.", color=Red), file=file)


@bot.slash_command(name="хост", description="Пишет статы хоста бота")
async def host(ctx):
    if ctx.author.id in Blocklist:
        return

    cpu = cpu_percent()

    ram_percent = virtual_memory().percent
    ram_used = round(virtual_memory().used / 1048576)
    ram_total = round(virtual_memory().total / 1048576)

    await ctx.send(embed=discord.Embed(title="Нагрузка хоста",
                                       description=f"Пинг: ``{round(bot.latency * 1000)} мс`` \nЦП: ``{cpu}%`` \nОперативная память: ``{ram_percent}% ({ram_used}/{ram_total} мб)``",
                                       color=Yellow))

    print("Кто-то прописал /хост")


@bot.slash_command(name="инфо", description="Пишет информацию о боте")
async def info(ctx):
    if ctx.author.id in Blocklist:
        return

    guild = bot.get_guild(983767050302398514)
    member_count = guild.member_count

    await ctx.send(embed=discord.Embed(title="Обо мне",
                                       description=f"Я бот {bot.owner.display_name} (или {bot.owner.name}), сделан для сервера 『Σ』Syndicate Sigma на языке Python, библиотека Disnake. Поддерживаю слэш-команды \nВсего участников на сервере: {member_count}",
                                       color=Yellow))

    print("Кто-то прописал /инфо")


@bot.slash_command(name="репорт", description="Отправляет сообщение о баге в отдельный канал")
async def bug(ctx, описание: str, скрин_бага: discord.Attachment):
    if ctx.author.id in Blocklist:
        return

    channel = bot.get_channel(1145040647481479261)

    embed = discord.Embed(title="", description=f"{описание}", color=Yellow)
    embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar.url}")
    embed.set_image(url=скрин_бага.url)

    await ctx.send(embed=discord.Embed(title="Успешно", description="Баг репорт отправлен!", color=Green))
    await channel.send(embed=embed)

    print(f"Зарепортили баг \nОписание: {описание} \nURL скриншота: {скрин_бага.url}")


@bot.slash_command(name="спросить", description="Отвечает на заданный вопрос \"да\", \"нет\" или другое")
async def ask(ctx, вопрос: str):
    if ctx.author.id in Blocklist:
        return

    answers = ["Да", "Нет", "НИ В КОЕМ СЛУЧАЕ!!!!!", "КОНЕЧНО ЖЕ ДА!!!!!!!!!", "Не уверен", "Скорее всего нет",
               "Возможно", "Спроси у ChatGPT", "Спроси у другого бота", "Мне лень, переспроси еще раз"]

    answer = random.choice(answers)

    await ctx.send(
        embed=discord.Embed(title="Спросили", description=f"Вопрос: ``{вопрос}`` \nОтвет: ``{answer}``", color=Green))

    print(f"Спросили \nВопрос: {вопрос} \nОтвет: {answer}")


@bot.slash_command(name="канобу", description="Игра \"Камень-Ножницы-Бумага\"")
async def kanobu(ctx, выбор: str = commands.Param(choices=["камень", "ножницы", "бумага"])):
    if ctx.author.id in Blocklist:
        return

    bot_choices = ["камень", "ножницы", "бумага"]

    bot_choice = random.choice(bot_choices)

    if выбор.lower() == bot_choice.lower():
        await ctx.send(
            embed=discord.Embed(title="Ничья!", description=f"Я выбрал ``{bot_choice}`` \nВы выбрали ``{выбор}``",
                                color=Yellow))

    elif ((выбор.lower() == "бумага" and bot_choice.lower() == "камень") or (
            выбор.lower() == "ножницы" and bot_choice.lower() == "бумага") or (
                  выбор.lower() == "камень" and bot_choice.lower() == "ножницы")):
        await ctx.send(
            embed=discord.Embed(title="Вы выиграли!", description=f"Я выбрал ``{bot_choice}`` \nВы выбрали ``{выбор}``",
                                color=Green))

    else:
        await ctx.send(embed=discord.Embed(title="Вы проиграли!",
                                           description=f"Я выбрал ``{bot_choice}`` \nВы выбрали ``{выбор}``",
                                           color=Red))

    print(f"Бот сыграл в КаНоБу \nИгрок выбрал {выбор}, бот выбрал {bot_choice}")


@bot.slash_command(name="выбор", description="Выбирает из двух вариантов")
async def choice(ctx, вариант_1, вариант_2):
    if ctx.author.id in Blocklist:
        return

    final_choice = random.randint(1, 3)

    if final_choice == 1:
        await ctx.send(
            embed=discord.Embed(title="Выбираю первый вариант", description=f"Вариант: ``{вариант_1}``", color=Green))

    elif final_choice == 2:
        await ctx.send(
            embed=discord.Embed(title="Выбираю второй вариант", description=f"Вариант: ``{вариант_2}``", color=Red))

    else:
        await ctx.send(embed=discord.Embed(title="Тут без понятия, выбирай по ситуации", color=Yellow))

    print(f"Бот выбрал: {final_choice}")


@bot.slash_command(name="рулетка", description="Русская рулетка")
async def roulette(ctx, пули: int):
    if ctx.author.id in Blocklist:
        return

    chance = random.randint(1, 6)

    if пули > 6 or пули <= 0:
        await ctx.send(embed=discord.Embed(title="Неправильное количество пуль!", color=Yellow))

    else:
        if chance < пули:
            await ctx.send(embed=discord.Embed(title="Пистолет выстрелил и вы умерли",
                                               description=f"Пуль было заряжено: ``{пули}``", color=Red))

        else:
            await ctx.send(embed=discord.Embed(title="Выстрела не произошло и вы выжили!",
                                               description=f"Пуль было заряжено: ``{пули}``", color=Green))

    print(f"Бот сыграл в рулетку, пуль было {пули}, шанс {chance} из {пули}")


@bot.slash_command(name="калькулятор", description="Вычисляет заданный пример")
async def calc(ctx, пример):
    if ctx.author.id in Blocklist:
        return

    result = evaluate(пример)

    await ctx.send(embed=discord.Embed(title=f"Результат: ``{result}``", color=Yellow))

    print(f"Бот вычислил пример и получил {result}")


@bot.slash_command(name="аватарка", description="Получает аватарку выбранного пользователя")
async def avatar(ctx, пользователь: discord.Member):
    if ctx.author.id in Blocklist:
        return

    embed = discord.Embed(title=f"Аватарка пользователя {пользователь.display_name}", color=Yellow)
    embed.set_image(url=пользователь.avatar.url)

    await ctx.send(embed=embed)

    print(f"Бот получил аватарку пользователя {пользователь.display_name}: {пользователь.avatar.url}")


@bot.slash_command(name="гугл-картинка", description="Присылает картинку по запросу в Google")
async def googlimage(ctx, запрос: str):
    if ctx.author.id in Blocklist:
        return

    await ctx.send(embed=discord.Embed(title=f"Идет поиск по запросу ``{запрос}``...", color=Yellow))

    resource = build("customsearch", "v1", developerKey=config["Google_CS_Key"]).cse()
    result = resource.list(q=f"{запрос}", cx=config["Google_PS_Key"], searchType="image", safe="active").execute()
    ran = random.randint(0, (len(result["items"]) - 1))

    if "items" in result and len(result["items"]) > 0:
        final_url = result["items"][ran]["link"]

        embed = discord.Embed(title=f"{запрос}", description=final_url, url=final_url, color=Green)
        embed.set_image(url=final_url)

        await ctx.send(embed=embed)

    else:
        await ctx.send(embed=discord.Embed(title="Не удалось ничего найти по вашему запросу.", color=Red))

    print(f"Бот нашел {final_url} по запросу {запрос}")


@bot.slash_command(name="гугл-ссылка", description="Отправляет ссылку по запросу в Google")
async def googlink(ctx, запрос: str):
    if ctx.author.id in Blocklist:
        return

    await ctx.send(embed=discord.Embed(title=f"Идет поиск по запросу ``{запрос}``...", color=Yellow))

    resource = build("customsearch", "v1", developerKey=config["Google_cS_Key"]).cse()
    result = resource.list(q=f"{запрос}", cx=config["Google_PS_Key"], searchType="searchTypeUndefined",
                           safe="active").execute()
    ran = random.randint(0, (len(result["items"]) - 1))

    if "items" in result and len(result["items"]) > 0:
        final_url = result["items"][ran]["link"]

        embed = discord.Embed(title=f"{запрос}", description=final_url, url=final_url, color=Green)

        await ctx.send(embed=embed)

    else:
        await ctx.send(embed=discord.Embed(title="Не удалось ничего найти по вашему запросу.", color=Red))

    print(f"Бот нашел {final_url} по запросу {запрос}")


@bot.slash_command(name="сгенерировать", description="Генерирует картинку по запросу")
async def genimage(ctx, запрос: str):
    if ctx.author.id in Blocklist:
        return

    generator = craiyon.Craiyon()

    await ctx.send(embed=discord.Embed(title=f"Генерируется картинка по запросу ``{запрос}``...", color=Yellow))

    result = await generator.async_generate(prompt=запрос)
    final_image = random.choice(result.images)

    embed = discord.Embed(title=f"{запрос}")
    embed.set_image(url=final_image)

    await ctx.send(embed=embed)

    print(f"Бот сгенерировал {final_image}")


@bot.slash_command(name="base64", description="Работает с кодировкой Base64")
async def base64(ctx, ввод: str, тип: str = commands.Param(choices=["декодировать", "закодировать"])):
    if ctx.author.id in Blocklist:
        return

    if тип == "декодировать":
        decoded_bytes = b64.b64decode(ввод.encode("utf-8"))
        decoded_text = decoded_bytes.decode("utf-8")

        await ctx.send(embed=discord.Embed(title=f"Декодированный текст: ``{decoded_text}``", color=Yellow))

        print(ввод, decoded_text)

    elif тип == "закодировать":
        encoded_bytes = b64.b64encode(ввод.encode("utf-8"))
        encoded_text = encoded_bytes.decode("utf-8")

        await ctx.send(embed=discord.Embed(title=f"Закодированный текст: ``{encoded_text}``", color=Yellow))

        print(ввод, encoded_text)


@bot.slash_command(name="озвучить", description="Озвучивает введенный текст")
async def tts(ctx, текст: str):
    if ctx.author.id in Blocklist:
        return

    await ctx.send(embed=discord.Embed(title="Подождите, идет озвучка...", color=Yellow))

    voice = gtts.gTTS(текст, lang="ru")
    voice.save("voice_message.ogg")

    await ctx.send(file=discord.File("voice_message.ogg"))

    print(f"Бот озвучил текст \nТекст: \n{текст}")


@bot.slash_command(name="qr-код", description="Превращает ссылку в QR-код")
async def qr(ctx, текст: str):
    if ctx.author.id in Blocklist:
        return

    await ctx.send(embed=discord.Embed(title="Подождите, идет создание QR-кода...", color=Yellow))

    img = qrcode.make(текст)
    img.save("qrcode.png")
    final_qr_code = discord.File("qrcode.png")

    embed = discord.Embed(title="Готово", description=f"{текст}", color=Green)
    embed.set_image(file=final_qr_code)

    await ctx.send(embed=embed)

    print(f"Бот сделал QR-код \nТекст: {текст}")


@bot.slash_command()
async def execute(ctx, command: str):
    if ctx.author != bot.owner:
        return

    try:
        await eval(command)

    except Exception as e:
        await ctx.send(embed=discord.Embed(title="Ошибка!", description=f"``{e}``", color=Red))


# Музыка
@bot.slash_command(name="присоединить", description="Присоединяет бота к вашему голосовому чату")
async def join(ctx):
    if ctx.author.id in Blocklist:
        return

    channel = ctx.author.voice.channel
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        voice.move_to(channel)

        await ctx.send(embed=discord.Embed(title="Бот успешно присоединился к голосовому каналу!", color=Green))

    elif voice == channel:
        await ctx.send(embed=discord.Embed(title="Бот уже находится в вашем голосовом канале!", color=Yellow))

    else:
        voice = await channel.connect()

        await ctx.send(embed=discord.Embed(title="Бот успешно присоединился к голосовому каналу!", color=Green))

        print(f"Бота присоединили к каналу {voice}")


@bot.slash_command(name="играть", description="Играет музыку (ссылка)")
async def play(ctx, ссылка: str):
    if ctx.author.id in Blocklist:
        return

    YDL_OPTIONS = {"format": "bestaudio", "noplaylist": "True"}
    FFMPEG_OPTIONS = {"before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", "options": "-vn"}

    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    channel = ctx.author.voice.channel

    if not voice:
        voice = await channel.connect()

    elif voice and voice.is_connected():
        voice.move_to(channel)

    if voice and not voice.is_playing():
        await ctx.send(embed=discord.Embed(title="Начинаю проигрывание...", color=Yellow))
        try:
            with ytdlp.YoutubeDL(YDL_OPTIONS) as ydl:
                INFO = ydl.extract_info(ссылка, download=False)

            URL = INFO["url"]
            voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
            voice.is_playing()

            await ctx.send(
                embed=discord.Embed(title="Готово!", description=f"Сейчас играет: [Песня]({ссылка})", color=Green))

        except Exception as e:
            await ctx.send(embed=discord.Embed(title="Что-то пошло не так!", description=f"Подробнее: ``{e}``"))

        print(f"Бот начал играть {ссылка}")


@bot.slash_command(name="скип", description="пропускает текущую музыку")
async def skip(ctx):
    if ctx.author.id in Blocklist:
        return

    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        voice.stop()

        await ctx.send(embed=discord.Embed(title="Текущая музыка пропущена!", color=Green))

    else:
        await ctx.send(embed=discord.Embed(title="Бот не играет музыку в текущий момент!", color=Yellow))

    print("Бот скипнул музыку")


@bot.slash_command(name="пауза", description="Приостанавливает текущую музыку")
async def pause(ctx):
    if ctx.author.id in Blocklist:
        return

    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        voice.pause()

        await ctx.send(embed=discord.Embed(title="Бот успешно остановил проигрывание!", color=Green))

    else:
        await ctx.send(embed=discord.Embed(title="Бот не играет музыку в текущий момент!", color=Yellow))

    print("Бот остановил проигрывание")


@bot.slash_command(name="стоп", description="Останавливает текущую музыку и кикает бота из чата")
async def stop(ctx):
    if ctx.author.id in Blocklist:
        return

    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        voice.pause()
        await voice.disconnect()

        await ctx.send(embed=discord.Embed(title="Бот успешно вышел из голосового чата!", color=Green))

    else:
        await ctx.send(embed=discord.Embed(title="Бот не находится в голосовом чате в текущий момент!", color=Yellow))

    print("Бот вышел из голосового канала")


@bot.slash_command(name="регистрация", description="Регистрирует вас в ДБ с экономикой и уровнями")
async def reg(ctx):
    if ctx.author.id in Blocklist:
        return

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE user_id = ?", (ctx.author.id,))
    existing_user = cursor.fetchone()

    if existing_user:
        await ctx.send(embed=discord.Embed(title="Вы уже зарегистрированы в ДБ!", color=Red))

    else:
        cursor.execute("INSERT INTO users (user_id, balance, level, exp) VALUES (?, 500, 0, 0)", (ctx.author.id,))
        conn.commit()

        await ctx.send(embed=discord.Embed(title="Вы зарегистрированы в ДБ!", description="Ваш начальный баланс - 500<:coin:1231332348487012454>", color=Green))


@bot.slash_command(name="работа", description="Способ заработать немного денег")
@commands.cooldown(1, 3600, commands.BucketType.user)
async def work(ctx):
    if ctx.author.id in Blocklist:
        return

    user_id = ctx.author.id
    amnt = random.randint(50, 250)

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amnt, user_id))
    conn.commit()
    conn.close()

    await ctx.send(embed=discord.Embed(title=f"Вы поработали и получили {amnt}<:coin:1231332348487012454>!", color=Green))


@bot.slash_command(name="профиль", description="Показывает профиль выбранного пользователя")
async def profile(ctx, пользователь: discord.Member = None):
    if ctx.author.id in Blocklist:
        return

    if пользователь is None:
        пользователь = ctx.author

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE user_id = ?", (пользователь.id,))
    existing_user = cursor.fetchone()

    if existing_user:
        cursor.execute("SELECT balance, level, exp FROM users WHERE user_id = ?", (пользователь.id,))
        user_info = cursor.fetchone()
        user_balance = user_info[0]
        user_level = user_info[1]
        user_exp = user_info[2]

        conn.close()

        if user_info:
            await ctx.send(embed=discord.Embed(title=f"Пользователь {пользователь.name}", description=f"Баланс: {user_balance}<:coin:1231332348487012454> \nУровень: {user_level} \nОпыт: {user_exp}/{user_level * 10}", color=Yellow))

    else:
        await ctx.send(embed=discord.Embed(title="Пользователя нет в ДБ!", color=Red))


@bot.slash_command(name="передать", description="Передает выбранному пользователю деньги")
async def transfer(ctx, пользователь: discord.Member, количество: int):
    if ctx.author.id in Blocklist:
        return

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (ctx.author.id,))
    user_info = cursor.fetchone()
    user_balance = user_info[0]

    cursor.execute("SELECT * FROM users WHERE user_id = ?", (пользователь.id,))
    existing_user = cursor.fetchone()

    if existing_user:
        if количество <= user_balance:
            cursor.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (количество, пользователь.id))
            cursor.execute("UPDATE users SET balance = balance - ? WHERE user_id = ?", (количество, ctx.author.id))

            await ctx.send(embed=discord.Embed(title=f"Вы передали {пользователь.name} {количество}<:coin:1231332348487012454>", color=Green))

        else:
            await ctx.send(embed=discord.Embed(title="У вас недостаточно <:coin:1231332348487012454> для передачи!", color=Red))

    else:
        await ctx.send(embed=discord.Embed(title="Пользователя нет в ДБ!", color=Red))

    conn.commit()
    conn.close()

    print(f"Пользователь {ctx.author.name} перекинул {пользователь.name} {количество} монет")


password = input("Запустить бота? (y/n) \n>>> ")

if password.lower() == "y":
    print("Принято, запускаю...")

    bot.run(config["Token"])

else:
    print("Принято, откат")
