![Logo for Sunless Sea - The Bloomin Casual. A fancy cocktail glass containing a mysterious and luminous drink, an eyeball, and a tipsy looking purple mushroom stands on a dark wooden table](https://github.com/CaffeinePwrdAl/SunlessSeaCasual/blob/main/Bloomin%20Casual.png?raw=true)

# About

You pass by "The Storied Mode" public house just outside the docks, it beckons you in like an old friend. You walk to the bar, meet eyes with the bartender, and ask for a large
pitcher of Bloomin Casual. He serves it up luke warm, just as you like it.

This is a script for editing the JSON save files for the game [Sunless Sea](https://www.failbettergames.com/games/sunless-sea). I love the game, the lore, the stories, but I'm impatient and not a good captain!

## Usage

```
$ python bloomin_casual.py --help
usage: The Bloomin Casual [-h] [-i INPUT] [-o OUTPUT] [-b BACKUP] [-p] [-f FUEL] [-s SUPPLIES] [-c COFFEE] [-l] [-a ADD] [-n NUM]

You pass by "The Storied Mode" public house just outside the docks, it beckons you in like an old friend. You walk to the bar, meet eyes with the bartender, and ask for a large
glass of Bloomin Casual. He serves it up luke warm, just as you like it.

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input filename of JSON save game. Default: Autosave.json
  -o OUTPUT, --output OUTPUT
                        Output filename of JSON save game. Default: Autosave.json
  -b BACKUP, --backup BACKUP
                        Back up the input json file. Default: True
  -p, --pretty          Load input and pretty print json to output file. When -p used with out any arguments the autosave will be pretty printed and saved in place
  -f FUEL, --fuel FUEL  Add n fuel (integer)
  -s SUPPLIES, --supplies SUPPLIES
                        Add n supplies (integer)
  -c COFFEE, --coffee COFFEE
                        Add dark drop coffee beans (integer)
  -l, --list            List known qualities
  -a ADD, --add ADD     Increase the level of the named quality (can also use ID)
  -n NUM, --num NUM     Add 'n' of the quality named by the --add option
```
