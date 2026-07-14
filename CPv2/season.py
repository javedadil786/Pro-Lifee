import random

from development import yearly_development
from matches import simulate_season
from transfers import transfer_window
from trophies import season_awards
from injuries import check_injury, injury_status
from international import (
    international_tournament,
    setup_international_stats,
)


def setup_career_tracking(player):
    player.setdefault("season", 1)
    player.setdefault("overall_history", [])
    player.setdefault(
        "peak_overall",
        player.get("overall", 60),
    )
    player.setdefault("career_matches", 0)
    player.setdefault("career_rating_total", 0.0)
    player.setdefault("career_rating_seasons", 0)
    player.setdefault("career_seasons", 0)
    player.setdefault(
        "clubs_history",
        ["Youth Academy"],
    )
    player.setdefault("biggest_transfer_fee", 0)
    player.setdefault("retired", False)
    player.setdefault("retirement_reason", "")

    setup_international_stats(player)


def career_hub(player):
    setup_career_tracking(player)

    while True:
        print()
        print("====================================")
        print("          CAREER HUB")
        print("====================================")
        print(f"Name: {player['name']}")
        print(f"Age: {player['age']}")
        print(f"Nationality: {player['nationality']}")
        print(f"Club: {player['club']}")
        print(f"Position: {player['position']}")
        print(f"Overall: {player['overall']}")
        print(f"Potential: {player['potential']}")
        print(f"Season: {player['season']}")
        print()
        print("1. Play Next Season")
        print("2. View Player")
        print("3. Injury Status")
        print("4. Retire")

        choice = input("\nChoose: ").strip()

        if choice == "1":
            play_season(player)

            if retirement_check(player):
                player["retired"] = True
                player["retirement_reason"] = (
                    "Automatic retirement"
                )
                career_summary(player)
                break

        elif choice == "2":
            player_profile(player)

        elif choice == "3":
            injury_status(player)

        elif choice == "4":
            player["retired"] = True
            player["retirement_reason"] = (
                "Player chose to retire"
            )
            career_summary(player)
            break

        else:
            print("Invalid option.")


def player_profile(player):
    print()
    print("====================================")
    print("        PLAYER PROFILE")
    print("====================================")
    print(f"Name: {player['name']}")
    print(f"Age: {player['age']}")
    print(f"Nationality: {player['nationality']}")
    print(f"Club: {player['club']}")
    print(f"Position: {player['position']}")
    print(f"Overall: {player['overall']}")
    print(f"Potential: {player['potential']}")


def play_season(player, web_mode=False):
    setup_career_tracking(player)

    if player.get("retired", False):
        return

    print()
    print("====================================")
    print(f"          SEASON {player['season']}")
    print("====================================")

    player["age"] += 1

    check_injury(player)

    old_overall = player["overall"]
    yearly_development(player)

    print()
    print(
        f"Overall: "
        f"{old_overall} -> {player['overall']}"
    )

    simulate_season(player)

    if player["position"] == "Goalkeeper":
        player["career_saves"] = (
            player.get("career_saves", 0)
            + player.get("season_saves", 0)
        )

        player["career_clean_sheets"] = (
            player.get("career_clean_sheets", 0)
            + player.get(
                "season_clean_sheets",
                0,
            )
        )

    international_tournament(player)
    season_awards(player)

    if not web_mode:
        transfer_window(player)

    player["overall_history"].append(
        player["overall"]
    )

    player["peak_overall"] = max(
        player.get(
            "peak_overall",
            player["overall"],
        ),
        player["overall"],
    )

    player["career_seasons"] = (
        player.get("career_seasons", 0)
        + 1
    )

    player["season"] += 1


def retirement_check(player):
    age = player.get("age", 15)

    if age >= 40:
        return True

    if age < 30:
        return False

    retirement_chances = {
        30: 1,
        31: 2,
        32: 4,
        33: 7,
        34: 10,
        35: 18,
        36: 30,
        37: 45,
        38: 65,
        39: 85,
    }

    chance = retirement_chances.get(
        age,
        100,
    )

    return random.randint(1, 100) <= chance


def total_trophies(player):
    return (
        player.get("league_titles", 0)
        + player.get("domestic_cups", 0)
        + player.get("champions_leagues", 0)
        + player.get("world_cups", 0)
        + player.get("euros", 0)
    )


def career_status(player):
    score = 0

    score += (
        player.get("peak_overall", 60)
        - 60
    )
    score += (
        player.get("career_matches", 0)
        // 40
    )
    score += (
        player.get("career_goals", 0)
        // 50
    )
    score += (
        player.get("career_assists", 0)
        // 40
    )
    score += total_trophies(player) * 4
    score += (
        player.get("ballon_dors", 0)
        * 10
    )
    score += (
        player.get("golden_boots", 0)
        * 4
    )
    score += (
        player.get("international_caps", 0)
        // 20
    )

    if score >= 100:
        return "GOAT"
    if score >= 75:
        return "All-Time Great"
    if score >= 55:
        return "World-Class Legend"
    if score >= 38:
        return "Club Legend"
    if score >= 24:
        return "Top Professional"
    if score >= 12:
        return "Journeyman"

    return "Short Career"


def build_career_summary(player):
    history = player.get(
        "overall_history",
        [],
    )

    if history:
        average_overall = round(
            sum(history) / len(history),
            1,
        )
    else:
        average_overall = player.get(
            "overall",
            0,
        )

    rating_seasons = player.get(
        "career_rating_seasons",
        0,
    )

    if rating_seasons:
        average_rating = round(
            player.get(
                "career_rating_total",
                0.0,
            )
            / rating_seasons,
            2,
        )
    else:
        average_rating = 0.0

    return {
        "average_overall": average_overall,
        "average_rating": average_rating,
        "career_status": career_status(player),
        "total_trophies": total_trophies(player),
        "clubs_played": " → ".join(
            player.get(
                "clubs_history",
                ["Youth Academy"],
            )
        ),
    }


def career_summary(player):
    summary = build_career_summary(player)

    print()
    print("====================================")
    print("          CAREER COMPLETE")
    print("====================================")
    print(f"Name: {player['name']}")
    print(f"Retirement Age: {player['age']}")
    print(f"Final Club: {player['club']}")
    print(f"Final Overall: {player['overall']}")
    print(
        f"Peak Overall: "
        f"{player.get('peak_overall', player['overall'])}"
    )
    print(
        f"Average Overall: "
        f"{summary['average_overall']}"
    )
    print(
        f"Average Match Rating: "
        f"{summary['average_rating']}"
    )
    print(
        f"Career Matches: "
        f"{player.get('career_matches', 0)}"
    )
    print(
        f"Total Trophies: "
        f"{summary['total_trophies']}"
    )
    print(
        f"Career Status: "
        f"{summary['career_status']}"
    )

    return summary