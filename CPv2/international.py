import random


NATION_STRENGTHS = {
    "Argentina": 95,
    "France": 95,
    "Spain": 94,
    "England": 93,
    "Brazil": 93,
    "Portugal": 91,
    "Germany": 91,
    "Netherlands": 89,
    "Italy": 89,
    "Belgium": 86,
    "Croatia": 85,
    "Uruguay": 85,
    "Morocco": 84,
    "Colombia": 83,
    "Japan": 81,
    "United States": 80,
    "Mexico": 80,
    "Denmark": 80,
    "Switzerland": 80,
    "Austria": 79,
    "Turkey": 79,
    "Senegal": 79,
    "Norway": 78,
    "Sweden": 78,
    "Poland": 77,
    "Serbia": 77,
    "Scotland": 76,
    "Wales": 75,
    "Republic Of Ireland": 73,
}

EUROPEAN_NATIONS = {
    "England",
    "France",
    "Spain",
    "Germany",
    "Portugal",
    "Italy",
    "Netherlands",
    "Belgium",
    "Croatia",
    "Denmark",
    "Switzerland",
    "Austria",
    "Turkey",
    "Norway",
    "Sweden",
    "Poland",
    "Serbia",
    "Scotland",
    "Wales",
    "Republic Of Ireland",
}


def setup_international_stats(player):
    player.setdefault("international_caps", 0)
    player.setdefault("international_goals", 0)
    player.setdefault("international_assists", 0)
    player.setdefault("international_saves", 0)
    player.setdefault("international_clean_sheets", 0)
    player.setdefault("world_cups", 0)
    player.setdefault("euros", 0)
    player.setdefault("world_cup_appearances", 0)
    player.setdefault("euros_appearances", 0)
    player.setdefault("won_world_cup_this_season", False)
    player.setdefault("won_euros_this_season", False)


def get_nation_strength(nationality):
    return NATION_STRENGTHS.get(nationality, 72)


def selected_for_country(player):
    overall = player.get("overall", 60)
    nationality = player.get("nationality", "")
    nation_strength = get_nation_strength(nationality)

    if nation_strength >= 92:
        required_overall = 82
    elif nation_strength >= 87:
        required_overall = 79
    elif nation_strength >= 82:
        required_overall = 76
    elif nation_strength >= 77:
        required_overall = 72
    else:
        required_overall = 68

    if player.get("season_rating", 0) >= 8.0:
        required_overall -= 2

    if player.get("position") == "Goalkeeper":
        if player.get("season_clean_sheets", 0) >= 15:
            required_overall -= 1
    else:
        if player.get("season_goals", 0) >= 20:
            required_overall -= 1
        if player.get("season_assists", 0) >= 12:
            required_overall -= 1

    if player.get("injured", False):
        return False

    if overall < required_overall:
        return False

    selection_chance = 75

    if overall >= required_overall + 5:
        selection_chance = 90

    if overall >= required_overall + 9:
        selection_chance = 98

    return random.randint(1, 100) <= selection_chance


def tournament_matches(player):
    overall = player.get("overall", 60)

    if overall >= 90:
        return random.randint(5, 7)

    if overall >= 84:
        return random.randint(4, 7)

    if overall >= 78:
        return random.randint(2, 6)

    return random.randint(1, 4)


def simulate_international_stats(player, matches):
    position = player.get("position", "Striker")
    overall = player.get("overall", 60)

    goals = 0
    assists = 0
    saves = 0
    clean_sheets = 0

    if position == "Goalkeeper":
        saves = round(
            matches
            * random.uniform(2.0, 4.5)
        )

        clean_sheet_chance = max(
            0.12,
            min(0.55, (overall - 50) / 90),
        )

        clean_sheets = round(
            matches
            * clean_sheet_chance
            * random.uniform(0.75, 1.20)
        )

        clean_sheets = max(
            0,
            min(matches, clean_sheets),
        )

    elif position == "Defender":
        goals = random.randint(
            0,
            max(1, matches // 4),
        )
        assists = random.randint(
            0,
            max(1, matches // 3),
        )

    elif position == "Midfielder":
        goal_rate = max(
            0.05,
            (overall - 65) / 100,
        )
        assist_rate = max(
            0.10,
            (overall - 55) / 85,
        )

        goals = round(
            matches
            * goal_rate
            * random.uniform(0.65, 1.20)
        )
        assists = round(
            matches
            * assist_rate
            * random.uniform(0.65, 1.20)
        )

    elif position == "Winger":
        goal_rate = max(
            0.10,
            (overall - 55) / 80,
        )
        assist_rate = max(
            0.12,
            (overall - 52) / 78,
        )

        goals = round(
            matches
            * goal_rate
            * random.uniform(0.65, 1.20)
        )
        assists = round(
            matches
            * assist_rate
            * random.uniform(0.65, 1.20)
        )

    else:
        goal_rate = max(
            0.12,
            (overall - 50) / 70,
        )

        goals = round(
            matches
            * goal_rate
            * random.uniform(0.65, 1.20)
        )
        assists = random.randint(
            0,
            max(1, matches // 2),
        )

    goals = max(0, min(matches + 2, goals))
    assists = max(0, min(matches + 1, assists))

    player["international_caps"] += matches
    player["international_goals"] += goals
    player["international_assists"] += assists
    player["international_saves"] += saves
    player["international_clean_sheets"] += clean_sheets

    return {
        "matches": matches,
        "goals": goals,
        "assists": assists,
        "saves": saves,
        "clean_sheets": clean_sheets,
    }


def tournament_win_chance(player):
    nation_strength = get_nation_strength(
        player.get("nationality", "")
    )
    overall = player.get("overall", 60)

    if nation_strength >= 94:
        chance = 16
    elif nation_strength >= 90:
        chance = 11
    elif nation_strength >= 86:
        chance = 7
    elif nation_strength >= 82:
        chance = 4
    elif nation_strength >= 77:
        chance = 2
    else:
        chance = 1

    if overall >= 88:
        chance += 2

    if overall >= 93:
        chance += 2

    if player.get("season_rating", 0) >= 8.2:
        chance += 1

    return min(chance, 20)


def display_tournament_stats(player, tournament, stats):
    print()
    print("==============================")
    print(f"{tournament.upper()} STATS")
    print("==============================")
    print(f"Country: {player['nationality']}")
    print(f"Appearances: {stats['matches']}")

    if player["position"] == "Goalkeeper":
        print(f"Saves: {stats['saves']}")
        print(f"Clean Sheets: {stats['clean_sheets']}")
    else:
        print(f"Goals: {stats['goals']}")
        print(f"Assists: {stats['assists']}")


def play_world_cup(player):
    print()
    print("==============================")
    print("          WORLD CUP")
    print("==============================")

    if not selected_for_country(player):
        print(
            f"You were not selected for "
            f"{player['nationality']}."
        )
        return

    print(
        f"You were selected for "
        f"{player['nationality']}!"
    )

    player["world_cup_appearances"] += 1

    matches = tournament_matches(player)
    stats = simulate_international_stats(
        player,
        matches,
    )

    display_tournament_stats(
        player,
        "World Cup",
        stats,
    )

    if (
        random.randint(1, 100)
        <= tournament_win_chance(player)
    ):
        player["world_cups"] += 1
        player["won_world_cup_this_season"] = True

        print()
        print("YOU WON THE WORLD CUP!")
    else:
        print()
        print(
            f"{player['nationality']} "
            f"did not win the World Cup."
        )


def play_euros(player):
    nationality = player.get(
        "nationality",
        "",
    )

    if nationality not in EUROPEAN_NATIONS:
        return

    print()
    print("==============================")
    print("             EUROS")
    print("==============================")

    if not selected_for_country(player):
        print(
            f"You were not selected for "
            f"{nationality}."
        )
        return

    print(
        f"You were selected for "
        f"{nationality}!"
    )

    player["euros_appearances"] += 1

    matches = tournament_matches(player)
    stats = simulate_international_stats(
        player,
        matches,
    )

    display_tournament_stats(
        player,
        "Euros",
        stats,
    )

    chance = min(
        tournament_win_chance(player) + 2,
        22,
    )

    if random.randint(1, 100) <= chance:
        player["euros"] += 1
        player["won_euros_this_season"] = True

        print()
        print("YOU WON THE EUROS!")
    else:
        print()
        print(
            f"{nationality} "
            f"did not win the Euros."
        )


def international_tournament(player):
    setup_international_stats(player)

    player["won_world_cup_this_season"] = False
    player["won_euros_this_season"] = False

    season = player.get("season", 1)

    if season % 4 == 0:
        play_world_cup(player)
        return

    if season % 4 == 2:
        play_euros(player)