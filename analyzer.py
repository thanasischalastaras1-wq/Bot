# analyzer.py

from statistics import mean



def team_form(matches, team_id):

    form = []

    for match in matches:

        home_id = match["teams"]["home"]["id"]
        away_id = match["teams"]["away"]["id"]

        home_goals = match["goals"]["home"]
        away_goals = match["goals"]["away"]


        if home_goals is None or away_goals is None:
            continue


        if team_id == home_id:

            if home_goals > away_goals:
                form.append("✅")

            elif home_goals == away_goals:
                form.append("➖")

            else:
                form.append("❌")


        elif team_id == away_id:

            if away_goals > home_goals:
                form.append("✅")

            elif away_goals == home_goals:
                form.append("➖")

            else:
                form.append("❌")


    return "".join(form[-5:])




def calculate_stats(matches, team_id):

    scored = []
    conceded = []

    gg = 0
    over15 = 0
    over25 = 0
    over35 = 0


    games = 0


    for match in matches:

        hg = match["goals"]["home"]
        ag = match["goals"]["away"]


        if hg is None or ag is None:
            continue


        games += 1


        if match["teams"]["home"]["id"] == team_id:

            scored.append(hg)
            conceded.append(ag)

        else:

            scored.append(ag)
            conceded.append(hg)



        if hg > 0 and ag > 0:
            gg += 1


        total = hg + ag


        if total >= 2:
            over15 += 1

        if total >= 3:
            over25 += 1

        if total >= 4:
            over35 += 1



    return {

        "games": games,

        "avg_scored":
            round(mean(scored),2)
            if scored else 0,

        "avg_conceded":
            round(mean(conceded),2)
            if conceded else 0,


        "gg": gg,

        "over15": over15,
        "over25": over25,
        "over35": over35

    }




def analyze_1x2(home, away):

    home_strength = (
        home["avg_scored"]
        -
        home["avg_conceded"]
    )


    away_strength = (
        away["avg_scored"]
        -
        away["avg_conceded"]
    )


    if home_strength > away_strength + 0.30:
        return "1"


    if away_strength > home_strength + 0.30:
        return "2"


    return "Χ"





def analyze_goals(home, away):

    picks = []


    avg_goals = (

        home["avg_scored"]
        +
        away["avg_scored"]

    )


    if avg_goals >= 1.8:
        picks.append("Over 1.5")


    if avg_goals >= 2.5:
        picks.append("Over 2.5")


    if avg_goals >= 3.5:
        picks.append("Over 3.5")



    if avg_goals < 2:
        picks.append("Under 2.5")


    if avg_goals < 3:
        picks.append("Under 3.5")



    total_gg = (
        home["gg"]
        +
        away["gg"]
    )


    if total_gg >= 6:
        picks.append("G/G")

    else:
        picks.append("N/G")


    return picks





def h2h_analysis(matches):

    data = {

        "games":0,
        "gg":0,
        "over25":0,
        "home":0,
        "away":0,
        "draw":0
    }



    for match in matches:

        hg = match["goals"]["home"]
        ag = match["goals"]["away"]


        if hg is None or ag is None:
            continue


        data["games"] += 1


        if hg > 0 and ag > 0:
            data["gg"] += 1


        if hg + ag >= 3:
            data["over25"] += 1



        if hg > ag:
            data["home"] += 1

        elif ag > hg:
            data["away"] += 1

        else:
            data["draw"] += 1



    return data






def best_selection(picks):


    if "G/G" in picks and "Over 2.5" in picks:

        return (
            "G/G & Over 2.5",
            78
        )


    if "Over 2.5" in picks:

        return (
            "Over 2.5",
            72
        )


    if "G/G" in picks:

        return (
            "G/G",
            70
        )


    return (
        picks[0],
        65
    )
