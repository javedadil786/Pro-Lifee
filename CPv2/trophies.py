import random

from clubs import clubs


def find_club(club_name):
    for club in clubs:
        if club.get("name") == club_name:
            return club

    return None


def get_club_rating(player):
    club = find_club(
        player.get("club", "")
    )

    if club is None:
        return 70

    return club.get(
        "rating",
        club.get("reputation", 70),
    )


def get_club_europe(player):
    club = find_club(
        player.get("club", "")
    )

    if club is None:
        return "None"

    return club.get("europe", "None")


def simulate_trophies(player):
    player["won_league_this_season"] = False
    player["won_cup_this_season"] = False
    player["won_ucl_this_season"] = False

    league_title(player)
    domestic_cup(player)
    champions_league(player)


def league_title(player):
    rating = get_club_rating(player)

    if rating >= 96:
        chance = 45
    elif rating >= 93:
        chance = 35
    elif rating >= 90:
        chance = 25
    elif rating >= 87:
        chance = 17
    elif rating >= 84:
        chance = 10
    elif rating >= 80:
        chance = 5
    else:
        chance = 2

    if player.get("overall", 60) >= 88:
        chance += 3

    if player.get("season_rating", 0) >= 8.0:
        chance += 2

    chance = min(chance, 50)

    if random.randint(1, 100) <= chance:
        player["league_titles"] = (
            player.get("league_titles", 0)
            + 1
        )
        player["won_league_this_season"] = True
        print("Won the League Title!")


def domestic_cup(player):
    rating = get_club_rating(player)

    if rating >= 94:
        chance = 28
    elif rating >= 90:
        chance = 22
    elif rating >= 86:
        chance = 16
    elif rating >= 82:
        chance = 11
    elif rating >= 78:
        chance = 7
    else:
        chance = 4

    if player.get("season_rating", 0) >= 8.0:
        chance += 2

    chance = min(chance, 32)

    if random.randint(1, 100) <= chance:
        player["domestic_cups"] = (
            player.get("domestic_cups", 0)
            + 1
        )
        player["won_cup_this_season"] = True
        print("Won the Domestic Cup!")


def champions_league(player):
    rating = get_club_rating(player)
    europe = get_club_europe(player)

    if rating < 87 and europe != "UCL":
        return

    if rating >= 97:
        chance = 20
    elif rating >= 94:
        chance = 15
    elif rating >= 91:
        chance = 10
    elif rating >= 88:
        chance = 6
    else:
        chance = 3

    if player.get("overall", 60) >= 90:
        chance += 2

    if player.get("season_rating", 0) >= 8.2:
        chance += 2

    if player.get("position") == "Goalkeeper":
        if player.get("season_clean_sheets", 0) >= 18:
            chance += 2
    else:
        if player.get("season_goals", 0) >= 25:
            chance += 2

    chance = min(chance, 24)

    if random.randint(1, 100) <= chance:
        player["champions_leagues"] = (
            player.get("champions_leagues", 0)
            + 1
        )
        player["won_ucl_this_season"] = True
        print("Won the UEFA Champions League!")


def golden_boot(player):
    if player.get("position") == "Goalkeeper":
        return

    goals = player.get("season_goals", 0)

    if goals < 25:
        return

    if goals >= 40:
        chance = 75
    elif goals >= 34:
        chance = 50
    elif goals >= 29:
        chance = 30
    else:
        chance = 15

    if random.randint(1, 100) <= chance:
        player["golden_boots"] = (
            player.get("golden_boots", 0)
            + 1
        )
        print("Won the Golden Boot!")


def team_of_season(player):
    rating = player.get("season_rating", 0)

    if rating >= 8.4:
        chance = 75
    elif rating >= 8.0:
        chance = 45
    elif rating >= 7.7:
        chance = 20
    else:
        chance = 0

    if chance and random.randint(1, 100) <= chance:
        player["team_of_seasons"] = (
            player.get("team_of_seasons", 0)
            + 1
        )
        print("Named in Team of the Season!")


def ballon_dor(player):
    overall = player.get("overall", 60)
    rating = player.get("season_rating", 0)
    position = player.get("position", "Striker")

    if overall < 87 or rating < 7.9:
        return

    score = 0

    score += max(0, overall - 86) * 2
    score += max(0, rating - 7.8) * 20

    if position == "Goalkeeper":
        clean_sheets = player.get(
            "season_clean_sheets",
            0,
        )
        saves = player.get(
            "season_saves",
            0,
        )

        if clean_sheets >= 18:
            score += 12
        if clean_sheets >= 24:
            score += 10
        if saves >= 150:
            score += 8
    else:
        goals = player.get("season_goals", 0)
        assists = player.get("season_assists", 0)

        if goals >= 20:
            score += 8
        if goals >= 30:
            score += 10
        if goals >= 40:
            score += 10
        if assists >= 12:
            score += 6
        if assists >= 18:
            score += 6

    if player.get("won_league_this_season", False):
        score += 8

    if player.get("won_cup_this_season", False):
        score += 4

    if player.get("won_ucl_this_season", False):
        score += 18

    if player.get("won_world_cup_this_season", False):
        score += 22

    if player.get("won_euros_this_season", False):
        score += 14

    major_trophy = (
        player.get("won_league_this_season", False)
        or player.get("won_ucl_this_season", False)
        or player.get("won_world_cup_this_season", False)
        or player.get("won_euros_this_season", False)
    )

    if not major_trophy:
        score -= 20

    chance = max(
        0,
        min(30, int(score / 3)),
    )

    if random.randint(1, 100) <= chance:
        player["ballon_dors"] = (
            player.get("ballon_dors", 0)
            + 1
        )
        print("YOU WON THE BALLON D'OR!")


def season_awards(player):
    print()
    print("==========================")
    print("SEASON AWARDS")
    print("==========================")

    simulate_trophies(player)
    golden_boot(player)
    team_of_season(player)
    ballon_dor(player)

    print()
    print(f"League Titles: {player.get('league_titles', 0)}")
    print(f"Domestic Cups: {player.get('domestic_cups', 0)}")
    print(
        f"Champions Leagues: "
        f"{player.get('champions_leagues', 0)}"
    )
    print(f"World Cups: {player.get('world_cups', 0)}")
    print(f"Euros: {player.get('euros', 0)}")
    print(f"Ballon d'Ors: {player.get('ballon_dors', 0)}")
    print(f"Golden Boots: {player.get('golden_boots', 0)}")
    print(
        f"Team of the Seasons: "
        f"{player.get('team_of_seasons', 0)}"
    )