import random


def setup_hidden_attributes(player):
    player.setdefault("professionalism", random.randint(50, 99))
    player.setdefault("consistency", random.randint(50, 99))
    player.setdefault("big_game", random.randint(50, 99))
    player.setdefault(
        "personality",
        random.choice(
            [
                "Hard Worker",
                "Natural Talent",
                "Late Bloomer",
                "Big Game Player",
                "Laid Back",
            ]
        ),
    )
    player.setdefault("overall_history", [])
    player.setdefault("injured", False)

    if "career_peak" not in player:
        potential = player.get(
            "potential",
            player.get("overall", 70) + 10,
        )

        missed_potential = random.choices(
            [0, 1, 2, 3, 4],
            weights=[30, 30, 22, 13, 5],
            k=1,
        )[0]

        player["career_peak"] = max(
            player.get("overall", 60),
            potential - missed_potential,
        )


def age_growth(player):
    age = player["age"]
    overall = player["overall"]
    peak = player["career_peak"]
    gap = peak - overall

    if age <= 17:
        growth = random.choices(
            [0, 1, 2, 3, 4],
            weights=[5, 25, 38, 25, 7],
            k=1,
        )[0]

    elif age <= 20:
        growth = random.choices(
            [-1, 0, 1, 2, 3],
            weights=[3, 12, 35, 38, 12],
            k=1,
        )[0]

    elif age <= 23:
        growth = random.choices(
            [-1, 0, 1, 2, 3],
            weights=[5, 18, 40, 30, 7],
            k=1,
        )[0]

    elif age <= 26:
        growth = random.choices(
            [-1, 0, 1, 2],
            weights=[10, 30, 45, 15],
            k=1,
        )[0]

    elif age <= 29:
        growth = random.choices(
            [-1, 0, 1],
            weights=[20, 45, 35],
            k=1,
        )[0]

    elif age == 30:
        growth = random.choices(
            [-2, -1, 0],
            weights=[10, 35, 55],
            k=1,
        )[0]

    elif age == 31:
        growth = random.choices(
            [-2, -1, 0],
            weights=[20, 50, 30],
            k=1,
        )[0]

    elif age == 32:
        growth = random.randint(-3, -1)

    elif age == 33:
        growth = random.randint(-4, -1)

    elif age == 34:
        growth = random.randint(-5, -2)

    elif age == 35:
        growth = random.randint(-6, -2)

    elif age == 36:
        growth = random.randint(-7, -3)

    elif age == 37:
        growth = random.randint(-8, -4)

    else:
        growth = random.randint(-9, -5)

    if age <= 24 and gap >= 10:
        growth += 1

    if age <= 21 and gap >= 18:
        growth += 1

    if gap <= 2 and growth > 0:
        if random.randint(1, 100) <= 75:
            growth = 0

    return growth


def professionalism_effect(player):
    professionalism = player["professionalism"]

    if player["age"] >= 30:
        if professionalism >= 90:
            return 1

        if professionalism <= 60:
            return -1

        return 0

    if professionalism >= 92:
        return random.choice([0, 0, 1])

    if professionalism <= 58:
        return random.choice([-1, 0, 0])

    return 0


def consistency_effect(player):
    consistency = player["consistency"]

    if consistency >= 90:
        return random.choice([0, 0, 0, 1])

    if consistency >= 70:
        return random.choice([-1, 0, 0, 0, 1])

    return random.choice([-1, -1, 0, 0, 1])


def personality_effect(player):
    personality = player["personality"]
    age = player["age"]

    if personality == "Hard Worker":
        if age <= 28:
            return random.choice([0, 0, 1])

        return random.choice([-1, 0])

    if personality == "Natural Talent":
        if age <= 24:
            return random.choice([-1, 0, 1, 2])

        return random.choice([-1, 0, 1])

    if personality == "Late Bloomer":
        if age <= 20:
            return random.choice([-1, 0])

        if 21 <= age <= 27:
            return random.choice([0, 1, 1, 2])

        return 0

    if personality == "Laid Back":
        return random.choice([-1, 0, 0, 0])

    return 0


def injury_effect(player):
    if not player.get("injured", False):
        return 0

    injury_games = player.get("injury_games", 0)

    if injury_games >= 25:
        return -3

    if injury_games >= 12:
        return -2

    return -1


def update_attributes(player, overall_change):
    if overall_change == 0:
        return

    position = player["position"]

    if position == "Goalkeeper":
        positive_stats = [
            "defending",
            "defending",
            "passing",
        ]

    elif position == "Defender":
        positive_stats = [
            "defending",
            "defending",
            "pace",
            "passing",
        ]

    elif position == "Midfielder":
        positive_stats = [
            "passing",
            "passing",
            "shooting",
            "pace",
            "defending",
        ]

    elif position == "Winger":
        positive_stats = [
            "pace",
            "pace",
            "shooting",
            "passing",
        ]

    else:
        positive_stats = [
            "shooting",
            "shooting",
            "pace",
            "passing",
        ]

    if overall_change > 0:
        changes = max(1, overall_change * 2)

        for _ in range(changes):
            stat = random.choice(positive_stats)
            player[stat] = min(
                99,
                player.get(stat, 40) + 1,
            )

    else:
        changes = abs(overall_change)

        for _ in range(changes):
            if player["age"] >= 30:
                stat = random.choices(
                    [
                        "pace",
                        "shooting",
                        "passing",
                        "defending",
                    ],
                    weights=[
                        50,
                        18,
                        14,
                        18,
                    ],
                    k=1,
                )[0]
            else:
                stat = random.choice(positive_stats)

            player[stat] = max(
                30,
                player.get(stat, 40) - 1,
            )


def yearly_development(player):
    setup_hidden_attributes(player)

    old_overall = player["overall"]

    change = age_growth(player)
    change += professionalism_effect(player)
    change += consistency_effect(player)
    change += personality_effect(player)
    change += injury_effect(player)

    if player["age"] <= 29:
        change = max(-2, min(4, change))
    else:
        change = max(-9, min(1, change))

    new_overall = old_overall + change
    new_overall = min(new_overall, player["career_peak"])
    new_overall = max(40, min(99, new_overall))

    actual_change = new_overall - old_overall

    player["overall"] = new_overall

    player["peak_overall"] = max(
        player.get("peak_overall", new_overall),
        new_overall,
    )

    update_attributes(player, actual_change)

    return actual_change