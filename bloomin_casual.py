import os
import sys
import json
import argparse
import shutil
from pathlib import Path
from datetime import datetime

# "QualitiesPossessedList": [
#   AssociatedQualityId
#

# Weight = 1 - one unit of any counts against the cargo hold size
known_qualities_physical = {
    'Supplies':      { 'id': 102026, 'full_name': 'Supplies'                          },
    'Fuel':          { 'id': 102027, 'full_name': 'Fuel'                              },
    'Colonist':      { 'id': 102021, 'full_name': 'Tomb Colonist'                     },
    'Silk':          { 'id': 102015, 'full_name': 'Bolts of Spider-Silk'              },
    'HumanSouls':    { 'id': 102016, 'full_name': 'Crate of Human Souls'              },
    'Honey':         { 'id': 102017, 'full_name': 'Firkin of Prisoner\’s honey'       },
    'Coffee':        { 'id': 102018, 'full_name': 'Sack of Darkdrop Coffee Beans'     },
    'Linen':         { 'id': 102019, 'full_name': 'Bale of Parabola-Linen'            },
    'Wine':          { 'id': 102020, 'full_name': 'Cask of Mushroom Wine'             },
    'Dice':          { 'id': 105969, 'full_name': 'Devilbone Dice'                    },
    'Ivory':         { 'id': 105973, 'full_name': 'Stygian Ivory'                     },
    'Salt':          { 'id': 105974, 'full_name': 'Mutersalt'                         },
    'Longbox':       { 'id': 105976, 'full_name': 'Soothe and Cooper Longbox'         },
    'Scintillack':   { 'id': 107719, 'full_name': 'Scintillack'                       },
    'StrangeCatch':  { 'id': 108654, 'full_name': 'Strange Catch'                     },
    'Candles':       { 'id': 110233, 'full_name': 'Foxfire Candles'                   },
    'Zzoup':         { 'id': 110547, 'full_name': 'Zzoup'                             },
    'Solacefruit':   { 'id': 111725, 'full_name': 'Solacefruit'                       },
    'Flares':        { 'id': 113263, 'full_name': 'Flares'                            },
    'FilledBox':     { 'id': 113966, 'full_name': 'Sunlight-Filled Mirrorcatch Box'   },
    'Dawn':          { 'id': 114995, 'full_name': 'Element of Dawn'                   },
    'EmptyBox':      { 'id': 115025, 'full_name': 'Empty Mirrorcatch box'             },
}

# Weight = 0
known_qualities_ethereal = {
    'Echoes':                           { 'id': 102028, 'full_name': 'Echoes' },
}

def list_qualities(qlist):
    for (name, qdata) in qlist.items():
        print("%14s (%06d) - %-40s" % (name, qdata['id'], qdata['full_name']))

def print_quality(qual, name, qdata):
    level = qual['Level']
    if level != 0:
        print("%06d %-40s: %4d" % (qdata['id'], qdata['full_name'], level))

def print_title(title):
    rule="="*80
    print(rule)
    print(title)
    print(rule)

#
# Get Character Data
#
def get_character_data(jsondata):
    return {
        'name':     jsondata['Name'],
        'status':   jsondata['Status']
    }

def print_character_data(chardata):
    print_title("Character")
    print("Name:   ", chardata['name'])
    print("Status: ", chardata['status'])
    print()

#
# Find the ship section
#
def find_ship(jsondata):
    for qual in jsondata['QualitiesPossessedList']:
        qid = int(qual['AssociatedQualityId'])
        if qid == 102889:
            return qual
    print("Didn't find ship entry")
    return None

#
# Stash useful ship data in a flatter structure
#
def get_ship_data(jsondata):
    shipdata = find_ship(jsondata)
    equipped = shipdata['EquippedPossession']
    qualities = equipped['AssociatedQuality']
    enhancements = qualities['Enhancements']
    for enhc in enhancements:
        if enhc['AssociatedQuality']['Name'] == 'Hold':
            hold_size = enhc['Level']
    return {
        'name': equipped['Name'],
        'type': qualities['Name'],
        'desc': qualities['Description'],
        'hold_size': hold_size
    }

def print_ship_data(shipdata, total_cargo):
    print_title("Ship")
    print("Name:        ", shipdata['name'])
    print("Ship Type:   ", shipdata['type'])
    print("Ship Desc:   ", shipdata['desc'])
    print("Ship Hold (total cargo): %d (%d)" % (shipdata['hold_size'], total_cargo))
    print()

#
# Load Quality Information
#
def load_qualities_set(jsondata, qlist):
    for qual in jsondata['QualitiesPossessedList']:
        qid = int(qual['AssociatedQualityId'])
        for (name, qdata) in qlist.items():
            if qid == qdata['id']:
                qdata['level'] = qual['Level']
                break

def load_qualities_data(jsondata):
    load_qualities_set(jsondata, known_qualities_physical)
    load_qualities_set(jsondata, known_qualities_ethereal)
    total_cargo=0
    for (name, qdata) in known_qualities_physical.items():
        qty = qdata['level'] if 'level' in qdata else 0
        total_cargo += qty
    return total_cargo

#
# Print standard properties
#
def print_qualities_set(jsondata, qlist):
    for qual in jsondata['QualitiesPossessedList']:
        qid = int(qual['AssociatedQualityId'])
        for (name, qdata) in qlist.items():
            if qid == qdata['id']:
                print_quality(qual, name, qdata)
                break

def print_standard_props(jsondata):
    print_title("Qualities Possessed")
    print_qualities_set(jsondata, known_qualities_physical)
    print_qualities_set(jsondata, known_qualities_ethereal)
    print()

def find_quality(jsondata, associd):
    for qual in jsondata['QualitiesPossessedList']:
        qid = int(qual['AssociatedQualityId'])
        if qid == associd:
            return qual
    print("Posessed Quality ID", associd, "not found")
    return None

def update_quality_by_id(jsondata, qid, level):
    qual = find_quality(jsondata, qid)
    if qual:
        if qual['Level']:
            print('Increasing level of %d (currently %d) by %d' % (qid, qual['Level'], level))
            qual['Level'] += level
        else:
            print('Un-set quality %d will have level set to %d' % (qid, level))
            qual['Level'] = level
        print('Level of %d now %d' % (qid, qual['Level']))

def update_quality(jsondata, name, level):
    try:
        qdata = known_qualities_physical[name]
    except:
        qdata = known_qualities_ethereal[name]

    associd = qdata['id']
    qual = find_quality(jsondata, associd)
    current = qual['Level']
    print('Increasing level of %s (%d) from %d to %d' % (name, associd, current, level))
    qual['Level'] = level

def process_args():
    parser = argparse.ArgumentParser(
        prog='The Bloomin Casual',
        description='''
You pass by "The Storied Mode" public house just outside the docks, it beckons you in
like an old friend. You walk to the bar, meet eyes with the bartender, and ask for a
large pitcher of Bloomin Casual.

He serves it up luke warm, just as you like it.
''',
        epilog=''
    )
    parser.add_argument('-i', '--input',
                        type=str,
                        default='Autosave.json',
                        help="Input filename of JSON save game. Default: Autosave.json")
    parser.add_argument('-o', '--output',
                        default="Autosave.json",
                        help='Output filename of JSON save game. Default: Autosave.json')
    parser.add_argument('-b', '--backup',
                        type=bool,
                        default=True,
                        help="Back up the input json file. Default: True")
    parser.add_argument('-p', '--pretty',
                        action='store_true',
                        help='Load input and pretty print json to output file. When -p used with out any arguments the autosave will be pretty printed and saved in place')
    parser.add_argument('-f', '--fuel',
                        type=int,
                        default=None,
                        help="Add n fuel (integer)")
    parser.add_argument('-s', '--supplies',
                        type=int,
                        default=None,
                        help="Add n supplies (integer)")
    parser.add_argument('-c', '--coffee',
                        type=int,
                        default=None,
                        help="Add dark drop coffee beans (integer)")
    parser.add_argument('-l', '--list',
                        action='store_true',
                        help="List known qualities")
    parser.add_argument('-a', '--add',
                        type=str,
                        default=None,
                        help="Increase the level of the named quality (can also use ID)")
    parser.add_argument('-n', '--num',
                        type=int,
                        default=None,
                        help="Add 'n' of the quality named by the --add option")

    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    return parser.parse_args()

def main():
    args = process_args()

    input_file = Path(args.input).resolve()
    output_file = Path(args.output).resolve()

    rootpath = input_file.parent
    basename = input_file.stem

    if args.list:
        list_qualities(known_qualities_physical)
        list_qualities(known_qualities_ethereal)
        sys.exit(1)

    if args.backup:
        backup_date=datetime.now().strftime("%Y%m%d_%H%M")
        backup_file=Path(rootpath, "%s_bkup_%s.json" % (basename,backup_date)).resolve()
        print(backup_file)
        shutil.copyfile(input_file, backup_file)

    with open(input_file) as fp:
        try:
            jsondata = json.load(fp)
        except json.JSONDecodeError as e:
            print(e)

    chardata = get_character_data(jsondata)
    total_cargo = load_qualities_data(jsondata)
    shipdata = get_ship_data(jsondata)

    print_character_data(chardata)
    print_ship_data(shipdata, total_cargo)
    print_standard_props(jsondata)

    #
    # Update posessed qualities
    #
    updated=False
    if args.coffee:
        update_quality(jsondata, 'Coffee', args.coffee)
        updated=True

    if args.fuel:
        update_quality(jsondata, 'Fuel', args.fuel)
        updated=True

    if args.supplies:
        update_quality(jsondata, 'Supplies', args.supplies)
        updated=True

    if args.add:
        num = args.num if args.num is not None else 1
        try:
            # Check if it's an ID first
            qid = int(args.add)
            update_quality_by_id(jsondata, qid, num)
        except:
            # If not an ID, then treat as name
            update_quality(jsondata, args.add, num)
        updated=True

    #
    # Print updated quals
    #
    if updated:
        print()
        print_standard_props(jsondata)
        total_cargo = load_qualities_data(jsondata)
        if total_cargo > shipdata['hold_size']:
            print("Warning: Cargo exceeds hold size (%d vs. %d)" % (total_cargo, shipdata['hold_size']))

    #
    # Output updated json
    #
    indent_option=None
    if args.pretty:
        indent_option=4

    with open(output_file, "w") as fp:
        try:
            json.dump(jsondata, fp, indent=indent_option, sort_keys=False)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()
