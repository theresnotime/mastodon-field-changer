import config
import getopt
import moods
import random
import re
import sys
from mastodon import Mastodon


def get_used_moods() -> list:
    with open("used_moods.txt", "r") as f:
        return f.read().splitlines()


def save_used_mood(index: int) -> None:
    with open("used_moods.txt", "a") as f:
        f.write(f"{index}\n")


def write_status(mood: str, dry_run: bool = False) -> None:
    """Write a status to Mastodon"""
    mastodon = Mastodon(access_token=config.ACCESS_TOKEN_2, api_base_url=config.API_URL)
    if dry_run is False:
        # Post
        mastodon.toot(mood)
        print(f"Posted {mood}")
    else:
        print(f"Dry run, would have posted {mood}")


def filter_moods():
    """Filters out moods that have been used before"""
    # Get a list of used moods
    used_moods = get_used_moods()
    # Get a list of all moods
    all_moods = moods.MOOD_LIST
    # Copy the list of all moods
    filtered_moods = all_moods
    # Iterate over all moods
    for mood in all_moods:
        if isinstance(mood, dict):
            mood_value = mood["content"]
        else:
            mood_value = mood

        if str(mood_value) in used_moods:
            # If the mood has been used before, remove it from the list
            filtered_moods.remove(mood)
    if len(filtered_moods) == 0:
        # If there are no moods left, reset the list of used moods and exit
        print("Resetting used moods")
        with open("used_moods.txt", "w") as f:
            f.write("")
        exit()
    return filtered_moods


def get_a_mood():
    """Gets a random, unused mood"""
    mood = random.choice(filter_moods())
    if isinstance(mood, dict):
        mood_value = mood["content"]
    else:
        mood_value = mood
    save_used_mood(mood_value)
    return mood


def do_update(dry_run: bool = False) -> None:
    """Update Mastodon account fields with a random mood"""
    urlreg = re.compile('href="(?P<url>.*?)"')
    mastodon = Mastodon(access_token=config.ACCESS_TOKEN, api_base_url=config.API_URL)
    me = mastodon.account_verify_credentials()
    url_match = urlreg.search(me.fields[0]["value"])

    if url_match is None:
        # Fallback to a known URL as something went wrong...
        url = config.KNOWN_URL
    else:
        # Strip the URL out of the HTML
        url = url_match.group("url")

    # Get a random mood
    mood = get_a_mood()

    if isinstance(mood, dict):
        # If the mood is a dict, it has a label and a content
        mood_label = mood["label"]
        mood = mood["content"]
    elif isinstance(mood, str):
        # Otherwise, it's just a string
        mood_label = "Mood"
    else:
        # If it's neither a dict nor a string, it's a bad mood
        mood_label = "Mood"
        mood = "Bad mood"

    # Build the fields
    fields = [
        (me.fields[0]["name"], url),
        (me.fields[1]["name"], me.fields[1]["value"]),
        (me.fields[2]["name"], me.fields[2]["value"]),
        (mood_label, mood),
    ]

    if dry_run is False:
        # Update the account fields
        mastodon.account_update_credentials(fields=fields)
        print(f"Updated! You were {mood} today :)")
    else:
        print(f"Dry run, fields would be: \n{fields}")

    # write_status(mood, dry_run)


if __name__ == "__main__":
    dry_run = False
    opts, args = getopt.getopt(sys.argv[1:], shortopts="d", longopts="dry-run")
    for opt, arg in opts:
        if opt in ("-d", "--dry-run"):
            dry_run = True
    while True:
        do_update(dry_run)
