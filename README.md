# fep-participant-auto-listing
> Line Bot for chat automation.
### Feature
- Auto listing.

# Installation
```sh
$ pip install -r requirements.txt
```

# Getting Started
Before using bothub-cli, you need to tell it about your [BotHub.Studio](https://bothub.studio) credentials.
```
$ bothub configure
```

# Usage
- user
```
add <batch> <name> <campus> <room> - .add a kamu Kemanggisan 000
upd <batch> <number> <name> <campus> <room> - .upd a 1 kamu Kemanggisan 000
del <batch> <number> - .del a 1
view <batch> - .view a / .view
```

- admin
```
reset_store - .reset_store
pre_store <url> - .pre_store https://gist.githubusercontent.com/muazhari/38a5819eb228a20a693db0516e76bedb/raw/108e665e24b63184f92444436b83142a4bf1fb0b/feplist / .pre_store
backup_store <condition> - .backup_store silent / .backup_store
```

# Todos
- Please fork it, and contribute yeah!

# Authors
- Muhammad Kharisma Azhari - Initial work
