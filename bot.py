# bot.py

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

from config import TELEGRAM_TOKEN

from football_api import (
    today_matches,
    last_matches,
    h2h
)

from analyzer import (
    calculate_stats,
    team_form,
    analyze_1x2,
    analyze_goals,
    h2h_analysis,
    best_selection
)


# προσωρινή μνήμη αγώνων
MATCH_LIST = {}



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        """
⚽ Deep Data Football Bot

Εντολές:

/today
➡️ Όλοι οι σημερινοί αγώνες

/analyze 1
➡️ Ανάλυση αγώνα από τη λίστα
"""
    )





async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global MATCH_LIST


    matches = today_matches()


    if not matches:

        await update.message.reply_text(
            "Δεν υπάρχουν αγώνες σήμερα."
        )

        return



    MATCH_LIST = {}


    text = "⚽ Σημερινοί αγώνες\n\n"


    counter = 1


    for match in matches:

        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]

        league = match["league"]["name"]


        MATCH_LIST[str(counter)] = match


        text += (
            f"{counter}) ⚽ {home} - {away}\n"
            f"🏆 {league}\n\n"
        )


        counter += 1



    await update.message.reply_text(
        text
    )







async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global MATCH_LIST


    if not context.args:

        await update.message.reply_text(
            "Χρήση:\n/analyze 1"
        )

        return



    number = context.args[0]


    if number not in MATCH_LIST:

        await update.message.reply_text(
            "Δεν βρέθηκε ο αγώνας."
        )

        return



    match = MATCH_LIST[number]


    fixture_id = match["fixture"]["id"]


    home = match["teams"]["home"]

    away = match["teams"]["away"]



    home_matches = last_matches(
        home["id"]
    )


    away_matches = last_matches(
        away["id"]
    )


    history = h2h(
        home["id"],
        away["id"]
    )



    home_stats = calculate_stats(
        home_matches,
        home["id"]
    )


    away_stats = calculate_stats(
        away_matches,
        away["id"]
    )



    one_x_two = analyze_1x2(
        home_stats,
        away_stats
    )


    goals = analyze_goals(
        home_stats,
        away_stats
    )


    h2h_data = h2h_analysis(
        history
    )


    picks = [
        one_x_two
    ] + goals



    best, confidence = best_selection(
        picks
    )



    text = f"""
⚽ {home['name']} - {away['name']}

🏆 {match['league']['name']}


📊 Deep Data Ανάλυση


🎯 Σημεία

"""


    for p in picks:

        text += f"✅ {p}\n"



    text += f"""

📈 Φόρμα

{home['name']}:
{team_form(home_matches, home['id'])}


{away['name']}:
{team_form(away_matches, away['id'])}



⚔ Προϊστορία

• G/G: {h2h_data['gg']}/{h2h_data['games']}
• Over 2.5: {h2h_data['over25']}/{h2h_data['games']}
• {home['name']} νίκες: {h2h_data['home']}
• {away['name']} νίκες: {h2h_data['away']}
• Ισοπαλίες: {h2h_data['draw']}



📊 xGoals (Expected Goals)

{home['name']}:
Έλεγχος διαθέσιμων xG δεδομένων


{away['name']}:
Έλεγχος διαθέσιμων xG δεδομένων



💡 Καλύτερη επιλογή

🏆 {best}

📌 Εμπιστοσύνη: {confidence}%

"""



    await update.message.reply_text(
        text
    )







def main():


    app = Application.builder().token(
        TELEGRAM_TOKEN
    ).build()



    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    app.add_handler(
        CommandHandler(
            "today",
            today
        )
    )


    app.add_handler(
        CommandHandler(
            "analyze",
            analyze
        )
    )



    print("Bot running...")


    app.run_polling()





if __name__ == "__main__":

    main()
