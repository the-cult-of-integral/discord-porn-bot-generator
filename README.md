# Discord Porn Bot Generator
Create fully functional rule34-based porn bots in seconds...

---

DPBG allows you to create fully functional discord porn bots in seconds, including configuration settings that allow you to toggle each command and whether to only post to NSFW channels.

##### Installation
1. Download the files via the [releases page](https://github.com/the-cult-of-integral/discord-porn-bot-generator/releases) or by cloning the repository.
2. Run `install_requirements.bat`.
3. Setup `config.json` then run `main.py` when you want to generate.

##### Setting up config.json
The configuration json is as follows.

```json
{
    "VERBOSE": true,
    
    "SETTINGS_PATH": "settings.json",
    "SETTINGS_RUN_DEF_DICT": false,
    "SETTINGS_DEF_DICT": {
        "database_name": "database.db",
        "prefix": "$",
        "status": ["$help", "generated by dpbg"],
        "categories": {
            "cmd1": ["tag1", ["alias1", "alias2"], "description1"],
            "cmd2": ["tag2", ["alias1", "alias2"], "description2"],
            "cmd3": ["tag3", ["alias1", "alias2"], "description3"]
        },
        "help_embed": {
            "title": "Commands",
            "color": "0xffffff",
            "image": "",
            "footer": "Bot generated by DPBG"
        },
        "log_name": "bot"
    }
}
```
- **VERBOSE**: allows you to choose whether or not the program shows and logs additional information, such as each link added.

- **SETTINGS_PATH**: where a copy of SETTINGS_DEF_DICT will be stored.
- **SETTINGS_RUN_DEF_DICT**: if false, the program will ask the user to exit after generating a copy of SETTINGS_DEF_DICT so that they can edit the copy. If true, the program will run after generating the copy without editing — set this value to true if you intend to change SETTINGS_DEF_DICT rather than a copy of it.
- **SETTINGS_DEF_DICT**: the settings for bot generation itself; forever a boilerplate unless edited.

- **Categories**: the other options for SETTINGS_DEF_DICT are self-explanatory, but for categories: cmd is the command name, tag is the rule 34 tag, aliases are discord aliases for the command and the description is used as a part of the help embed.

##### Planned featues for the future
- **More than R34**: at the moment, this porn bot rule-34 tags for porn images. This makes this project great for generating kinky, interesting, porn bots, but not so great for generating porn bots with real people as subjects. In the future, I hope to add many more options as to where to get images from.

---

##### More by the-cult-of-integral
- [Discord Raidkit](https://github.com/the-cult-of-integral/discord-raidkit) is the trojan horse of discord raiding; includes raiding tools (designed to appear useful to discord servers), hacking tools, and a token grabber generator.

- [Image to Discord link](https://github.com/the-cult-of-integral/image-to-discord-link) is a tool used to convert images to cdn discord links. It does this by uploading each image to discord, then copying all of the links to a local text file.