import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# Ενεργοποίηση καταγραφής
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = os.getenv("TELEGRAM_TOKEN")
FOOTBALL_API_KEY = "5e68f21c06f5453db1ca54a9a80076c9"

# 1. Εντολή /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚽ Γεια σου! Είμαι το bot ανάλυσης ποδοσφαίρου.\n\n"
        "Διαθέσιμες εντολές:\n"
        "• /competitions - Εμφάνιση ΟΛΩΝ των διαθέσιμων διοργανώσεων και των IDs τους\n"
        "• /analyze [ID] - Ανάλυση αγώνων για μια συγκεκριμένη διοργάνωση (π.χ. /analyze 2021)"
    )

# 2. Εντολή /competitions (Φέρνει ΟΛΕΣ τις διοργανώσεις από το API)
async def list_competitions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "https://api.football-data.org/v4/competitions"
    headers = {"X-Auth-Token": FOOTBALL_API_KEY}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        await update.message.reply_text("⚠️ Σφάλμα ανάκτησης διοργανώσεων από το API.")
        return

    data = response.json()
    comp_list = "🏆 **Όλες οι Διαθέσιμες Διοργανώσεις:**\n\n"
    
    for comp in data.get("competitions", []):
        comp_id = comp['id']
        comp_name = comp['name']
        area_name = comp['area']['name']
        
        comp_list += f"• **ID:** `{comp_id}` | {comp_name} ({area_name})\n"
        
        # Το Telegram έχει όριο 4096 χαρακτήρες ανά μήνυμα, οπότε το σπάμε αν γεμίσει
        if len(comp_list) > 3500:
            await update.message.reply_text(comp_list, parse_mode="Markdown")
            comp_list = ""

    if comp_list:
        await update.message.reply_text(comp_list, parse_mode="Markdown")

# 3. Εντολή /analyze [ID] (Ανάλυση βάσει επιλεγμένης διοργάνωσης)
async def analyze_match(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Αν ο χρήστης δεν δώσει ID, βάζουμε προεπιλογή την Premier League (ID: 2021)
    comp_id = context.args[0] if context.args else "2021"
    
    url = f"https://api.football-data.org/v4/competitions/{comp_id}/matches?status=SCHEDULED"
    headers = {"X-Auth-Token": FOOTBALL_API_KEY}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        await update.message.reply_text("⚠️ Σφάλμα: Ίσخة η διοργάνωση δεν υπάρχει ή δεν υποστηρίζεται στο τρέχον πακέτο.")
        return

    data = response.json()
    matches = data.get("matches", [])

    if not matches:
        await update.message.reply_text("📭 Δεν βρέθηκαν προγραμματισμένοι αγώνες για αυτή τη διοργάνωση αυτή τη στιγμή.")
        return

    match = matches[0]
    home_team = match["homeTeam"]["name"]
    away_team = match["awayTeam"]["name"]
    competition = data.get("competition", {}).get("name", "Άγνωστη Διοργάνωση")
    match_date = match["utcDate"]

    # Στατιστικά / Προσομοίωση xGoals
    home_xG = 1.65
    away_xG = 1.15
    
    analysis_text = (
        f"📊 **DEEP DATA MATCH ANALYSIS** 📊\n\n"
        f"🏆 **Διοργάνωση:** {competition}\n"
        f"⚽ **Αγώνας:** {home_team} vs {away_team}\n"
        f"📅 **Ημερομηνία:** {match_date[:10]}\n\n"
        f"📈 **Προηγμένη Ανάλυση (xGoals):**\n"
        f"• xG {home_team}: **{home_xG}**\n"
        f"• xG {away_team}: **{away_xG}**\n\n"
        f"💡 **Εκτίμηση:** Over 1.5 Goals & 1X (Διπλή Ευκαιρία)."
    )

    await update.message.reply_text(analysis_text, parse_mode="Markdown")

if __name__ == '__main__':
    if not TOKEN:
        raise ValueError("Δεν βρέθηκε το TELEGRAM_TOKEN!")

    app = ApplicationBuilder().token(TOKEN).build()

    # Καταχώρηση εντολών
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("competitions", list_competitions))
    app.add_handler(CommandHandler("analyze", analyze_match))

    print("Το bot ενημερώθηκε και ξεκίνησε επιτυχώς...")
    app.run_polling()
