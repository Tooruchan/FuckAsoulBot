from pyrogram import Client, filters
from pyrogram.errors import UserAdminInvalid
from pyrogram.types import Message, ChatPermissions

app = Client("bot", bot_token="", config_file="config.ini")

packs = ["a_soul_diana", "jiarandiana"]
COUNT_LIMIT = 3
count = {}
blocklist = ['嘉人', '嘉然', '嘉心糖', "晚晚", "向晚", "珈乐", "孩梓", "海子姐", "然然", "AS", "一个魂", "A-Soul", "AU", 'au', "8u", "杜华",
             "阿梓", 'yhm', "樱花妹", "娜娜米"]


@app.on_message(filters.group & filters.text)
async def process_texts(client: Client, message: Message):
    chat = message.chat.id
    user = message.from_user
    text = message.text
    for i in blocklist:
        if text.find(i) or text.endswith("捏"):
            await client.delete_messages(chat, message.message_id)
            if str(message.chat.id) + '_' + str(message.from_user.id) in count.keys():
                pass
            else:
                count[str(message.chat.id) + '_' + str(message.from_user.id)] = 0
            count[str(message.chat.id) + '_' + str(message.from_user.id)] = count[str(message.chat.id) + '_' + str(
                message.from_user.id)] + 1
            await client.send_message(chat,
                                      "[{target}](tg://user?id={target_id})发送的话题在本群已被禁止，请勿再次发送，您已发送{counts}次，当您发送 {maxcount} 次时将会被禁言。".format(
                                          target='您', target_id=user.id,
                                          counts=count[str(message.chat.id) + '_' + str(message.from_user.id)],
                                          maxcount=COUNT_LIMIT))
            if count[str(message.chat.id) + '_' + str(message.from_user.id)] == COUNT_LIMIT:
                del count[str(message.chat.id) + '_' + str(message.from_user.id)]
                try:
                    await client.restrict_chat_member(chat, message.from_user.id, ChatPermissions())
                    await client.send_message(chat,
                                              "用户{UID}已经连续发送{count}次违禁发言，已被永久禁言。".format(UID=message.from_user.id,
                                                                                          count=COUNT_LIMIT))
                except UserAdminInvalid:
                    pass
            return


@app.on_message(filters.group & filters.sticker)
async def process_stickers(client: Client, message: Message):
    setname = message.sticker.set_name
    chat = message.chat.id
    user = message.from_user
    if setname in packs:
        await client.delete_messages(chat, message.message_id)
        if str(message.chat.id) + '_' + str(message.from_user.id) in count.keys():
            pass
        else:
            count[str(message.chat.id) + '_' + str(message.from_user.id)] = 0
        count[str(message.chat.id) + '_' + str(message.from_user.id)] = count[str(message.chat.id) + '_' + str(
            message.from_user.id)] + 1
        await client.send_message(chat,
                                  "[{target}](tg://user?id={target_id})发送的 Sticker 在本群已被禁止，请勿再次发送，您已发送{counts}次，当您发送 {maxcount} 次时将会被禁言。".format(
                                      target='您', target_id=user.id,
                                      counts=count[str(message.chat.id) + '_' + str(message.from_user.id)],
                                      maxcount=COUNT_LIMIT))
        if count[str(message.chat.id) + '_' + str(message.from_user.id)] == COUNT_LIMIT:
            del count[str(message.chat.id) + '_' + str(message.from_user.id)]
            try:
                await client.restrict_chat_member(chat, message.from_user.id, ChatPermissions())
                await client.send_message(chat, "用户{UID}已经连续发送{count}次违禁表情包，已被永久禁言。".format(UID=message.from_user.id,
                                                                                            count=COUNT_LIMIT))
            except UserAdminInvalid:
                pass


if __name__ == '__main__':
    app.run()
