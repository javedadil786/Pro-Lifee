import random

from clubs import clubs


def get_club_strength(club_name):
    for club in clubs:
        if club.get("name") == club_name:
            return club.get(
                "rating",
                club.get("reputation", 70),
            )

    return 70


def get_club_style(club_name):
    for club in clubs:
        if club.get("name") == club_name:
            return club.get("style", "Balanced")

    return "Balanced"


def performance_modifier(player):
    modifier = 1.0
    consistency = player.get("consistency", 70)

    if consistency >= 90:
        modifier += 0.08
    elif consistency < 60:
        modifier -= 0.10

    personality = player.get("personality", "")

    if personality == "Hard Worker":
        modifier += 0.05
    elif personality == "Laid Back":
        modifier -= 0.05

    if player.get("injured", False):
        modifier -= 0.15

    modifier += random.uniform(-0.15, 0.15)

    return max(0.60, min(1.25, modifier))


def calculate_matches(player, overall, club_strength):
    required_level = club_strength - 10
    difference = overall - required_level

    if difference <= -10:
        matches = random.randint(3, 12)
    elif difference <= -5:
        matches = random.randint(8, 20)
    elif difference <= 0:
        matches = random.randint(15, 30)
    elif difference <= 5:
        matches = random.randint(24, 38)
    else:
        matches = random.randint(32, 48)

    role = player.get("squad_role", "First Team")

    if role == "Prospect":
        matches -= random.randint(5, 12)
    elif role == "Rotation":
        matches -= random.randint(2, 7)
    elif role in ["Star Player", "Superstar"]:
        matches += random.randint(2, 5)

    if player.get("injured", False):
        matches -= player.get(
            "injury_games",
            random.randint(3, 10),
        )

    return max(0, min(55, matches))


def striker_stats(player, matches, overall, club_style):
    if matches == 0:
        return 0, 0

    if overall < 68:
        goal_rate = 0.10
    elif overall < 73:
        goal_rate = 0.18
    elif overall < 78:
        goal_rate = 0.27
    elif overall < 83:
        goal_rate = 0.38
    elif overall < 88:
        goal_rate = 0.50
    elif overall < 92:
        goal_rate = 0.62
    else:
        goal_rate = 0.72

    if club_style == "Attacking":
        goal_rate += 0.06
    elif club_style == "Possession":
        goal_rate += 0.03
    elif club_style == "Defensive":
        goal_rate -= 0.06

    modifier = performance_modifier(player)

    goals = round(matches * goal_rate * modifier)
    goals += random.randint(-3, 3)
    goals = max(0, min(matches, goals))

    assist_rate = random.uniform(0.10, 0.25)
    assists = round(matches * assist_rate * modifier)
    assists = max(0, min(18, assists))

    return goals, assists


def winger_stats(player, matches, overall, club_style):
    if matches == 0:
        return 0, 0

    goal_rate = max(0.08, (overall - 55) / 100)
    assist_rate = max(0.12, (overall - 50) / 95)

    if club_style == "Attacking":
        goal_rate += 0.04
        assist_rate += 0.04
    elif club_style == "Defensive":
        goal_rate -= 0.04
        assist_rate -= 0.03

    modifier = performance_modifier(player)

    goals = round(matches * goal_rate * modifier)
    assists = round(matches * assist_rate * modifier)

    goals += random.randint(-2, 2)
    assists += random.randint(-2, 2)

    return max(0, min(30, goals)), max(0, min(20, assists))


def midfielder_stats(player, matches, overall, club_style):
    if matches == 0:
        return 0, 0

    goal_rate = max(0.04, (overall - 62) / 150)
    assist_rate = max(0.10, (overall - 52) / 105)

    if club_style == "Possession":
        assist_rate += 0.06
    elif club_style == "Attacking":
        goal_rate += 0.03

    modifier = performance_modifier(player)

    goals = round(matches * goal_rate * modifier)
    assists = round(matches * assist_rate * modifier)

    goals += random.randint(-2, 2)
    assists += random.randint(-2, 2)

    return max(0, min(20, goals)), max(0, min(20, assists))


def defender_stats(player, matches, overall, club_strength):
    if matches == 0:
        return 0, 0, 0

    modifier = performance_modifier(player)

    goals = random.randint(0, max(1, matches // 10))
    assists = random.randint(0, max(1, matches // 8))

    clean_rate = (club_strength - 55) / 100
    clean_sheets = round(matches * clean_rate * modifier)
    clean_sheets = max(0, min(matches, clean_sheets))

    return goals, assists, clean_sheets


def goalkeeper_stats(player, matches, overall, club_strength):
    if matches == 0:
        return 0, 0

    modifier = performance_modifier(player)

    saves = round(
        matches
        * random.uniform(2.0, 4.5)
        * modifier
    )

    clean_rate = (
        club_strength
        + overall
        - 120
    ) / 140

    clean_sheets = round(
        matches
        * clean_rate
        * modifier
    )

    return (
        max(0, min(250, saves)),
        max(0, min(matches, clean_sheets)),
    )


def calculate_rating(
    player,
    matches,
    goals,
    assists,
    saves,
    clean_sheets,
):
    if matches == 0:
        return 5.8

    overall = player.get("overall", 60)
    position = player.get("position", "Striker")

    rating = 5.8
    rating += (overall - 60) / 35

    if position == "Goalkeeper":
        rating += (
            saves / max(matches, 1)
        ) * 0.15
        rating += (
            clean_sheets / max(matches, 1)
        ) * 0.8

    elif position == "Defender":
        rating += (
            clean_sheets / max(matches, 1)
        ) * 0.6
        rating += goals * 0.04
        rating += assists * 0.03

    else:
        rating += (
            goals / max(matches, 1)
        ) * 1.3
        rating += (
            assists / max(matches, 1)
        ) * 0.9

    if player.get("injured", False):
        rating -= 0.25

    rating += random.uniform(-0.25, 0.25)

    return round(
        max(5.5, min(9.5, rating)),
        1,
    )


def simulate_season(player):
    position = player.get("position", "Striker")
    overall = player.get("overall", 60)

    club_strength = get_club_strength(
        player.get("club", "")
    )
    club_style = get_club_style(
        player.get("club", "")
    )

    matches = calculate_matches(
        player,
        overall,
        club_strength,
    )

    goals = 0
    assists = 0
    saves = 0
    clean_sheets = 0

    if position == "Goalkeeper":
        saves, clean_sheets = goalkeeper_stats(
            player,
            matches,
            overall,
            club_strength,
        )

    elif position == "Defender":
        goals, assists, clean_sheets = defender_stats(
            player,
            matches,
            overall,
            club_strength,
        )

    elif position == "Midfielder":
        goals, assists = midfielder_stats(
            player,
            matches,
            overall,
            club_style,
        )

    elif position == "Winger":
        goals, assists = winger_stats(
            player,
            matches,
            overall,
            club_style,
        )

    else:
        goals, assists = striker_stats(
            player,
            matches,
            overall,
            club_style,
        )

    rating = calculate_rating(
        player,
        matches,
        goals,
        assists,
        saves,
        clean_sheets,
    )

    player["season_matches"] = matches
    player["season_goals"] = goals
    player["season_assists"] = assists
    player["season_saves"] = saves
    player["season_clean_sheets"] = clean_sheets
    player["season_rating"] = rating

    player["career_matches"] = (
        player.get("career_matches", 0)
        + matches
    )

    player["career_goals"] = (
        player.get("career_goals", 0)
        + goals
    )

    player["career_assists"] = (
        player.get("career_assists", 0)
        + assists
    )

    player["career_rating_total"] = (
        player.get("career_rating_total", 0.0)
        + rating
    )

    player["career_rating_seasons"] = (
        player.get("career_rating_seasons", 0)
        + 1
    )

    print()
    print("==========================")
    print("SEASON STATS")
    print("==========================")
    print(f"Matches: {matches}")

    if position == "Goalkeeper":
        print(f"Saves: {saves}")
        print(f"Clean Sheets: {clean_sheets}")
    else:
        print(f"Goals: {goals}")
        print(f"Assists: {assists}")

        if position == "Defender":
            print(f"Clean Sheets: {clean_sheets}")

    print(f"Average Rating: {rating}")