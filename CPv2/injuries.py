import random


# ======================================
# CHECK FOR INJURY
# ======================================

def check_injury(player):

    if player.get("injury_games", 0) > 0:

        player["injury_games"] -= 1

        player["injured"] = True

        if player["injury_games"] == 0:

            player["injured"] = False

            print("\n✅ You have recovered from injury!")

        return

    player["injured"] = False

    age = player["age"]

    chance = 8

    if age >= 30:
        chance += 4

    if age >= 34:
        chance += 5

    professionalism = player.get("professionalism", 75)

    if professionalism >= 90:
        chance -= 2

    if professionalism <= 60:
        chance += 3

    if random.randint(1,100) > chance:
        return

    roll = random.randint(1,100)

    # ------------------------------
    # Minor Injury
    # ------------------------------

    if roll <= 50:

        games = random.randint(1,3)

        injury = random.choice([
            "Knock",
            "Bruised Leg",
            "Sprained Wrist"
        ])

    # ------------------------------
    # Medium Injury
    # ------------------------------

    elif roll <= 85:

        games = random.randint(4,8)

        injury = random.choice([
            "Hamstring",
            "Groin Injury",
            "Ankle Sprain"
        ])

    # ------------------------------
    # Serious Injury
    # ------------------------------

    elif roll <= 97:

        games = random.randint(10,20)

        injury = random.choice([
            "Broken Foot",
            "Broken Ankle",
            "Knee Injury"
        ])

    # ------------------------------
    # ACL (Very Rare)
    # ------------------------------

    else:

        games = random.randint(25,40)

        injury = "ACL Tear"

    player["injured"] = True
    player["injury_name"] = injury
    player["injury_games"] = games

    print()
    print("================================")
    print("🚑 INJURY")
    print("================================")
    print(f"Injury: {injury}")
    print(f"Expected games out: {games}")


# ======================================
# APPLY MATCH REDUCTION
# ======================================

def available_matches(player, matches):

    if not player.get("injured", False):
        return matches

    missed = player.get("injury_games", 0)

    matches -= missed

    return max(0, matches)


# ======================================
# INJURY EFFECT ON DEVELOPMENT
# ======================================

def development_penalty(player):

    if not player.get("injured", False):
        return 0

    games = player.get("injury_games", 0)

    if games >= 25:
        return -3

    if games >= 15:
        return -2

    if games >= 5:
        return -1

    return 0


# ======================================
# INJURY EFFECT ON TRANSFERS
# ======================================

def transfer_penalty(player):

    if not player.get("injured", False):
        return 0

    games = player.get("injury_games", 0)

    if games >= 20:
        return 25

    if games >= 10:
        return 15

    return 5


# ======================================
# DISPLAY INJURY STATUS
# ======================================

def injury_status(player):

    if not player.get("injured", False):

        print("Status: Healthy")

        return

    print("Status: Injured")
    print(f"Injury: {player['injury_name']}")
    print(f"Games Remaining: {player['injury_games']}")