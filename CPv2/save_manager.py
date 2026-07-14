import json
import re
from datetime import datetime
from pathlib import Path


SAVES_FOLDER = Path(__file__).parent / "saves"


def ensure_saves_folder():
    SAVES_FOLDER.mkdir(
        parents=True,
        exist_ok=True,
    )


def clean_save_name(name):
    cleaned = re.sub(
        r"[^a-zA-Z0-9_-]+",
        "_",
        name.strip(),
    )

    cleaned = cleaned.strip("_")

    if not cleaned:
        cleaned = "career"

    return cleaned.lower()


def create_save_id(player):
    player_name = player.get(
        "name",
        "career",
    )

    clean_name = clean_save_name(
        player_name
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    return f"{clean_name}_{timestamp}"


def get_save_path(save_id):
    ensure_saves_folder()

    safe_id = clean_save_name(save_id)

    return SAVES_FOLDER / f"{safe_id}.json"


def save_career(player, save_id=None):
    ensure_saves_folder()

    if save_id is None:
        save_id = player.get("save_id")

    if not save_id:
        save_id = create_save_id(player)

    player["save_id"] = save_id

    save_path = get_save_path(save_id)

    save_data = {
        "save_id": save_id,
        "updated_at": datetime.now().isoformat(
            timespec="seconds"
        ),
        "player": player,
    }

    with save_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            save_data,
            file,
            indent=4,
            ensure_ascii=False,
        )

    return save_id


def load_career(save_id):
    save_path = get_save_path(save_id)

    if not save_path.exists():
        return None

    try:
        with save_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            save_data = json.load(file)

    except (
        json.JSONDecodeError,
        OSError,
    ):
        return None

    player = save_data.get("player")

    if not isinstance(player, dict):
        return None

    player["save_id"] = save_id

    return player


def delete_career(save_id):
    save_path = get_save_path(save_id)

    if not save_path.exists():
        return False

    try:
        save_path.unlink()
        return True

    except OSError:
        return False


def list_careers():
    ensure_saves_folder()

    careers = []

    for save_path in SAVES_FOLDER.glob(
        "*.json"
    ):
        try:
            with save_path.open(
                "r",
                encoding="utf-8",
            ) as file:
                save_data = json.load(file)

        except (
            json.JSONDecodeError,
            OSError,
        ):
            continue

        player = save_data.get(
            "player",
            {},
        )

        if not isinstance(player, dict):
            continue

        careers.append({
            "save_id": save_data.get(
                "save_id",
                save_path.stem,
            ),
            "updated_at": save_data.get(
                "updated_at",
                "",
            ),
            "name": player.get(
                "name",
                "Unknown Player",
            ),
            "age": player.get(
                "age",
                15,
            ),
            "club": player.get(
                "club",
                "Youth Academy",
            ),
            "position": player.get(
                "position",
                "Unknown",
            ),
            "overall": player.get(
                "overall",
                0,
            ),
            "season": player.get(
                "season",
                1,
            ),
            "retired": player.get(
                "retired",
                False,
            ),
        })

    careers.sort(
        key=lambda career: career[
            "updated_at"
        ],
        reverse=True,
    )

    return careers