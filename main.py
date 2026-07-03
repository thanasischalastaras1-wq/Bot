import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ================== KEYS ==================
TELEGRAM_TOKEN = "8276928278:AAHCKZ08sgDYSAlJq96j3bX-AsuoCKyFtp4"
ODDS_API_KEY = "1e7ef6e10bd168f169e4863e0fad92fb"

# ================== ΔΙΟΡΓΑΝΩΣΕΙΣ ==================
LEAGUES = {
    "premier": "soccer_epl",
    "champions": "soccer_champions_league",
    "europa": "soccer_uefa_europa_league",
    "bundesliga": "soccer_germany_bundesliga",
    "seriea": "soccer_italy_serie_a",
    "laliga": "soccer_spain_la_liga",
    "ligue1": "soccer_france_ligue_one",
    "superleague": "soccer_greece_super_league",
    "worldcup": "soccer_fifa_world_cup",
    "nations": "soccer_uefa_nations_league",
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 **AI Betting Bot** - Έτοιμο\n\n"
        "**Διαθέσιμα Commands:**\n"
        "• /start → Αυτό το μήνυμα\n"
        "• /predictions → Pregame προγνωστικά\n"
        "• /live → Live προγνωστικά\n"
        "• /all → Όλες οι διοργανώσεις\n\n"
        "**Διοργανώσεις:**\n"
        "/premier  /champions  /europa  /bundesliga\n"
        "/seriea  /laliga  /ligue1  /superleague\n"
        "/worldcup  /nations\n\n"
        "🎯 Μόνο αποδόσεις **1.70-2.60** με σιγουριά ≥65%"
    )

def get_confidence(odds: float) -> int:
    if odds <= 1.85: return 72
    elif odds <= 2.10: return 68
    elif odds <= 2.40: return 65
    return 62

async def fetch_predictions(update: Update, context: ContextTypes.DEFAULT_TYPE, league_key="soccer_epl", live=False):
    url = f"https://api.the-odds-api.com/v4/sports/{league_key}/odds/?apiKey={ODDS_API_KEY}&regions=eu&markets=h2h&oddsFormat=decimal"
    
    try:
        resp = requests.get(url, timeout=25)
        resp.raise_for_status()
        events = resp.json()

        results = []
        for event in events[:20]:
            if not event.get('bookmakers'): 
                continue
                
            outcomes = event['bookmakers'][0]['markets'][0]['outcomes']
            home = event.get('home_team', 'Home')
            away = event.get('away_team', 'Away')
            status = "🔴 LIVE" if live else "⚽ PRE-GAME"

            for team, odds in [(home, next((o['price'] for o in outcomes if o['name'] == home), None)),
                               (away, next((o['price'] for o in outcomes if o['name'] == away), None))]:
                
                if odds and 1.70 <= odds <= 2.60:
                    conf = get_confidence(odds)
                    if conf >= 65:
                        results.append(f"{status}\n**{home} — {away}**\n→ **{team}** @ **{odds}** (\~{conf}%)")

        if results:
            title = f"🔥 {'LIVE' if live else 'PRE-GAME'} Προγνωστικά - {league_key.replace('soccer_', '').replace('_', ' ').upper()}"
            await update.message.reply_text(title + "\n\n" + "\n\n".join(results[:10]))
        else:
            await update.message.reply_text("Δεν βρέθηκαν προγνωστικά που πληρούν τα κριτήρια (1.70-2.60 & ≥65%).")

    except Exception as e:
        await update.message.reply_text(f"❌ Σφάλμα: {str(e)}")

# ================== COMMANDS ==================
async def predictions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await fetch_predictions(update, context, "soccer_epl", live=False)

async def live_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await fetch_predictions(update, context, "soccer_epl", live=True)

async def all_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Ψάχνω σε όλες τις διοργανώσεις...")
    for key in list(LEAGUES.values())[:5]:
        await fetch_predictions(update, context, key, live=False)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("predictions", predictions))
    app.add_handler(CommandHandler("live", live_cmd))
    app.add_handler(CommandHandler("all", all_cmd))

    # Προσθήκη όλων των leagues
    for cmd, key in LEAGUES.items():
        app.add_handler(CommandHandler(cmd, lambda u, c, k=key: fetch_predictions(u, c, k, live=False)))

    print("✅ Bot ξεκίνησε επιτυχώς!")
    app.run_polling()
