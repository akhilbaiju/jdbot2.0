from pyrogram import filters, Client, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from bot import Translation # pylint: disable=import-error
from bot.database import Database # pylint: disable=import-error
from presets import Presets
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from bot.plugins.custfilter import insertid
import asyncio
from datetime import date
db = Database()

@Client.on_message(filters.command(["start"]) & filters.private, group=1)
async def start(bot, update):
    name=update.from_user.first_name
    insertid(int(update.chat.id))
    try:
        file_uid = update.command[1]
    except IndexError:
        file_uid = False
    
    if file_uid:
        file_id, file_name, file_caption, file_type = await db.get_file(file_uid)
        
        if (file_id or file_type) == None:
            return
        caption = file_caption if file_caption != ("" or None) else ("<code>" + file_name + "</code>")
        update_channel = "honeybeemovies"
        user_id = update.from_user.id
        if update_channel :
            try:
                await bot.get_chat_member(update_channel, user_id)
                if file_type == "document":        
                    await bot.send_document(
                        chat_id=update.chat.id,
                        document = file_id,
                        caption = "<b><i>"+caption+" </i></b>",
                        parse_mode=enums.ParseMode.HTML,
                        reply_to_message_id=update.id,
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton
                                        (
                                            '👉🏻 Click to Join Channel 👈🏻', url="https://t.me/honeybeemovies"
                                        )
                                ]
                            ]
                        )
                    )

                elif file_type == "video":
                    await bot.send_video(
                        chat_id=update.chat.id,
                        video = file_id,
                        caption = caption,
                        parse_mode=enums.ParseMode.HTML,
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton
                                        (
                                            '👉🏻 Click to Join Channel 👈🏻', url="https://t.me/honeybeemovies"
                                        )
                                ]
                            ]
                        )
                    )
            
                elif file_type == "audio":
                    await bot.send_audio(
                        chat_id=update.chat.id,
                        audio = file_id,
                        caption = caption,
                        parse_mode=enums.ParseMode.HTML,
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton
                                        (
                                            '👉🏻 Click to Join Channel 👈🏻', url="https://t.me/honeybeemovies"
                                        )
                                ]
                            ]
                        )
                    )

                else:
                    print(file_type)
                return
            except UserNotParticipant:
                await update.reply_text(f'Hey {name} !. You are not Joined on Honey bee movies. Please Join Honey Bee Movies and Retry.\n\nതാഴെ ഉള്ള ബട്ടൺ ക്ലിക്ക് ചെയ്ത ചാനലിൽ ജോയിൻ ആയ ശേഷം. Retry ബട്ടൺ അമർത്തുക. \n\nJD-',reply_to_message_id = update.id, reply_markup = InlineKeyboardMarkup([ [ InlineKeyboardButton("👉🏻 Join Channel 👈🏻" ,url=f"https://t.me/{update_channel}") ],[ InlineKeyboardButton("🔄       Retry       🔄" ,url=f"https://t.me/TheJDbot?start={file_uid}") ]   ]))
                return
        

    buttons = [[
        InlineKeyboardButton('Youtube', url='https://www.youtube.com/channel/UCe5RaLkqRimYwdWss4FpH2w'),
        InlineKeyboardButton('Telegram', url ='https://t.me/honeybeemovies')
    ],[
        InlineKeyboardButton('⚡ Movie Updates ⚡🛠', url='https://t.me/malluflix')
    ],[
        InlineKeyboardButton('⚙ Help ⚙', callback_data="help")
    ]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    
    send_messager=await bot.send_photo(
                chat_id = update.chat.id,
                photo="https://telegra.ph/file/156cfe447430f759c5d4d.jpg",
                caption=Translation.START_TEXT.format(
                update.from_user.first_name),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML,
                reply_to_message_id=update.id
            )
        


@Client.on_message(filters.command(["help"]) & filters.private, group=1)
async def help(bot, update):
    buttons = [[
        InlineKeyboardButton('Home ⚡', callback_data='start'),
        InlineKeyboardButton('About 🚩', callback_data='about')
    ],[
        InlineKeyboardButton('Close 🔐', callback_data='close')
    ]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.HELP_TEXT,
        reply_markup=reply_markup,
        parse_mode=enums.ParseMode.HTML,
        reply_to_message_id=update.id
    )


@Client.on_message(filters.command(["about"]) & filters.private, group=1)
async def about(bot, update):
    
    buttons = [[
        InlineKeyboardButton('Home ⚡', callback_data='start'),
        InlineKeyboardButton('Close 🔐', callback_data='close')
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.ABOUT_TEXT,
        reply_markup=reply_markup,
        disable_web_page_preview=True,
        parse_mode=enums.ParseMode.HTML,
        reply_to_message_id=update.id
    )

@Client.on_message(filters.command(["uk"]) & filters.private, group=1)
async def uk(bot, update):
    
    
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.UK_TEXT,
        disable_web_page_preview=True,
        parse_mode=enums.ParseMode.HTML,
        reply_to_message_id=update.id
    )
    await bot.send_video(
        chat_id=update.chat.id,
        video="https://telegra.ph/file/fd15b7c8c6fc7291d0717.mp4",
        caption=f"😘😘😘😘😘❤️❤️",
        parse_mode=enums.ParseMode.HTML,
        reply_to_message_id=update.id
    )

@Client.on_message(filters.command(["ping"]) & filters.private, group=1)
async def ping(bot, update):
    await update.reply_text("pong")
    
@Client.on_message(filters.command(["send"]) & (filters.user([866263993,411872315])) & filters.private)
async def sendu(bot, message): #| filters.user(961108166)
    try:
        if(len(message.text.split()))<3:
            await bot.send_message(
                text="Mmm. Kazhinjo😒",
                chat_id=message.chat.id,
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML,
            )
        elif message.reply_to_message is not None:
            id=message.text.split()[1]
            """await bot.copy_message(
                chat_id=id,
                from_chat_id=message.chat.id,
                message_id=message.reply_to_message.message_id,
                parse_mode=enums.ParseMode.HTML
            )"""
            await message.reply_to_message.copy(id)
        else:
            id=message.text.split()[1]
            tt=' '.join(message.text.split()[2:])
            await bot.send_message(
            text=tt,
            chat_id=id,
            disable_web_page_preview=True,
            parse_mode=enums.ParseMode.HTML,
            reply_to_message_id=message.message_id
        )
    except Exception as e:
            await message.reply_text(f"{e}")
            
@Client.on_message(filters.command(["lg"]) & (filters.user([866263993,411872315])) & filters.private) # FOR IDENTIFY WHICH MOVIE USER TAKEN. UNIQUE ID WILL GET FROM pm_text
async def linkgen(client, message):
    if message.reply_to_message:
        try:
            count =len(message.reply_to_message.text.split())
            id=message.reply_to_message.text.split()[count-1]
            link="https://t.me/TheJDbot?start="+id
            await message.reply_text(link)
        except Exception as e:
            await message.reply_text(f"{e}") 
    """ FROM HERE PM CHAT REPLY IS SETTED   here 4 funs are created 2 for client, 2 for sender//  """
    
@Client.on_message(filters.private & filters.text)
async def pm_text(bot, message):
    if message.from_user.id == 411872315:
        await reply_text(bot, message)
        return
    info = await bot.get_users(user_ids=message.from_user.id)
    reference_id = int(message.chat.id)
    await bot.send_message(
        chat_id=411872315,
        text=Presets.PM_TXT_ATT.format(reference_id, info.mention(info.first_name), message.text),
        parse_mode=enums.ParseMode.HTML
    )


@Client.on_message(filters.private & filters.media)
async def pm_media(bot, message):
    if message.from_user.id == 411872315:
        await replay_media(bot, message)
        return
    info = await bot.get_users(user_ids=message.from_user.id)
    reference_id = int(message.chat.id)
    await bot.copy_message(
        chat_id=411872315,
        from_chat_id=message.chat.id,
        message_id=message.message_id,
        caption=Presets.PM_MED_ATT.format(reference_id, info.first_name),
        parse_mode=enums.ParseMode.HTML
    )


@Client.on_message(filters.user(411872315) & filters.text)
async def reply_text(bot, message):
    reference_id = True
    if message.reply_to_message is not None:
        file = message.reply_to_message
        try:
            reference_id = file.text.split()[2]
        except Exception as e:
            pass
        try:
            reference_id = file.caption.split()[2]
        except Exception as e:
            pass
        try:
            chat_id=int(reference_id)
            await bot.send_message(
                text=message.text,
                chat_id=int(reference_id)
            )
        except Exception as e:
            await message.reply_text(f"{e}") 


@Client.on_message(filters.user(411872315) & filters.media)
async def replay_media(bot, message):
    reference_id = True
    if message.reply_to_message is not None:
        file = message.reply_to_message
        try:
            reference_id = file.text.split()[2]
        except Exception:
            pass
        try:
            reference_id = file.caption.split()[2]
        except Exception:
            pass
        try:
            
            await bot.copy_message(
                chat_id=int(reference_id),
                from_chat_id=message.chat.id,
                message_id=message.message_id,
                parse_mode=enums.ParseMode.HTML
            )
        except Exception as e:
            await message.reply_text(f"{e}") 
#Movie request command
@Client.on_message(filters.command(["request","request@TheJDbot"]) | filters.private & filters.group, group=1) #@TheJDbot
async def requestt(bot, message):
    id=message.from_user.id
    info = await bot.get_users(user_ids=message.from_user.id)
    try:
        if(len(message.text.split()))<2:
            texto="Before sending request please check your movie in @honeybeemoviesgroup .if you didnt get Please Send request in this format \n\n      eg: /request Jilla 2014\n\n."
        else:
            movie=message.text.split()[1]
            texto="Hey " +str(message.from_user.first_name)+". Your request for movie " +movie+ " has been send successfully ✅ please check @honeybeemoviesgroup after few hours 🥂"
        await bot.send_message(
            text=texto,
            chat_id=message.chat.id,
            disable_web_page_preview=True,
            parse_mode=enums.ParseMode.HTML,
            reply_to_message_id=message.message_id
        ) 
        if(len(message.text.split()))>1:
            await bot.send_message(        
            text=Presets.REQ_FORMAT.format(str(id), info.mention(info.first_name), ' '.join(message.text.split()[1:])),
            chat_id=-1001658152726,
            disable_web_page_preview=True,
            parse_mode=enums.ParseMode.HTML,
            reply_to_message_id=message.message_id
            )
    except Exception as e:
            await bot.send_message(
            text=e,
            chat_id=-1001658152726,
            reply_to_message_id=message.message_id
            )
    


@Client.on_message(filters.command(["motivation","motivation@TheJDbot"]) | filters.private & filters.group, group=1) #@TheJDbot
async def moti(bot, update):        
    await bot.send_video(
        chat_id=update.chat.id,
        video="https://telegra.ph/file/b85c9c5cb62f2370a5508.mp4",
        caption=f"Life is Very Short Nanba.Always be Happy 😉☺️",
        parse_mode=enums.ParseMode.HTML
    )
    
@Client.on_message(filters.command(["uki"]) & filters.private, group=1)
async def ukii(bot, message):
    chat_id=message.chat.id
    today = date.today()
    diff=date(2023,8,18)-today
    day= diff.days
    """if today.month<=8:
        x=date.today()
        diff=date(2022,8,18)-date(2022,x.month,x.day)
        day=diff.days
    else:
        x=date.today()
        diff=date(2022,8,18)-date(2021,12-x.month+7,31-x.date+17)
        day= diff.days"""


    wish=await bot.send_message(chat_id, text="Hey UK 😉😉😉😉")
    await asyncio.sleep(3)
    await wish.edit_text(str(day)+" days left for my uki day")
    await asyncio.sleep(3)
    await wish.edit_text("Are you Excited baby")
    await asyncio.sleep(3)
    await wish.edit_text("3️⃣")
    await asyncio.sleep(1)
    await wish.edit_text("2️⃣")
    await asyncio.sleep(1)
    await wish.edit_text("1️⃣")
    await asyncio.sleep(1)
    await wish.edit_text("🎆")
    await asyncio.sleep(3)
    await wish.edit_text("🎂")
    await asyncio.sleep(4)
    await wish.edit_text("Always be Happy Ukii.Im with you🥰🥰😘😘")

@Client.on_message(filters.command(["tryme","tryme@TheJDbot"]) | filters.private & filters.group, group=1)     # JUST FOR FUN
async def tryme(bot, message):
    array=['😫','🍾','🥂','😌','😉','🕺','😂']
    chat_id=message.chat.id
    anim=await bot.send_message(chat_id, text="🥴")
    try:
        for x in range(len(array)):
            await asyncio.sleep(3)
            await anim.edit_text(array[x])

    except Exception as e:
        await bot.send_message(
            text="Nashipikkuo",
            chat_id=-1001658152726,
            reply_to_message_id=message.message_id
            )
@Client.on_message(filters.new_chat_members, group=1)     # TO GENERATE WELCOME MESSAGE
async def welcomee(client, message):
    new_member = [u.first_name for u in message.new_chat_members]
    texto = Presets.MELCOW.format(", ".join(new_member))
    wel = await client.send_video(
        chat_id=message.chat.id,
        video="https://telegra.ph/file/9a27c0cc08a173acb140c.mp4",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Click Here to Join in Channel", url="https://t.me/honeybeemovies" )]]),
        caption=texto
        )

    await asyncio.sleep(40)
    await wel.delete()
    
@Client.on_message(filters.command(["cap"]) & (filters.user([866263993,411872315])) & filters.private, group=1)     # TO GENERATE CAPTION
async def caption(client, message):
    if message.reply_to_message:
        ogcap=message.reply_to_message.caption
        if ogcap==None:
            newcap=Presets.ccaption
        else:
            newcap="<b><i>"+str(ogcap)+"</b></i>"+Presets.ccaption
        await message.reply_to_message.copy(message.chat.id, caption=newcap)
  
@Client.on_message(filters.command(["but"]) & filters.private, group=1)     # TO GENERATE BUTTON
async def buttton(client, message):
    if message.reply_to_message:
        try:
            if(len(message.text.split()))<3:
                await message.reply_text("Linkm button Textum indo")
            else:
                butname=message.text.split()[1]
                link=message.text.split()[2]
                buttmaker=InlineKeyboardMarkup(
                                [
                                    [
                                        InlineKeyboardButton
                                            (
                                                f'{butname}', url=f"{link}"
                                            )
                                    ]
                                ]
                            )
                await message.reply_to_message.copy(message.chat.id, reply_markup=buttmaker)
        except Exception as e:
            await message.reply_text(f"{e}")

            
@Client.on_message(filters.command(["donors","donors@TheJDbot"]) | filters.private & filters.group, group=-1)     # JUST FOR FUN
async def donation(bot, message):
    await message.reply_text(f"{Presets.donors}",disable_web_page_preview="true")

    
@Client.on_message(filters.command(["donate","donate@TheJDbot"]) | filters.private & filters.group, group=-1)
async def donate(bot, message):
    await message.reply_text(f"Please donate any amount to support JD Bot. You can donate from (10 Rs - ∞)\n\n  UPI ID : <code>akhilbaiju00135@oksbi</code> \n\nDonors list will be published on /donors. Send Payment and then send the screenshot to @hbmccbot") 
