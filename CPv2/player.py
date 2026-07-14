import random


def calculate_overall(position, pace, shooting, passing, defending):
    if position == "Goalkeeper":
        overall = round(
            defending * 0.65
            + passing * 0.25
            + pace * 0.10
        )
    elif position == "Defender":
        overall = round(
            defending * 0.50
            + pace * 0.20
            + passing * 0.20
            + shooting * 0.10
        )
    elif position == "Midfielder":
        overall = round(
            passing * 0.45
            + shooting * 0.20
            + pace * 0.20
            + defending * 0.15
        )
    elif position == "Winger":
        overall = round(
            pace * 0.40
            + shooting * 0.30
            + passing * 0.25
            + defending * 0.05
        )
    else:
        overall = round(
            shooting * 0.50
            + pace * 0.25
            + passing * 0.20
            + defending * 0.05
        )

    return max(40, min(99, overall))


def choose_nationality():
    nations = {
        "1": "England",
        "2": "France",
        "3": "Spain",
        "4": "Germany",
        "5": "Brazil",
        "6": "Argentina",
        "7": "Portugal",
        "8": "Italy",
        "9": "Netherlands",
        "10": "Belgium",
    }

    print()
    print("Choose nationality:")
    print("1. England")
    print("2. France")
    print("3. Spain")
    print("4. Germany")
    print("5. Brazil")
    print("6. Argentina")
    print("7. Portugal")
    print("8. Italy")
    print("9. Netherlands")
    print("10. Belgium")
    print("11. Enter your own nationality")

    while True:
        choice = input("Choose: ").strip()

        if choice in nations:
            return nations[choice]

        if choice == "11":
            custom_nation = input("Enter nationality: ").strip()

            if custom_nation:
                return custom_nation.title()

            print("Please enter a nationality.")
        else:
            print("Invalid choice.")


def choose_position():
    positions = {
        "1": "Goalkeeper",
        "2": "Defender",
        "3": "Midfielder",
        "4": "Winger",
        "5": "Striker",
    }

    print()
    print("Choose position:")
    print("1. Goalkeeper")
    print("2. Defender")
    print("3. Midfielder")
    print("4. Winger")
    print("5. Striker")

    while True:
        choice = input("Choose: ").strip()

        if choice in positions:
            return positions[choice]

        print("Invalid choice.")


def generate_starting_stats(position):
    if position == "Goalkeeper":
        pace = random.randint(38, 52)
        shooting = random.randint(15, 28)
        passing = random.randint(58, 70)
        defending = random.randint(70, 80)

    elif position == "Defender":
        pace = random.randint(62, 75)
        shooting = random.randint(30, 45)
        passing = random.randint(57, 70)
        defending = random.randint(71, 82)

    elif position == "Midfielder":
        pace = random.randint(66, 78)
        shooting = random.randint(60, 73)
        passing = random.randint(74, 84)
        defending = random.randint(54, 68)

    elif position == "Winger":
        pace = random.randint(80, 90)
        shooting = random.randint(66, 78)
        passing = random.randint(67, 78)
        defending = random.randint(32, 46)

    else:
        pace = random.randint(72, 84)
        shooting = random.randint(78, 89)
        passing = random.randint(56, 69)
        defending = random.randint(28, 41)

    return pace, shooting, passing, defending


def generate_potential(overall):
    potential_group = random.choices(
        [
            "average",
            "good",
            "high",
            "elite",
            "generational",
        ],
        weights=[
            15,
            30,
            30,
            20,
            5,
        ],
        k=1,
    )[0]

    if potential_group == "average":
        minimum = max(overall + 6, 78)
        maximum = max(overall + 11, 84)

    elif potential_group == "good":
        minimum = max(overall + 9, 83)
        maximum = max(overall + 15, 89)

    elif potential_group == "high":
        minimum = max(overall + 12, 87)
        maximum = max(overall + 18, 93)

    elif potential_group == "elite":
        minimum = max(overall + 15, 91)
        maximum = 97

    else:
        minimum = max(overall + 17, 95)
        maximum = 99

    minimum = min(99, minimum)
    maximum = min(99, max(minimum, maximum))

    return random.randint(minimum, maximum)


def create_player():
    print()
    print("========================")
    print("     CREATE PLAYER")
    print("========================")

    while True:
        name = input("Player name: ").strip()

        if name:
            break

        print("Please enter a player name.")

    nationality = choose_nationality()
    position = choose_position()

    pace, shooting, passing, defending = generate_starting_stats(position)

    overall = calculate_overall(
        position,
        pace,
        shooting,
        passing,
        defending,
    )

    potential = generate_potential(overall)

    player = {
        "name": name,
        "age": 15,
        "nationality": nationality,
        "position": position,
        "club": "Youth Academy",

        "pace": pace,
        "shooting": shooting,
        "passing": passing,
        "defending": defending,

        "overall": overall,
        "potential": potential,

        "season": 1,
        "overall_history": [],
        "peak_overall": overall,
        "career_rating_total": 0.0,
        "career_rating_seasons": 0,
        "career_seasons": 0,
        "clubs_history": ["Youth Academy"],
        "biggest_transfer_fee": 0,

        "career_matches": 0,
        "career_goals": 0,
        "career_assists": 0,
        "career_saves": 0,
        "career_clean_sheets": 0,

        "league_titles": 0,
        "domestic_cups": 0,
        "champions_leagues": 0,
        "world_cups": 0,
        "ballon_dors": 0,
        "golden_boots": 0,
        "team_of_seasons": 0,

        "season_matches": 0,
        "season_goals": 0,
        "season_assists": 0,
        "season_saves": 0,
        "season_clean_sheets": 0,
        "season_rating": 0.0,

        "injured": False,
        "injury_name": "",
        "injury_games": 0,

        "contract_years": 0,
        "weekly_wage": 0,
        "squad_role": "Academy Player",

        "won_league_this_season": False,
        "won_cup_this_season": False,
        "won_ucl_this_season": False,
        "won_world_cup_this_season": False,
    }

    print()
    print("========================")
    print("    PLAYER CREATED")
    print("========================")
    print(f"Name: {player['name']}")
    print(f"Age: {player['age']}")
    print(f"Nationality: {player['nationality']}")
    print(f"Position: {player['position']}")
    print(f"Club: {player['club']}")
    print()
    print(f"Overall: {player['overall']}")
    print(f"Potential: {player['potential']}")
    print()
    print("Starting Attributes")
    print("-------------------")
    print(f"Pace: {player['pace']}")
    print(f"Shooting: {player['shooting']}")
    print(f"Passing: {player['passing']}")
    print(f"Defending: {player['defending']}")

    return player