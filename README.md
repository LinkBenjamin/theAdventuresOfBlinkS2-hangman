## The Adventures of Blink, Season 2:  Hangman!

Hey pals!  If you stumbled across this repo direct from GitHub, this is a tutorial build that I'm doing on my blog & Youtube channel.  I'd love for you to come along and build with me!

## The Adventures of Blink

- [Blog](https://dev.to/LinkBenjamin)
- [Youtube Channel](https://www.youtube.com/@TheAdventuresOfBlink/)
  - [Season 2 Playlist](https://www.youtube.com/watch?v=sprHBFPQZTw&list=PLzx3AhqFM-JCde64SNh6I1_EHLMOLO2dL)

## How to use this repository

`main` - This branch will be updated with the cumulative work done throughout Season 2.  You can think of this as "the latest".

`S2E[x]` - There will be a separate branch showing the end result of each episode, so that you can match up with each week's adventure.  If you're joining mid-season, or if you got stuck and want to pick up from a "checkpoint"... use the appropriate one of these.

`Actions Workflow` - In Episode 5, we're introducing a GitHub Actions workflow to automatically run our unit tests when we commit to a branch.

## An .env file

Create a .env in the project root (it will be .gitignored).  Here are the elements you should identify in your .env:

```bash
MONGO_URI=
MONGO_URI_API=
MONGO_INITDB_ROOT_USERNAME=
MONGO_INITDB_ROOT_PASSWORD=
DB_NAME=
COLLECTION_NAME=
API_URL=
LLM_URI=
MODEL_ID=
```

## Running Hangman

This will vary from episode to episode, but generally speaking we're going to try to run our application in the following manner:

1. `docker-compose up`: Starts the Mongo DB and the accompanying API
2. `python main.py`: Starts the frontend Hangman game
3. `pytest`: When run within the hangman folder, executes the unit test suite