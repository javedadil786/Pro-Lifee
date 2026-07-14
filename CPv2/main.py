from player import create_player
from season import career_hub


print("========================")
print("      CAREER PATH V2")
print("========================")


while True:

    print()
    print("1. New Career")
    print("2. Exit")

    choice = input("Choose: ")


    if choice == "1":

        player = create_player()

        print()
        print("========================")
        print("   CAREER CREATED")
        print("========================")

        print(f"Name: {player['name']}")
        print(f"Age: {player['age']}")
        print(f"Nationality: {player['nationality']}")
        print(f"Position: {player['position']}")
        print(f"Club: {player['club']}")
        print(f"Overall: {player['overall']}")

        career_hub(player)

        break


    elif choice == "2":

        print("Goodbye!")
        break


    else:

        print("Invalid option")
    