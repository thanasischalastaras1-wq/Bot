import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TELEGRAM_TOKEN = "8276928278:AAHCKZ08sgDYSAlJq96j3bX-AsuoCKyFtp4"
API_KEY = "e10d3062f8f4474c5462122b5979d172"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 **Live Stats + Over/Under Bot**\n\n"
        "🔴 /live → Live ανάλυση + Προγνωστικά (Over, BTTS κλπ.)\n"
    )

def make_prediction(home_name, away_name, stats):
    possession = 50
    total_shots = 0

    for s in stats:
        if 'Ball Possession' in str(s):
            possession = 55  # Απλοποιημένο
        if 'Shots on Goal' in str(s):
            total_shots += 2

    if total_shots >= 8 or possession > 58:
        return f"→ **Over 2.5 Goals** (Πολλές ευκαιρίες)"
    elif total_shots <= 4:
        return f"→ **Under 2.5 Goals**"
    else:
        return f"→ BTTS (Both Teams To Score) πιθανό"

async def live_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Αναλύω live ματς...")

    headers = {'x-apisports-key': API_KEY}
    
    try:
        resp = requests.get("https://v3.football.api-sports.io/fixtures?live=all", headers=headers)
        fixtures = resp.json().get('response', [])

        if not fixtures:
            await update.message.reply_text("Δεν υπάρχουν live ματς αυτή τη στιγμή.")
            return

        for fixture in fixtures[:5]:
            match_id = fixture['fixture']['id']
            home = fixture['teams']['home']['name']
            away = fixture['teams']['away']['name']
            score = f"{fixture['goals']['home']}-{fixture['goals']['away']}"

            stat_resp = requests.get(f"https://v3.football.api-sports.io/fixtures/statistics?fixture={match_id}", headers=headers)
            stats = stat_resp.json().get('response', [])

            analysis = f"🔴 **LIVE** | {home} {score} {away}\n"
            analysis += make_prediction(home, away, stats)
            
            await update.message.reply_text(analysis)

    except Exception as e:
        await update.message.reply_text(f"Σφάλμα: {str(e)}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("live", live_cmd))
    
    print("✅ Bot με Over/Under τρέχει!")
    app.run_polling()
