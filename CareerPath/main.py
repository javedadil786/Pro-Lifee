import random
from clubs import clubs
print("========================")
print("      CAREER PATH")
print("========================")
print()

print("1. New Career")
print("2. Exit")
print()

choice = input("Choose an option: ")

if choice == "1":
    print("Starting a new career...")
elif choice == "2":
    print("Thanks for playing!")
else:
    print("Invalid option.")
    print()

name = input("Enter your player's name: ")
age = 15
club = "Local Academy"

print()
print("Choose your position:")
print("1. Goalkeeper")
print("2. Defender")
print("3. Midfielder")
print("4. Winger")
print("5. Striker")

position_choice = input("Enter a number: ")

if position_choice == "1":
    position = "Goalkeeper"
    pace = 45
    shooting = 20
    passing = 65
    defending = 75
    overall = 65

elif position_choice == "2":
    position = "Defender"
    pace = 65
    shooting = 40
    passing = 60
    defending = 80
    overall = 65

elif position_choice == "3":
    position = "Midfielder"
    pace = 70
    shooting = 65
    passing = 80
    defending = 65
    overall = 65

elif position_choice == "4":
    position = "Winger"
    pace = 85
    shooting = 72
    passing = 70
    defending = 40
    overall = 65

elif position_choice == "5":
    position = "Striker"
    pace = 78
    shooting = 80
    passing = 60
    defending = 35
    overall = 65

else:
    position = "Unknown"



print()
print("Career Created!")
print("----------------")
print("Name:", name)
print("Age:", age)
print("Club:", club)
print("Position:", position)
print()
print("Player Stats")
print("------------")
print("Pace:", pace)
print("Shooting:", shooting)
print("Passing:", passing)
print("Defending:", defending)
print("Overall:", overall)
print()
print("Career Created!")
print("----------------")
print(f"Name: {name}")
print(f"Age: {age}")
print(f"Club: {club}")
print(f"Position: {position}")
print(f"Overall: {overall}")

season = 1

clubs = [
    "Leeds United", "Sheffield United", "Burnley", "Sunderland",
    "Brighton", "Brentford", "Crystal Palace", "Fulham",
    "Aston Villa", "West Ham", "Bournemouth", "Everton",
    "Chelsea", "Manchester United", "Manchester City",
    "Liverpool", "Arsenal", "Tottenham", "Newcastle United",
    "Real Madrid", "Barcelona", "Atletico Madrid", "Sevilla",
    "Valencia", "Real Sociedad", "Villarreal",
    "Bayern Munich", "Borussia Dortmund", "RB Leipzig",
    "Bayer Leverkusen", "Eintracht Frankfurt",
    "Juventus", "Inter Milan", "AC Milan", "Napoli",
    "Roma", "Lazio", "Atalanta",
    "PSG", "Marseille", "Monaco", "Lyon",
    "Ajax", "PSV", "Feyenoord",
    "Benfica", "Porto", "Sporting CP"
]

while True:

    print()
    print("========================")
    print("      CAREER HUB")
    print("========================")
    print(f"Name: {name}")
    print(f"Age: {age}")
    print(f"Club: {club}")
    print(f"Position: {position}")
    print(f"Overall: {overall}")
    print(f"Season: {season}")
    print()

    print("1. Play Next Season")
    print("2. View Player")
    print("3. Retire")

    hub = input("Choose an option: ")

    if hub == "1":

        old_overall = overall

        age += 1
        season += 1

        if age <= 19:
            change = random.randint(2,5)
        elif age <= 23:
            change = random.randint(1,4)
        elif age <= 28:
            change = random.randint(0,2)
        elif age <= 32:
            change = random.randint(-1,1)
        else:
            change = random.randint(-3,0)

        overall = max(1, min(99, overall + change))

        pace = max(1, min(99, pace + random.randint(-1,2)))
        shooting = max(1, min(99, shooting + random.randint(-1,2)))
        passing = max(1, min(99, passing + random.randint(-1,2)))
        defending = max(1, min(99, defending + random.randint(-1,2)))

        matches = random.randint(25,50)

        if position == "Striker":
            goals = random.randint(overall//4, overall//2)
            assists = random.randint(0,15)

        elif position == "Winger":
            goals = random.randint(5,20)
            assists = random.randint(5,18)

        elif position == "Midfielder":
            goals = random.randint(2,15)
            assists = random.randint(4,16)

        elif position == "Defender":
            goals = random.randint(0,8)
            assists = random.randint(0,6)

        else:
            goals = 0
            assists = random.randint(0,2)

        rating = round(random.uniform(6.2,8.9),1)

        print()
        print("========================")
        print(f"SEASON {season}")
        print("========================")
        print(f"Age: {age}")
        print()
        print(f"Overall: {old_overall} -> {overall} ({change:+})")
        print(f"Matches: {matches}")
        print(f"Goals: {goals}")
        print(f"Assists: {assists}")
        print(f"Average Rating: {rating}")

        if season % 2 == 0:

            print()
            print("========================")
            print("TRANSFER WINDOW")
            print("========================")

            offer = random.choice(clubs)

            print(f"{offer} have made an offer for you.")

            decision = input("Accept transfer? (y/n): ")

            if decision.lower() == "y":
                club = offer
                print(f"You have signed for {club}!")

            else:
                print(f"You stayed at {club}.")

    elif hub == "2":

        print()
        print("========================")
        print("PLAYER PROFILE")
        print("========================")
        print(f"Name: {name}")
        print(f"Age: {age}")
        print(f"Club: {club}")
        print(f"Position: {position}")
        print(f"Overall: {overall}")
        print()
        print("Attributes")
        print("----------------")
        print(f"Pace: {pace}")
        print(f"Shooting: {shooting}")
        print(f"Passing: {passing}")
        print(f"Defending: {defending}")

    elif hub == "3":

        print()
        print("========================")
        print("CAREER OVER")
        print("========================")
        print(f"{name} retired at age {age}.")
        print(f"Final Club: {club}")
        print(f"Final Overall: {overall}")
        break

    else:
        print("Invalid option.")

possible_clubs = []

for c in clubs:
    if abs(c["reputation"] - overall) <= 8:
        possible_clubs.append(c)

if len(possible_clubs) == 0:
    possible_clubs = clubs

offer = random.choice(possible_clubs)

print(f'{offer["name"]} have made an offer for you.')

decision = input("Accept transfer? (y/n): ")

if decision.lower() == "y":
    club = offer["name"]