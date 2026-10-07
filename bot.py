import os, re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

PROFILE = {
    'city': 'Tbilisi', 'district': 'Isani-Samgori', 'street': 'Moscow Avenue',
    'price': 850, 'area': 45, 'bedrooms': 1, 'floor': 10,
    'term': '1 year+', 'pets': False,
}

KEYWORDS = {
    'location': ['tbilisi','თბილისი','тбилиси','isani','ისანი','исани','samgori','სამგორი','самгори','moscow avenue','московский проспект','მოსკოვის გამზირი'],
    'longterm': ['long term','long-term','1 year','12 month','долгоср','год','1 год','გრძელვად','1 წელი','12 თვე'],
    'onebed': ['1 bedroom','one bedroom','1br','1 bed','1 спаль','однокомнат','1 საძინ'],
    'couple': ['couple','pair','пара','семейная пара','წყვილი','alone','single','один','одна','ერთი ადამიანი'],
    'nopets': ['no pets','без животных','нет животных','без питомцев','ცხოველების გარეშე','შინაური ცხოველები არ'],
}

def score_text(text: str):
    t = text.lower()
    score, reasons = 0, []
    if any(k in t for k in KEYWORDS['location']): score += 30; reasons.append('📍 location')
    if any(k in t for k in KEYWORDS['longterm']): score += 20; reasons.append('📅 long-term')
    if any(k in t for k in KEYWORDS['onebed']): score += 15; reasons.append('🛏 1 bedroom')
    if any(k in t for k in KEYWORDS['couple']): score += 10; reasons.append('👤 tenant type')
    if any(k in t for k in KEYWORDS['nopets']): score += 10; reasons.append('🐾 no pets')
    amounts = [int(x) for x in re.findall(r'\$\s?(\d{3,4})|(?:usd|dollars?)\s?(\d{3,4})', t) for x in x if x]
    if not amounts:
        amounts = [int(x) for x in re.findall(r'\b(\d{3,4})\s?(?:\$|usd)', t)]
    if amounts:
        budget=max(amounts)
        if budget >= 850: score += 15; reasons.append(f'💵 budget ${budget}')
        elif budget >= 750: score += 8; reasons.append(f'💵 budget ${budget} (negotiation)')
    return min(score,100), reasons

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '🏠 Tbilisi Tenant Finder\n\n'
        'Profile: Moscow Avenue, Isani–Samgori • 45 m² • 1 bedroom • $850/month • 1 year+ • no pets.\n\n'
        'Forward or paste a tenant-search post here and I will score the match.\n'
        'Commands: /profile /help'
    )

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '🏠 Apartment profile\n📍 Tbilisi, Isani–Samgori, Moscow Avenue\n📐 45 m² • 10th floor • 1 bedroom\n💵 $850/month\n📅 Minimum 1 year\n👤 One person or couple\n🐾 No pets\n🅿️ Parking • balcony • elevator • Smart Home'
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Paste or forward a public post from someone looking to rent in Tbilisi. I will calculate a match score and explain why.')

async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or update.message.caption or ''
    if not text.strip(): return
    score, reasons = score_text(text)
    level = '🟢 Strong match' if score >= 70 else ('🟡 Possible match' if score >= 45 else '🔴 Weak match')
    why = '\n'.join('• '+r for r in reasons) if reasons else '• No key criteria detected'
    await update.message.reply_text(f'{level} — {score}%\n\n{why}\n\nOriginal text:\n{text[:1200]}')

def main():
    if not TOKEN:
        raise RuntimeError('Set TELEGRAM_BOT_TOKEN environment variable')
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('profile', profile))
    app.add_handler(CommandHandler('help', help_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, analyze))
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
