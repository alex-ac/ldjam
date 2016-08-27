# Invent or die game

Chat bot that serves text-quest game.

You are an ancient man. You must invent technologies to live.

#### Installation:

```bash
git clone https://github.com/alex-ac/ldjam.git
virtualenv -p $(env python3) ldjam.env
. ldjam.env/bin/activate
cd ldjam
pip install -r requirements.txt
```

#### Setup:

Talk with @FatherBot at telegram:

```
/newbot
Game name
game_name_bot
```

Copy access token to bot.yaml.

#### Run:

```bash
./main.py
```

Go to telegram and say `/start` to user game\_name\_bot.

#### Known issues:

 * Bot forgets all during restart. Will fix this later.

#### TODO:

 * Use telegram webhook api;
 * Use facebook api;
 * Make commands loadable from python files;
 * Allow to modify scripts without restart;
 * !!!Make some real quests!!!;
 * Use templates for messages;

