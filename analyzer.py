# analyzer.py

from statistics import mean


def get_form(matches, team_id):

    form = []

    for match in matches:

        home = match["teams"]["home"]
        away = match["teams"]["away"]

        home_goals = match["goals"]["home"]
        away_goals = match["goals"]["away"]

        if home_goals is None or away_goals is None:
            continue


        if team_id == home["id"]:

            if home_goals > away_goals:
                form.append("✅")

            elif home_goals == away_goals:
                form.append("➖")

            else:
                form.append("❌")


        else:

            if away_goals > home_goals:
                form.append("✅")

            elif away_goals == home_goals:
                form.append("➖")

            else:
                form.append("❌")


    return "".join(form)



def calculate_goal_stats(matches, team_id):

    goals_for = []
    goals_against = []

    gg = 0
    ng = 0

    over15 = 0
    over25 = 0
    over35 = 0

    under15 = 0
    under25 = 0
    under35 = 0


    total_games = 0


    for match in matches:

        home = match["teams"]["home"]
        away = match["teams"]["away"]

        hg = match["goals"]["home"]
        ag = match["goals"]["away"]


        if hg is None or ag is None:
            continue


        total_games += 1


        if team_id == home["id"]:
            gf = hg
            ga = ag

        else:
            gf = ag
            ga = hg



        goals_for.append(gf)
        goals_against.append(ga)


        total = hg + ag


        if hg > 0 and ag > 0:
            gg += 1
        else:
            ng += 1


        if total >= 2:
            over15 += 1
        else:
            under15 += 1


        if total >= 3:
            over25 += 1
        else:
            under25 += 1


        if total >= 4:
            over35 += 1
        else:
            under35 += 1



    return {

        "games": total_games,

        "avg_for": round(mean(goals_for),2)
        if goals_for else 0,

        "avg_against": round(mean(goals_against),2)
        if goals_against else 0,


        "gg": gg,
        "ng": ng,

        "over15": over15,
        "over25": over25,
        "over35": over35,

        "under15": under15,
        "under25": under25,
        "under35": under35
    }



def analyze_1x2(home_stats, away_stats):

    home_power = (
        home_stats["avg_for"]
        -
        home_stats["avg_against"]
    )


    away_power = (
        away_stats["avg_for"]
        -
        away_stats["avg_against"]
    )


    if home_power > away_power + 0.4:
        return "1"

    elif away_power > home_power + 0.4:
        return "2"

    else:
        return "Χ"



def analyze_markets(home_stats, away_stats):

    picks = []


    avg_goals = (
        home_stats["avg_for"]
        +
        away_stats["avg_for"]
    )


    # Over

    if avg_goals >= 1.8:
        picks.append("Over 1.5")


    if avg_goals >= 2.5:
        picks.append("Over 2.5")


    if avg_goals >= 3.3:
        picks.append("Over 3.5")



    # Under

    if avg_goals < 2:
        picks.append("Under 2.5")


    if avg_goals < 3:
        picks.append("Under 3.5")



    # GG

    gg_total = (
        home_stats["gg"]
        +
        away_stats["gg"]
    )


    if gg_total >= 6:
        picks.append("G/G")

    else:
        picks.append("N/G")


    return picks



def analyze_h2h(matches):

    result = {

        "gg":0,
        "over25":0,
        "home":0,
        "away":0,
        "draw":0
    }


    for m in matches:

        hg = m["goals"]["home"]
        ag = m["goals"]["away"]


        if hg is None or ag is None:
            continue


        if hg > 0 and ag > 0:
            result["gg"] += 1


        if hg + ag >= 3:
            result["over25"] += 1


        if hg > ag:
            result["home"] += 1

        elif ag > hg:
            result["away"] += 1

        else:
            result["draw"] += 1


    return result



def best_pick(picks):

    if "G/G" in picks and "Over 2.5" in picks:
        return "G/G & Over 2.5", 78


    if "Over 2.5" in picks:
        return "Over 2.5", 72


    if "G/G" in picks:
        return "G/G", 70


    return picks[0], 65
