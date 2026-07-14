import random

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
)

from player import (
    generate_starting_stats,
    calculate_overall,
    generate_potential,
)

from season import (
    play_season,
    retirement_check,
    build_career_summary,
)

from transfers import (
    generate_web_transfer_offers,
    complete_web_transfer,
)

from save_manager import (
    save_career,
    load_career,
    delete_career,
    list_careers,
)


app = Flask(__name__)


current_player = None
pending_transfer_offers = []


def build_web_player(
    name,
    nationality,
    position,
):
    pace, shooting, passing, defending = (
        generate_starting_stats(position)
    )

    overall = calculate_overall(
        position,
        pace,
        shooting,
        passing,
        defending,
    )

    potential = generate_potential(overall)

    return {
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
        "peak_overall": overall,

        "season": 1,
        "overall_history": [],

        "career_matches": 0,
        "career_goals": 0,
        "career_assists": 0,
        "career_saves": 0,
        "career_clean_sheets": 0,

        "career_rating_total": 0.0,
        "career_rating_seasons": 0,
        "career_seasons": 0,

        "league_titles": 0,
        "domestic_cups": 0,
        "champions_leagues": 0,
        "world_cups": 0,
        "euros": 0,

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

        "clubs_history": [
            "Youth Academy"
        ],

        "biggest_transfer_fee": 0,
        "last_transfer_season": -100,

        "international_caps": 0,
        "international_goals": 0,
        "international_assists": 0,
        "international_saves": 0,
        "international_clean_sheets": 0,

        "world_cup_appearances": 0,
        "euros_appearances": 0,

        "won_league_this_season": False,
        "won_cup_this_season": False,
        "won_ucl_this_season": False,
        "won_world_cup_this_season": False,
        "won_euros_this_season": False,

        "retired": False,
        "retirement_reason": "",

        "save_id": None,
    }


def autosave_current_career():
    global current_player

    if current_player is None:
        return

    save_id = current_player.get(
        "save_id"
    )

    if save_id:
        save_career(
            current_player,
            save_id,
        )


def automatically_handle_transfers(
    player,
    offers,
    completed_season,
):
    if not offers:
        return

    if player.get("club") in [
        "Youth Academy",
        "Local Academy",
    ]:
        complete_web_transfer(
            player,
            offers[0],
            completed_season,
        )
        return

    best_offer = max(
        offers,
        key=lambda offer: (
            offer.get("rating", 70),
            offer.get("weekly_wage", 0),
            offer.get("fee", 0),
        ),
    )

    current_club_rating = 70

    if player.get("club") not in [
        "Youth Academy",
        "Local Academy",
    ]:
        current_club_rating = player.get(
            "club_rating",
            70,
        )

    new_club_rating = best_offer.get(
        "rating",
        70,
    )

    move_chance = 28

    if new_club_rating >= current_club_rating + 5:
        move_chance += 25

    elif new_club_rating >= current_club_rating:
        move_chance += 12

    if best_offer.get(
        "weekly_wage",
        0,
    ) > player.get(
        "weekly_wage",
        0,
    ):
        move_chance += 8

    if player.get("age", 18) <= 23:
        move_chance += 5

    if player.get("age", 18) >= 32:
        move_chance -= 10

    move_chance = max(
        15,
        min(75, move_chance),
    )

    if random.randint(1, 100) <= move_chance:
        complete_web_transfer(
            player,
            best_offer,
            completed_season,
        )


@app.route("/")
def home():
    careers = list_careers()

    return render_template(
        "index.html",
        careers=careers,
    )


@app.route(
    "/create-player",
    methods=["GET", "POST"],
)
def create_player_page():
    global current_player
    global pending_transfer_offers

    if request.method == "POST":
        name = request.form.get(
            "name",
            "",
        ).strip()

        nationality = request.form.get(
            "nationality",
            "England",
        ).strip()

        position = request.form.get(
            "position",
            "Striker",
        ).strip()

        if not name:
            return render_template(
                "create_player.html",
                error=(
                    "Please enter a player name."
                ),
            )

        current_player = build_web_player(
            name,
            nationality,
            position,
        )

        save_id = save_career(
            current_player
        )

        current_player["save_id"] = (
            save_id
        )

        pending_transfer_offers = []

        return redirect(
            url_for("career_page")
        )

    return render_template(
        "create_player.html"
    )


@app.route("/career")
def career_page():
    if current_player is None:
        return redirect(
            url_for("home")
        )

    summary = None

    if current_player.get(
        "retired",
        False,
    ):
        summary = build_career_summary(
            current_player
        )

    return render_template(
        "career.html",
        player=current_player,
        transfer_offers=(
            pending_transfer_offers
        ),
        summary=summary,
    )


@app.route(
    "/play-season",
    methods=["POST"],
)
def play_next_season():
    global current_player
    global pending_transfer_offers

    if current_player is None:
        return redirect(
            url_for("home")
        )

    if current_player.get(
        "retired",
        False,
    ):
        return redirect(
            url_for("career_page")
        )

    if pending_transfer_offers:
        return redirect(
            url_for("career_page")
        )

    play_season(
        current_player,
        web_mode=True,
    )

    if retirement_check(
        current_player
    ):
        current_player["retired"] = True

        current_player[
            "retirement_reason"
        ] = "Automatic retirement"

        pending_transfer_offers = []

        autosave_current_career()

        return redirect(
            url_for("career_page")
        )

    completed_season = (
        current_player.get(
            "season",
            1,
        )
        - 1
    )

    pending_transfer_offers = (
        generate_web_transfer_offers(
            current_player,
            completed_season,
        )
    )

    autosave_current_career()

    return redirect(
        url_for("career_page")
    )


@app.route(
    "/simulate-full-career",
    methods=["POST"],
)
def simulate_full_career():
    global current_player
    global pending_transfer_offers

    if current_player is None:
        return redirect(
            url_for("home")
        )

    if current_player.get(
        "retired",
        False,
    ):
        return redirect(
            url_for("career_page")
        )

    if pending_transfer_offers:
        completed_season = (
            current_player.get(
                "season",
                1,
            )
            - 1
        )

        automatically_handle_transfers(
            current_player,
            pending_transfer_offers,
            completed_season,
        )

        pending_transfer_offers = []

    simulated_seasons = 0
    maximum_simulated_seasons = 30

    while (
        not current_player.get(
            "retired",
            False,
        )
        and simulated_seasons
        < maximum_simulated_seasons
    ):
        play_season(
            current_player,
            web_mode=True,
        )

        simulated_seasons += 1

        if retirement_check(
            current_player
        ):
            current_player[
                "retired"
            ] = True

            current_player[
                "retirement_reason"
            ] = "Automatic retirement"

            break

        completed_season = (
            current_player.get(
                "season",
                1,
            )
            - 1
        )

        offers = (
            generate_web_transfer_offers(
                current_player,
                completed_season,
            )
        )

        automatically_handle_transfers(
            current_player,
            offers,
            completed_season,
        )

        autosave_current_career()

    if not current_player.get(
        "retired",
        False,
    ):
        current_player["retired"] = True

        current_player[
            "retirement_reason"
        ] = "Career simulation completed"

    pending_transfer_offers = []

    autosave_current_career()

    return redirect(
        url_for("career_page")
    )


@app.route(
    "/accept-transfer/<int:offer_index>",
    methods=["POST"],
)
def accept_transfer(
    offer_index,
):
    global current_player
    global pending_transfer_offers

    if current_player is None:
        return redirect(
            url_for("home")
        )

    if current_player.get(
        "retired",
        False,
    ):
        return redirect(
            url_for("career_page")
        )

    if not (
        0
        <= offer_index
        < len(
            pending_transfer_offers
        )
    ):
        return redirect(
            url_for("career_page")
        )

    completed_season = (
        current_player.get(
            "season",
            1,
        )
        - 1
    )

    selected_offer = (
        pending_transfer_offers[
            offer_index
        ]
    )

    complete_web_transfer(
        current_player,
        selected_offer,
        completed_season,
    )

    pending_transfer_offers = []

    autosave_current_career()

    return redirect(
        url_for("career_page")
    )


@app.route(
    "/reject-transfers",
    methods=["POST"],
)
def reject_transfers():
    global pending_transfer_offers

    pending_transfer_offers = []

    autosave_current_career()

    return redirect(
        url_for("career_page")
    )


@app.route(
    "/save-career",
    methods=["POST"],
)
def save_current_career():
    global current_player

    if current_player is None:
        return redirect(
            url_for("home")
        )

    save_id = save_career(
        current_player,
        current_player.get(
            "save_id"
        ),
    )

    current_player["save_id"] = (
        save_id
    )

    return redirect(
        url_for("career_page")
    )


@app.route(
    "/load-career/<save_id>",
    methods=["POST"],
)
def load_saved_career(
    save_id,
):
    global current_player
    global pending_transfer_offers

    loaded_player = load_career(
        save_id
    )

    if loaded_player is None:
        return redirect(
            url_for("home")
        )

    current_player = loaded_player
    pending_transfer_offers = []

    return redirect(
        url_for("career_page")
    )


@app.route(
    "/delete-career/<save_id>",
    methods=["POST"],
)
def delete_saved_career(
    save_id,
):
    global current_player
    global pending_transfer_offers

    delete_career(save_id)

    if (
        current_player is not None
        and current_player.get(
            "save_id"
        )
        == save_id
    ):
        current_player = None
        pending_transfer_offers = []

    return redirect(
        url_for("home")
    )


@app.route(
    "/retire",
    methods=["POST"],
)
def retire_player():
    global current_player
    global pending_transfer_offers

    if current_player is None:
        return redirect(
            url_for("home")
        )

    current_player["retired"] = True

    current_player[
        "retirement_reason"
    ] = "Player chose to retire"

    pending_transfer_offers = []

    autosave_current_career()

    return redirect(
        url_for("career_page")
    )


@app.route("/statistics")
def statistics_page():
    if current_player is None:
        return redirect(
            url_for("home")
        )

    return render_template(
        "statistics.html",
        player=current_player,
    )


if __name__ == "__main__":
    app.run(debug=True)