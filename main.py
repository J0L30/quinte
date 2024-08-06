import fitz  # PyMuPDF
import re
from collections import Counter
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Function to extract horse rankings from the document text
def extract_horse_rankings(document_text):
    pattern = r'\d+ [A-Z]+'
    matches = re.findall(pattern, document_text)
    horse_rankings = Counter()
    for match in matches:
        number, horse = match.split()
        horse_rankings[horse] += 1
    return horse_rankings

# Function to get the top N horses based on their frequencies
def get_top_horses(rankings, top_n=5):
    top_horses = rankings.most_common(top_n)
    return [horse for horse, freq in top_horses]

# Start command handler
def start(update: Update, context: CallbackContext):
    update.message.reply_text('Hi! Send me a PDF file with the race program and I will tell you the top 5 horses.')

# Document handler
def handle_document(update: Update, context: CallbackContext):
    file = update.message.document.get_file()
    file_path = 'race_program.pdf'
    file.download(file_path)
    
    document_text = extract_text_from_pdf(file_path)
    horse_rankings = extract_horse_rankings(document_text)
    top_horses = get_top_horses(horse_rankings)
    
    response = f"Top 5 horses based on expert predictions: {', '.join(top_horses)}"
    update.message.reply_text(response)

# Main function to set up the bot
def main():
    # Replace 'YOUR_TOKEN_HERE' with your actual Telegram bot token
    updater = Updater('YOUR_TOKEN_HERE', use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.document.mime_type("application/pdf"), handle_document))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
