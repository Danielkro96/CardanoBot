from secret import APIKEY, BOT_TOKEN
from requests import request
from telegram import Update, InputTextMessageContent, InlineQueryResultArticle
from telegram.ext import Application, CommandHandler, ContextTypes, InlineQueryHandler


url = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest?symbol=ada"
payload = {}
headers = {
    'X-CMC_PRO_API_KEY': APIKEY
}


def get_response(data: str):
    response = request("GET", url, headers=headers, data=payload).json()
    return response['data']['ADA'][0]['quote']['USD'][data]


def log(log):
    with open("log.txt", "a") as log_file:
        log_file.write(f"{log}\n")
    print(log)


# Bot Commands
async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price = round(get_response("price"), 5)
    await update.message.reply_text(f"The price now is: {price}$")
    log(f"[LOGGER] "
        f"{update.message.chat.first_name} "
        f"(username-{update.message.chat.username} id-{update.message.chat.id}): {update.message.text}"
        f", response: {price}"
        f"")


async def change(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    response = ""
    if "/change1h" in text:
        response = round(get_response("percent_change_1h"), 2)
        await update.message.reply_text(f"The price change in the last 1 hour is: {response}%")
    elif "/change24h" in text:
        response = round(get_response("percent_change_24h"), 2)
        await update.message.reply_text(f"The price change in the last 24 hour is: {response}%")
    elif "/change7d" in text:
        response = round(get_response("percent_change_7d"), 2)
        await update.message.reply_text(f"The price change in the last 7 days is: {response}%")
    elif "/change30d" in text:
        response = round(get_response("percent_change_30d"), 2)
        await update.message.reply_text(f"The price change in the last 30 days is: {response}%")

    log(f"[LOGGER] "
        f"{update.message.chat.first_name} "
        f"(username-{update.message.chat.username} id-{update.message.chat.id}): {update.message.text}"
        f", response: {response}"
        f"")


async def inline_query(update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    results = []

    if "price" in query:
        response = round(get_response("price"), 5)
        results.append(
            InlineQueryResultArticle(
                id='1',
                title='Price',
                description="The current price of Cardano (ADA)",
                input_message_content=InputTextMessageContent(
                    f"The price now is: {response}$"
                ),
                thumbnail_url="https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcT1LFIx_oSdXwtdFaDEvH10gVaRSVpWNqDY5-P8S2qMpIVexwxV",
                thumbnail_width=100,
                thumbnail_height=100
            )
        )
    elif "change1h" in query:
        response = round(get_response("percent_change_1h"), 2)
        results.append(
            InlineQueryResultArticle(
                id='1',
                title='Percent change in the last hour',
                description="The change in Cardano (ADA) price in the last hour",
                input_message_content=InputTextMessageContent(
                    f"The price change in the last hour is: {response}$"
                ),
                thumbnail_url="https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcT1LFIx_oSdXwtdFaDEvH10gVaRSVpWNqDY5-P8S2qMpIVexwxV",
                thumbnail_width=100,
                thumbnail_height=100
            )
        )
    elif "change24h" in query:
        response = round(get_response("percent_change_24h"), 2)
        results.append(
            InlineQueryResultArticle(
                id='1',
                title='Percent change in the last 24 hours',
                description= "The change in Cardano (ADA) price in the last 24 hours",
                input_message_content=InputTextMessageContent(
                    f"The price change in the last 24 hours is: {response}$"
                ),
                thumbnail_url="https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcT1LFIx_oSdXwtdFaDEvH10gVaRSVpWNqDY5-P8S2qMpIVexwxV",
                thumbnail_width=100,
                thumbnail_height=100
            )
        )
    elif "change7d" in query:
        response = round(get_response("percent_change_7d"), 2)
        results.append(
            InlineQueryResultArticle(
                id='1',
                title='Percent change in the last 7 days',
                description= "The change in Cardano (ADA) price in the last 7 days",
                input_message_content=InputTextMessageContent(
                    f"The price change in the last 7 days is: {response}$"
                ),
                thumbnail_url="https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcT1LFIx_oSdXwtdFaDEvH10gVaRSVpWNqDY5-P8S2qMpIVexwxV",
                thumbnail_width=100,
                thumbnail_height=100
            )
        )
    elif "change30d" in query:
        response = round(get_response("percent_change_30d"), 2)
        results.append(
            InlineQueryResultArticle(
                id='1',
                title='Percent change in the last 30 days',
                description= "The change in Cardano (ADA) price in the last 30 days",
                input_message_content=InputTextMessageContent(
                    f"The price change in the last 30 days is: {response}$"
                ),
                thumbnail_url="https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcT1LFIx_oSdXwtdFaDEvH10gVaRSVpWNqDY5-P8S2qMpIVexwxV",
                thumbnail_width=100,
                thumbnail_height=100
            )
        )
    else:
        results = []

    await update.inline_query.answer(results)
    log(f"[LOGGER] {update.inline_query}")


# Bot Error Logging
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log(f"[ERROR] {update} - caused error: {context.error}")


if __name__ == "__main__":
    print("Starting CardanoNow bot")
    app = Application.builder().token(BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("price", price))
    app.add_handler(CommandHandler("change1h", change))
    app.add_handler(CommandHandler("change24h", change))
    app.add_handler(CommandHandler("change7d", change))
    app.add_handler(CommandHandler("change30d", change))

    app.add_handler(InlineQueryHandler(inline_query))

    # Error Logging
    app.add_error_handler(error)

    print("Start polling...")
    app.run_polling(poll_interval=3)
