# Mastodon Field Changer
(best repo name ever)

Randomly changes a field on [my mastodon profile](https://iscurrently.live/@theresnotime).

## Moods
Mood strings (?) are defined in [moods.py](moods.py) because I couldn't be bothered to read from a JSON file when this just works. They're a nice simple Python list.
```py
MOOD_LIST = [
    "Happy",
    "Contemplating Python",
    "Looking at PHP",
    "etc."
]
```

### Add more for me
Do it! As long as it's safe for work I'll *probably* merge it :D
1. Fork the repo
2. Edit [moods.py](moods.py)
3. Submit a pull request


## Use it (why??)
1. Clone the repo (`git clone https://github.com/theresnotime/mastodon-field-changer.git`)
2. Install the dependencies (`pip install -r requirements.txt`)
3. Edit [config.example.py](config.example.py) and rename it to `config.py`
4. Run ~~away, never looking back~~ the script (`python mastodonChanger.py`)
