# bot.py

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

from config import TELEGRAM_TOKEN

from football_api import (
    search_team,
    get_last_matches,
    get_h2h
)

from analyzer import (
    get_form,
    calculate_goal_stats,
    analyze_1x2,
    analyze_markets,
    analyze_h2h,
    best_pick
)



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        """
⚽ Football Deep Data Bot

Χρήση:

/analyze Ομάδα1 Ομάδα2

Παράδειγμα:
/analyze Liverpool Arsenal
"""
    )



async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) < 2:

        await update.message.reply_text(
            "Χρήση:\n/analyze Liverpool Arsenal"
        )

        return


    team1_name = context.args[0]
    team2_name = context.args[1]


    team1 = search_team(team1_name)
    team2 = search_team(team2_name)


    if not team1 or not team2:

        await update.message.reply_text(
            "❌ Δεν βρέθηκαν οι ομάδες"
        )

        return



    team1_matches = get_last_matches(
        team1["id"],
        10
    )

    team2_matches = get_last_matches(
        team2["id"],
        10
    )


    h2h = get_h2h(
        team1["id"],
        team2["id"]
    )



    team1_stats = calculate_goal_stats(
        team1_matches,
        team1["id"]
    )


    team2_stats = calculate_goal_stats(
        team2_matches,
        team2["id"]
    )



    result_1x2 = analyze_1x2(
        team1_stats,
        team2_stats
    )


    markets = analyze_markets(
        team1_stats,
        team2_stats
    )


    h2h_stats = analyze_h2h(
        h2h
    )


    picks = [
        result_1x2
    ] + markets



    best, confidence = best_pick(
        picks
    )



    text = f"""
⚽ {team1['name']} - {team2['name']}


📊 Deep Data Ανάλυση


🎯 Σημεία

"""


    for pick in picks:

        text += f"✅ {pick}\n"



    text += f"""

📈 Φόρμα

{team1['name']}:
{get_form(team1_matches, team1['id'])}


{team2['name']}:
{get_form(team2_matches, team2['id'])}



⚔ Προϊστορία

• G/G στα {h2h_stats['gg']} τελευταία
• Over 2.5 στα {h2h_stats['over25']} τελευταία
• {team1['name']} νίκες: {h2h_stats['home']}
• {team2['name']} νίκες: {h2h_stats['away']}
• Ισοπαλίες: {h2h_stats['draw']}



📊 xGoals (Expected Goals)

{team1['name']}:
⚽ xG δεδομένα όπου διαθέσιμα


{team2['name']}:
⚽ xG δεδομένα όπου διαθέσιμα



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
            "analyze",
            analyze
        )
    )


    print(
        "Bot started..."
    )


    app.run_polling()



if __name__ == "__main__":

    main()
