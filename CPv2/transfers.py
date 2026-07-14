import random

from clubs import clubs


def club_name(club):
    return club.get("name", "Unknown Club")


def club_league(club):
    return club.get("league", "Unknown League")


def club_rating(club):
    return int(
        club.get(
            "rating",
            club.get("reputation", 70),
        )
    )


def club_budget(club):
    return int(club.get("budget", 40))


def is_wonderkid(player):
    return (
        player.get("age", 30) <= 21
        and player.get("overall", 0) >= 77
        and player.get("potential", 0) >= 88
    )


def had_great_season(player):
    rating = player.get("season_rating", 0)

    if player.get("position") == "Goalkeeper":
        return (
            player.get("season_clean_sheets", 0) >= 15
            or player.get("season_saves", 0) >= 135
            or rating >= 7.8
        )

    return (
        player.get("season_goals", 0) >= 20
        or player.get("season_assists", 0) >= 12
        or rating >= 8.0
    )


def player_reputation(player):
    reputation = player.get("overall", 60) * 2
    reputation += int(
        player.get("season_rating", 6.0) * 5
    )

    if player.get("position") == "Goalkeeper":
        reputation += (
            player.get("season_clean_sheets", 0) * 2
        )
        reputation += (
            player.get("season_saves", 0) // 20
        )
    else:
        reputation += (
            player.get("season_goals", 0) * 2
        )
        reputation += player.get(
            "season_assists",
            0,
        )

    reputation += (
        player.get("league_titles", 0) * 3
    )
    reputation += (
        player.get("champions_leagues", 0) * 8
    )
    reputation += (
        player.get("ballon_dors", 0) * 15
    )

    if is_wonderkid(player):
        reputation += 20

    if had_great_season(player):
        reputation += 15

    if player.get("injured", False):
        reputation -= 20

    if player.get("age", 18) >= 33:
        reputation -= 10

    return max(0, reputation)


def club_wants_player(club, player):
    rating = club_rating(club)
    overall = player.get("overall", 60)
    age = player.get("age", 18)
    reputation = player_reputation(player)

    if rating >= 94:
        return (
            overall >= 87
            or (
                is_wonderkid(player)
                and overall >= 80
            )
            or (
                had_great_season(player)
                and overall >= 83
            )
            or reputation >= 235
        )

    if rating >= 89:
        return (
            overall >= 82
            or (
                is_wonderkid(player)
                and overall >= 77
            )
            or (
                had_great_season(player)
                and overall >= 79
            )
            or reputation >= 205
        )

    if rating >= 84:
        return (
            overall >= 77
            or is_wonderkid(player)
            or reputation >= 175
        )

    if rating >= 79:
        return overall >= 70

    if age >= 35 and overall >= 84:
        return False

    return overall >= 60


def calculate_transfer_fee(player, buying_club):
    overall = player.get("overall", 60)
    age = player.get("age", 18)
    potential = player.get("potential", overall)

    if overall < 68:
        low, high = 1, 4
    elif overall < 72:
        low, high = 2, 8
    elif overall < 76:
        low, high = 5, 15
    elif overall < 80:
        low, high = 9, 25
    elif overall < 84:
        low, high = 17, 42
    elif overall < 88:
        low, high = 30, 65
    elif overall < 91:
        low, high = 50, 90
    elif overall < 94:
        low, high = 70, 115
    else:
        low, high = 90, 140

    fee = random.randint(low, high)

    if age <= 21 and potential >= 88:
        fee += random.randint(5, 18)

    if had_great_season(player):
        fee += random.randint(3, 12)

    if age >= 30:
        fee -= random.randint(2, 8)

    if age >= 33:
        fee -= random.randint(4, 12)

    if age >= 36:
        fee -= random.randint(5, 15)

    if player.get("injured", False):
        fee -= random.randint(3, 10)

    rating = club_rating(buying_club)
    budget = club_budget(buying_club)

    if rating < 79:
        fee = min(fee, 30)
    elif rating < 84:
        fee = min(fee, 50)
    elif rating < 89:
        fee = min(fee, 80)
    elif rating < 94:
        fee = min(fee, 110)
    else:
        fee = min(fee, 150)

    fee = min(fee, budget)

    if fee >= 100:
        huge_move = (
            overall >= 91
            or is_wonderkid(player)
            or had_great_season(player)
        )

        if not huge_move:
            fee = random.randint(70, 95)
        elif random.randint(1, 100) > 35:
            fee = random.randint(80, 99)

    return max(1, int(fee))


def generate_contract(player, club):
    overall = player.get("overall", 60)
    age = player.get("age", 18)
    rating = club_rating(club)

    if age >= 35:
        years = random.randint(1, 2)
    elif age >= 31:
        years = random.randint(1, 3)
    elif overall < 75:
        years = random.randint(2, 4)
    else:
        years = random.randint(3, 5)

    if overall < 68:
        wage = random.randint(3, 10) * 1000
        role = "Prospect"
    elif overall < 73:
        wage = random.randint(8, 22) * 1000
        role = "Prospect"
    elif overall < 78:
        wage = random.randint(18, 45) * 1000
        role = "Rotation"
    elif overall < 83:
        wage = random.randint(35, 85) * 1000
        role = "First Team"
    elif overall < 87:
        wage = random.randint(65, 145) * 1000
        role = "Starter"
    elif overall < 91:
        wage = random.randint(110, 230) * 1000
        role = "Star Player"
    else:
        wage = random.randint(180, 380) * 1000
        role = "Superstar"

    if rating >= 94:
        wage = int(wage * 1.2)
    elif rating >= 89:
        wage = int(wage * 1.1)

    return years, wage, role


def add_club_to_history(player, name):
    history = player.setdefault(
        "clubs_history",
        ["Youth Academy"],
    )

    if name not in history:
        history.append(name)


def build_offer(player, club, fee=None):
    if fee is None:
        fee = calculate_transfer_fee(
            player,
            club,
        )

    years, wage, role = generate_contract(
        player,
        club,
    )

    return {
        "club_name": club_name(club),
        "league": club_league(club),
        "rating": club_rating(club),
        "fee": fee,
        "contract_years": years,
        "weekly_wage": wage,
        "squad_role": role,
    }


def first_professional_offer(player):
    overall = player.get("overall", 60)

    possible = [
        club
        for club in clubs
        if club_rating(club) <= overall + 18
    ]

    if not possible:
        possible = sorted(
            clubs,
            key=club_rating,
        )[:10]

    if not possible:
        return []

    chosen = random.choice(possible)

    # Academy moves are represented as free first contracts.
    return [
        build_offer(
            player,
            chosen,
            fee=0,
        )
    ]


def transfer_interest_chance(player):
    overall = player.get("overall", 60)
    age = player.get("age", 18)

    chance = 18

    if overall >= 72:
        chance += 5
    if overall >= 78:
        chance += 7
    if overall >= 83:
        chance += 8
    if overall >= 88:
        chance += 8
    if overall >= 92:
        chance += 5

    if is_wonderkid(player):
        chance += 10

    if had_great_season(player):
        chance += 12

    if player.get("injured", False):
        chance -= 18

    if age >= 31:
        chance -= 5
    if age >= 34:
        chance -= 10
    if age >= 37:
        chance -= 15

    return max(5, min(65, chance))


def generate_web_transfer_offers(
    player,
    completed_season,
):
    if player.get("club") in [
        "Youth Academy",
        "Local Academy",
    ]:
        return first_professional_offer(player)

    if completed_season % 2 != 0:
        return []

    last_transfer = player.get(
        "last_transfer_season",
        -100,
    )

    if completed_season - last_transfer < 2:
        return []

    if (
        random.randint(1, 100)
        > transfer_interest_chance(player)
    ):
        return []

    candidates = clubs[:]
    random.shuffle(candidates)

    offers = []

    for club in candidates:
        if club_name(club) == player.get("club"):
            continue

        if not club_wants_player(
            club,
            player,
        ):
            continue

        bid_chance = 14

        if had_great_season(player):
            bid_chance += 8

        if is_wonderkid(player):
            bid_chance += 6

        if player.get("overall", 60) >= 88:
            bid_chance += 5

        if random.randint(1, 100) > bid_chance:
            continue

        offers.append(
            build_offer(
                player,
                club,
            )
        )

        if len(offers) >= 3:
            break

    return offers


def complete_web_transfer(
    player,
    offer,
    completed_season,
):
    old_club = player.get(
        "club",
        "Unknown Club",
    )

    player["club"] = offer["club_name"]
    player["contract_years"] = int(
        offer["contract_years"]
    )
    player["weekly_wage"] = int(
        offer["weekly_wage"]
    )
    player["squad_role"] = offer["squad_role"]
    player["last_transfer_season"] = (
        completed_season
    )

    fee = int(offer["fee"])

    player["biggest_transfer_fee"] = max(
        player.get("biggest_transfer_fee", 0),
        fee,
    )

    add_club_to_history(
        player,
        player["club"],
    )

    return {
        "old_club": old_club,
        "new_club": player["club"],
        "fee": fee,
    }


# ==========================================
# ORIGINAL TERMINAL TRANSFERS
# ==========================================

def first_professional_move(player):
    offers = first_professional_offer(player)

    if not offers:
        print("No clubs exist in clubs.py.")
        return

    offer = offers[0]
    completed_season = player.get("season", 1)

    complete_web_transfer(
        player,
        offer,
        completed_season,
    )

    print()
    print("==========================")
    print("FIRST PROFESSIONAL CONTRACT")
    print("==========================")
    print(f"Club: {offer['club_name']}")
    print(f"League: {offer['league']}")
    print(
        f"Contract: "
        f"{offer['contract_years']} years"
    )
    print(
        f"Wage: "
        f"£{offer['weekly_wage']:,}/week"
    )
    print(
        f"Squad Role: "
        f"{offer['squad_role']}"
    )


def transfer_window(player):
    print()
    print("==========================")
    print("TRANSFER WINDOW")
    print("==========================")

    season = player.get("season", 1)

    if player.get("club") in [
        "Youth Academy",
        "Local Academy",
    ]:
        first_professional_move(player)
        return

    offers = generate_web_transfer_offers(
        player,
        completed_season=season,
    )

    if not offers:
        print(
            "No suitable transfer offers "
            "arrived this season."
        )
        return

    for number, offer in enumerate(
        offers,
        start=1,
    ):
        print(
            f"{number}. "
            f"{offer['club_name']} "
            f"({offer['league']}) "
            f"- £{offer['fee']}m"
        )

    stay_option = len(offers) + 1

    print(
        f"{stay_option}. Stay at "
        f"{player.get('club', 'Current Club')}"
    )

    choice = input("\nChoose: ").strip()

    if not choice.isdigit():
        print("Invalid choice.")
        return

    choice = int(choice)

    if choice == stay_option:
        print(
            f"You stayed at "
            f"{player.get('club', 'your club')}."
        )
        return

    if not 1 <= choice <= len(offers):
        print("Invalid choice.")
        return

    selected = offers[choice - 1]

    result = complete_web_transfer(
        player,
        selected,
        completed_season=season,
    )

    print()
    print("==========================")
    print("TRANSFER COMPLETE")
    print("==========================")
    print(f"From: {result['old_club']}")
    print(f"To: {result['new_club']}")
    print(f"League: {selected['league']}")
    print(f"Transfer Fee: £{selected['fee']}m")
    print(
        f"Contract: "
        f"{selected['contract_years']} years"
    )
    print(
        f"Wage: "
        f"£{selected['weekly_wage']:,}/week"
    )
    print(
        f"Squad Role: "
        f"{selected['squad_role']}"
    )


def transfer_summary(player):
    print()
    print("==========================")
    print("TRANSFER INFORMATION")
    print("==========================")
    print(
        f"Club: "
        f"{player.get('club', 'Unknown Club')}"
    )
    print(
        f"Contract: "
        f"{player.get('contract_years', 0)} years"
    )
    print(
        f"Wage: "
        f"£{player.get('weekly_wage', 0):,}/week"
    )
    print(
        f"Squad Role: "
        f"{player.get('squad_role', 'Unknown')}"
    )