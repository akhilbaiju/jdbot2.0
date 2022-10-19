from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait
import re, io
import asyncio
from pyrogram.types import Message
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.plugins.helpers import parser,split_quotes
import pymongo
import logging
import time
from presets import Presets

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
BDB_NAME = "broadcast" #DATABASE FOR ID COLLECTION FOR BROADCAST
FDB_NAME ="custfilters" #DATABASE FOR saving custom filters
BDB_URL = "mongodb+srv://akku:akku@crazybotsz.0sigd.mongodb.net/myFirstDatabase?authSource=admin&replicaSet=atlas-hfb4ku-shard-0&w=majority&readPreference=primary&appname=MongoDB%20Compass&retryWrites=true&ssl=true"
mongo = pymongo.MongoClient(BDB_URL)
bdb = mongo[BDB_NAME]
fdb = mongo[FDB_NAME]
fdbcol = fdb["cfilters"]
bdbcol = bdb["user"]

def insertid(chat_id):                  #INSERT ID OF USER TO SEND HIM BROADCAST
            user_id = int(chat_id)
            user_det = {"_id":user_id}
            try:
            	bdbcol.insert_one(user_det)
            except:
            	value = 'new'
            	return value
            	pass

def getid():
    values = []
    for key  in bdbcol.find():
         id = key["_id"]
         values.append((id)) 
    return values

async def gfilters():   #getfilters
    texts = []
    query = fdbcol.find()
    try:
        for file in query:
            text = file['text']
            texts.append(text)
    except:
        pass
    return texts
async def delete_filter(message, text):
    myquery = {'text':text }
    query = fdbcol.count_documents(myquery)
    if query == 1:
        fdbcol.delete_one(myquery)
        await message.reply_text(
            f"Command Activated Successfully ✅. '`{text}`'  Filter deleted Boss. I'll not respond to that filter anymore.",
            quote=True,
            parse_mode="md"
        )
    else:
        await message.reply_text("Boss Angane oru Filter save cheythitilla! 🤫❌❌❌", quote=True)


async def del_all(message):
    try:
        fdbcol.drop()
        await message.edit_text(f"All filters from our group has been removed boss ✅")
    except:
        await message.edit_text(f"Couldn't remove all filters from our group! ❌")
        return


async def count_filters():
    count = fdbcol.count()
    if count == 0:
        return False
    else:
        return count

@Client.on_message(filters.command(["deleteallfiltersofhbm"]) & (filters.user([866263993,411872315])), group=1)
async def deleteallfilter(client, message):
    try:
        fdbcol.drop()
        await message.reply_text(f"All filters from our group has been removed boss ✅")
    except:
        await message.reply_text(f"Couldn't remove all filters from our group! ❌")
        return
    
 #///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// 
@Client.on_message(filters.command(['stop', 'delete']) & (filters.user([866263993,411872315])), group=1)
async def deletefilter(client, message):
    try:
        text=' '.join(message.text.split()[1:])
    except:
        await message.reply_text(
            "Filter Mention cheythilla mister 😟",
            quote=True
        )
        return
    query = text.lower()
    await delete_filter(message, query)
 #/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////       
@Client.on_message(filters.command(['viewfilters', 'vf']) & (filters.user([866263993,411872315])), group=1)
async def send(bot, message):
    texts = await gfilters()
    count = await count_filters()
    if count:
        filterlist = f"There are **{count}** filters in our group\n\n"
        for text in texts:
            keywords = " ×  `{}`\n".format(text)            
            filterlist += keywords
        if len(filterlist) > 4096:
            with io.BytesIO(str.encode(filterlist.replace("`", ""))) as keyword_file:
                keyword_file.name = "keywords.txt"
                await message.reply_document(
                    document=keyword_file,
                    quote=True
                )
            return
    else:
        filterlist = f"There are No filters in our group"

    await message.reply_text(
        text=filterlist,
        quote=True,
        parse_mode="md"
    )

#/////////////////////////////////////////////////////////ADD FILTER COMMAND//////////////////////////////////////////////////////////////////////////
async def add_filter(text, reply_text, btn, file):
    data = {
        'text':str(text),
        'reply':str(reply_text),
        'btn':str(btn),
        'file':str(file)
    }

    try:
        fdbcol.update_one({'text': str(text)},  {"$set": data}, upsert=True)
    except:
        print('Couldnt save, check your db')

def get_file_id(msg: Message):
    if msg.media:
        for message_type in (
            "photo",
            "animation",
            "audio",
            "document",
            "video",
            "video_note",
            "voice",
            "sticker"
        ):
            obj = getattr(msg, message_type)
            if obj:
                setattr(obj, "message_type", message_type)
                return obj

@Client.on_message(filters.command(['filter', 'add']) & (filters.user([866263993,411872315])) & filters.private, group=1)
async def addfilter(client, message):
    #userid = message.from_user.id
    #chat_type = message.chat.type
    args = message.text.html.split(None, 1)
    if len(args) < 2:
        await message.reply_text("Command Incomplete :(", quote=True)
        return
    
    extracted = split_quotes(args[1])
    text = extracted[0].lower()
   
    if not message.reply_to_message and len(extracted) < 2:
        await message.reply_text("Add some content to save your filter!", quote=True)
        return

    if (len(extracted) >= 2) and not message.reply_to_message:
        reply_text, btn, alert = parser(extracted[1], text)
        fileid = None
        if not reply_text:
            await message.reply_text("You cannot have buttons alone, give some text to go with it!", quote=True)
            return

    elif message.reply_to_message and message.reply_to_message.reply_markup:
        try:
            rm = message.reply_to_message.reply_markup
            btn = rm.inline_keyboard
            msg = message.reply_to_message.document or\
                  message.reply_to_message.video or\
                  message.reply_to_message.photo or\
                  message.reply_to_message.audio or\
                  message.reply_to_message.animation or\
                  message.reply_to_message.sticker
            if msg:
                fileid = msg.file_id
                reply_text = message.reply_to_message.caption.html
            else:
                reply_text = message.reply_to_message.text.html
                fileid = None
            alert = None
        except:
            reply_text = ""
            btn = "[]" 
            fileid = None
            alert = None

    elif message.reply_to_message and message.reply_to_message.photo:
        try:
            fileid = message.reply_to_message.photo.file_id
            reply_text, btn, alert = parser(message.reply_to_message.caption.html, text)
        except:
            reply_text = ""
            btn = "[]"
            alert = None

    elif message.reply_to_message and message.reply_to_message.video:
        try:
            fileid = message.reply_to_message.video.file_id
            reply_text, btn, alert = parser(message.reply_to_message.caption.html, text)
        except:
            reply_text = ""
            btn = "[]"
            alert = None

    elif message.reply_to_message and message.reply_to_message.audio:
        try:
            fileid = message.reply_to_message.audio.file_id
            reply_text, btn, alert = parser(message.reply_to_message.caption.html, text)
        except:
            reply_text = ""
            btn = "[]"
            alert = None
   
    elif message.reply_to_message and message.reply_to_message.document:
        try:
            fileid = message.reply_to_message.document.file_id
            reply_text, btn, alert = parser(message.reply_to_message.caption.html, text)
        except:
            reply_text = ""
            btn = "[]"
            alert = None

    elif message.reply_to_message and message.reply_to_message.animation:
        try:
            fileid = message.reply_to_message.animation.file_id
            reply_text, btn, alert = parser(message.reply_to_message.caption.html, text)
        except:
            reply_text = ""
            btn = "[]"
            alert = None

    elif message.reply_to_message and message.reply_to_message.sticker:
        try:
            fileid = message.reply_to_message.sticker.file_id
            reply_text, btn, alert =  parser(extracted[1], text)
        except:
            reply_text = ""
            btn = "[]"
            alert = None

    elif message.reply_to_message and message.reply_to_message.text:
        try:
            fileid = None
            reply_text, btn, alert = parser(message.reply_to_message.text.html, text)
        except:
            reply_text = ""
            btn = "[]"
            alert = None

    else:
        return
    
    await add_filter(text, reply_text, btn, fileid)
    await message.reply_text(text = f'Filter Added : <code> {text} </code>', reply_to_message_id=message.id)
    #await add_filter(grp_id, text, reply_text, btn, fileid, alert)
    

#///////////////////////////////////////////////////////  FILTER GIVING ON INCOMING ///////////////////////////////////////////////////////////////////
async def find_filter(name):
    query = fdbcol.find( {"text":name})
    # query = mycol.find( { "$text": {"$search": name}})
    try:
        for file in query:
            reply_text = file['reply']
            btn = file['btn']
            fileid = file['file']
        return reply_text, btn, fileid
    except:
        return None, None, None


async def manual_filters(client,message):
    name = message.text
    keywords = await gfilters()
    for keyword in keywords:
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            reply_text, btn, fileid = await find_filter(keyword)
            #print("\n\nREPLT_TEXT : ", reply_text,"\n\nBTN TEXT: ", btn,"\n\n FILE ID",fileid)
            if reply_text:
                reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")

            if btn is not None:
                try:
                    if fileid == "None":
                        if btn == "[]":
                            await message.reply_text(reply_text, disable_web_page_preview=True)
                        else:
           
                            but =str(btn).replace('pyrogram.types.', '')
                            button = eval(but)
                            await message.reply_text(
                                reply_text,
                                disable_web_page_preview=True,
                                reply_markup=InlineKeyboardMarkup(button)
                            )
                            
                    else:
                        if btn == "[]":
                            await message.reply_cached_media(
                                fileid,
                                caption=reply_text or ""
                            )
                            
                        else:
                            but =str(btn).replace('pyrogram.types.', '')
                            button = eval(but)
                            await message.reply_cached_media(
                                fileid,
                                caption=reply_text or "",
                                reply_markup=InlineKeyboardMarkup(button)
                            )
                            
                except Exception as e:
                    logger.exception(e)
                break
    else:
        return False

@Client.on_message(filters.command(['broadcast']) & (filters.user([866263993,411872315])) & filters.private, group=1)
async def broadcast(bot, message):
    if (message.reply_to_message):
        ms = await message.reply_text("Geting All ids from database ...........")
        ids = getid()
        tot = len(ids)
        success = 0 
        failed = 0 
        await ms.edit(f"Starting Broadcast .... \n Sending Message To {tot} Users")
        for id in ids:
            try:
     	        time.sleep(1)
     	        await message.reply_to_message.copy(id)
     	        success += 1 
            except:
     	        failed += 1 
     	        pass
            try:
     	        await ms.edit( f"Message sent to {success} chat(s). {failed} chat(s) failed on receiving message. \nTotal - {tot}" )
            except FloodWait as e:
     	        await asyncio.sleep(t.x)
 
@Client.on_message(filters.command(['count']) & (filters.user([866263993,411872315])) & filters.private, group=1)
async def count(bot, message):
        ms = await message.reply_text("Geting All ids from database ...........")
        ids = getid()
        tot = len(ids)       
        await ms.edit(f"There are {tot} Users available")
            
@Client.on_message(filters.command(["deleteallsubs"]) & (filters.user([866263993,411872315])) & filters.private, group=1)
async def deleteallsubs(client, message):
    try:
        bdbcol.drop()
        await message.reply_text(f"All subscribers are removed ✅")
    except:
        await message.reply_text(f"Couldn't remove all subscribers! ❌")
        return 


@Client.on_message(filters.command(["jd"]) & (filters.user([866263993,411872315])) & filters.private, group=1)
async def request(bot, message):    
    await bot.send_message(
        chat_id=message.chat.id,
        text= Presets.COMMANDS,
        disable_web_page_preview=True,
        reply_to_message_id=message.id
    )
