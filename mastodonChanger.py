import getopt
import random
import re
import sys

from mastodon import Mastodon

import config
import moods


def write_status(mood: str, dry_run: bool = False) -> None:
    """Write a status to Mastodon"""
    mastodon = Mastodon(access_token=config.ACCESS_TOKEN_2, api_base_url=config.API_URL)
    if dry_run is False:
        # Post
        mastodon.toot(mood)
        print(f"Posted {mood}")
    else:
        print(f"Dry run, would have posted {mood}")


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
    mood = random.choice(moods.MOOD_LIST)

    # Build the fields
    fields = [
        (me.fields[0]["name"], url),
        (me.fields[1]["name"], me.fields[1]["value"]),
        (me.fields[2]["name"], me.fields[2]["value"]),
        (me.fields[3]["name"], mood),
    ]

    if dry_run is False:
        # Update the account fields
        mastodon.account_update_credentials(fields=fields)
        print(f"Updated! You were {mood} today :)")
    else:
        print(f"Dry run, fields would be: \n{fields}")

    write_status(mood, dry_run)


if __name__ == "__main__":
    dry_run = False
    opts, args = getopt.getopt(sys.argv[1:], shortopts="d", longopts="dry-run")
    for opt, arg in opts:
        if opt in ("-d", "--dry-run"):
            dry_run = True
    do_update(dry_run)
