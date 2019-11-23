#!/usr/bin/env python3
#######################################################################
#######################################################################
#######################################################################
#   _____                         _               _______             #
#  / ____|                       (_)             |__   __|            #
# | (___  _ __   __ _ _ __  _ __  _ _ __   __ _     | |_ __ ___  ___  #
#  \___ \| '_ \ / _` | '_ \| '_ \| | '_ \ / _` |    | | '__/ _ \/ _ \ #
#  ____) | |_) | (_| | | | | | | | | | | | (_| |    | | | |  __/  __/ #
# |_____/| .__/ \__,_|_|_|_|_| |_|_|_| |_|\__, |    |_|_|  \___|\___| #
# |  __ \| |           | | (_)             __/ |                      #
# | |__) |_|_ __ _  ___| |_ _  ___ ___    |___/                       #
# |  ___/ '__/ _` |/ __| __| |/ __/ _ \                               #
# | |   | | | (_| | (__| |_| | (_|  __/                               #
# |_|   |_|  \__,_|\___|\__|_|\___\___|                               #
#                                                                     #
#######################################################################
#                     Made by Ivar Slotboom :)		              #
#######################################################################
#######################################################################

# Imports
from termcolor import colored  # colored outputs
from random import randrange  # random bridge numbers
from argparse import ArgumentParser # argument parser
import sys  # stdout without endl
import os  # clear screen
import time  # sleep
import math  # floor
import random  # range

network = []  # network[X][Y] = Edge,Network,(or)Bridge

highlightColor = "yellow"
highlightW = -1
highlightH = -1

rootW = -1
rootH = -1


# Classes
class Edge:
    classType = "Edge"
    representationHor = "-XY-"
    representationVer = "|XY|"
    representation = representationHor
    type = 0  # 0 = Unassigned; 1 = Root Port; 2 = Designated Port; 3 = Blocked Port;
    typeColors = ["white", "blue", "green", "red"]
    isHor = True
    color = typeColors[0]
    answer = "??"
    port = -1

    def UseHorizontalRepresentation(self):
        self.representation = self.representationHor
        self.isHor = True

    def UseVerticalRepresentation(self):
        self.representation = self.representationVer
        self.isHor = False

    def SetPortNumber(self, aVal):
        self.port = aVal
        portStr = list(str(aVal))
        reprStr = list(self.representation)
        reprStr[1] = portStr[0]
        reprStr[2] = portStr[1]
        self.representation = "".join(reprStr)

    def SetEdgeType(self, aName):
        # Naming in representation
        reprStr = list(self.representation)
        reprStr[1] = aName[0]
        reprStr[2] = aName[1]
        self.representation = "".join(reprStr)

        # Coloring
        if aName == "RP":
            self.color = self.typeColors[1]
        elif aName == "DP":
            self.color = self.typeColors[2]
        elif aName == "BP":
            self.color = self.typeColors[3]
        else:
            self.color = self.typeColors[0]

    def SetAnswer(self, aAnswer):
        self.answer = aAnswer

    def IsBlocked(self):
        return self.answer == "BP"


class Network:
    classType = "Network"
    networkRepresentation = "{XX}"
    representation = "{XX}"
    name = ""
    color = "cyan"

    def SetName(self, aName):
        self.name = aName
        self.representation = self.networkRepresentation.replace("XX", aName)


class Bridge:
    classType = "Bridge"
    bridgeRepresentation = "[XX]"
    representation = "[XX]"
    color = "magenta"

    value = 0

    def SetValue(self, aValue):
        self.value = aValue
        self.representation = self.bridgeRepresentation.replace("XX", "{}".format(aValue))


class Empty:
    classType = "Empty"
    representation = "    "
    color = "grey"


# Funcs
def parse_args(args=None):
    parser = ArgumentParser("This script will help you practise with spanning tree protocol topologies")
    parser.add_argument('--disable-banner', action='store_true', help='Disable script banner')
    parser.add_argument('-s', '--skip-abbreviations', action='store_true', help='Do not ask abbreviation questions')
    size_args = parser.add_argument_group(
        'Network size',
        'Specify the network size parameters, these can be between 3 and 11 bridges '
        'and it has to be an odd number of bridges'
    )
    size_args.add_argument(
        '-w',
        '--width',
        type=int,
        choices=list(filter(lambda x: (x % 2 != 0), range(3, 12))),
        default=7,
        help='The width of the topology in bridges (default: 7)'
    )
    size_args.add_argument(
        '-H',
        '--height',
        type=int,
        choices=list(filter(lambda x: (x % 2 != 0), range(3, 12))),
        default=7,
        help='The height of the topology in bridges (default: 7)'
    )
    return parser.parse_args(args)


def GenerateField(networkWidth, networkHeight):
    global network

    # Initialize network array
    for w in range(networkWidth):
        network.append([])
        for h in range(networkHeight):
            network[w].append(None)

    randValues = []
    portNumbers = []
    networkNameCount = 0

    for w in range(networkWidth):
        for h in range(networkHeight):
            # Bridge
            if (w + h) % 4 == 0 and h % 2 == 0:
                # Pick a random number as hop value - make sure it's unique
                number = 0
                while True:
                    number = 10 + randrange(89)
                    if not number in randValues:
                        randValues.append(number)
                        break

                # Make bridge
                network[w][h] = Bridge()
                network[w][h].SetValue(number)
            # Networks
            elif w % 2 == 0 and h % 2 == 0:
                char = chr(ord('A') + networkNameCount)
                char = "{}{}".format(char, char)  # AA, BB, CC, etc
                networkNameCount += 1
                network[w][h] = Network()
                network[w][h].SetName(char)
            # Edges
            elif w % 2 == 0 or h % 2 == 0:
                network[w][h] = Edge()
                if w % 2 != 0:
                    network[w][h].UseVerticalRepresentation()
                else:
                    network[w][h].UseHorizontalRepresentation()

                # Pick a random number as hop value - make sure it's unique
                number = 0
                while True:
                    number = 10 + randrange(89)
                    if number not in portNumbers:
                        portNumbers.append(number)
                        break
                network[w][h].SetPortNumber(number)

            # Empty
            else:
                network[w][h] = Empty()


def DrawField(networkWidth, networkHeight):
    global highlightW
    global highlightH

    # For every entry, print it
    for w in range(networkWidth):
        for h in range(networkHeight):
            if highlightW == w and highlightH == h:
                sys.stdout.write(colored(network[w][h].representation, highlightColor))
            else:
                sys.stdout.write(colored(network[w][h].representation, network[w][h].color))

        sys.stdout.write("\n")


def GetRootID(networkWidth, networkHeight):
    # Find root ID based on the lowest bridge value
    lowestID = 99999
    for w in range(networkWidth):
        for h in range(networkHeight):
            if network[w][h].classType == "Bridge":
                if network[w][h].value < lowestID:
                    lowestID = network[w][h].value

    # Debug
    # print("Root ID: {}".format(lowestID))

    return lowestID


rootPaths = []


def SolveEdgeLabeling(networkWidth, networkHeight):
    global rootPaths
    global rootW
    global rootH

    # Get root ID
    rootID = int(GetRootID(networkWidth, networkHeight))

    # Find root X/Y
    bridges = []
    for w in range(networkWidth):
        for h in range(networkHeight):
            if network[w][h].classType == "Bridge":
                if network[w][h].value == rootID:
                    rootW = w
                    rootH = h
                else:
                    bridges.append((w, h))

    # Set default values for edges
    for w in range(networkWidth):
        for h in range(networkHeight):
            if network[w][h].classType == "Edge":
                network[w][h].SetAnswer("BP")

    # Find every path possible per bridge
    for bridge in bridges:
        rootPaths = []
        # print("Finding paths to root ({}) from bridge {}".format(repr((rootW, rootH)), repr((bridge[0], bridge[1]))))
        path = []
        GetPaths(0, path, bridge[0], bridge[1], networkWidth, networkHeight)
        paths = rootPaths

        # Find shortest paths based on hop count
        shortestPaths = []
        shortestLen = 99999
        for path in rootPaths:
            if len(path) == 0:
                continue

            if len(path) < shortestLen:
                shortestPaths = []
                shortestLen = len(path)
            shortestPaths.insert(0, path)

        # print("Shortest path length: {} | Total paths: {}".format(shortestLen, len(shortestPaths)))

        # Tie breaker: find shortest path based on hop values from bridges
        minScore = 99999
        shortestCountPaths = []
        for shortPath in shortestPaths:
            count = 0
            for entry in shortPath:
                if network[entry[0]][entry[1]].classType == "Bridge":
                    count += network[entry[0]][entry[1]].value

            if count < minScore:
                minScore = count
                shortestCountPaths = []
                shortestCountPaths.append(shortPath)
            elif count == minScore:
                shortestCountPaths.append(shortPath)

        # print("Shortest route: {} | Path: {}".format(minScore, repr(shortestPath)))

        # Tie breaker: Lowest port number
        shortestPath = None
        if len(shortestCountPaths) > 1:
            minPort = 999999
            for path in shortestCountPaths:
                if network[path[1][0]][path[1][1]].port < minPort:
                    minPort = network[path[1][0]][path[1][1]].port
                    shortestPath = path
        else:
            shortestPath = shortestCountPaths[0]

        # Solve it
        isFromBridge = False
        # for entry in shortestPath:
        for i in range(len(shortestPath)):
            entry = shortestPath[i]
            if network[entry[0]][entry[1]].classType == "Bridge":
                isFromBridge = True
            elif network[entry[0]][entry[1]].classType == "Network":
                isFromBridge = False
            elif network[entry[0]][entry[1]].classType == "Edge":
                if isFromBridge:
                    network[entry[0]][entry[1]].SetAnswer("RP")
                else:
                    network[entry[0]][entry[1]].SetAnswer("DP")

    # Apply port numbers
    # Find duplicate RP entries, but pick one where the others become a BP
    for w in range(networkWidth):
        for h in range(networkHeight):
            rootPorts = []
            if network[w][h].classType == "Bridge":
                if w > 0:
                    if network[w - 1][h].classType == "Edge":
                        if network[w - 1][h].answer == "RP":
                            rootPorts.append((w - 1, h))
                if w < networkWidth - 1:
                    if network[w + 1][h].classType == "Edge":
                        if network[w + 1][h].answer == "RP":
                            rootPorts.append((w + 1, h))
                if h > 0:
                    if network[w][h - 1].classType == "Edge":
                        if network[w][h - 1].answer == "RP":
                            rootPorts.append((w, h - 1))
                if h < networkHeight - 1:
                    if network[w][h + 1].classType == "Edge":
                        if network[w][h + 1].answer == "RP":
                            rootPorts.append((w, h + 1))

            if len(rootPorts) > 1:
                # print("Removing duplicate root ports, picking lowest port and others will become BP")
                lowestPort = (-1, -1)
                minPort = 99999
                for rp in rootPorts:
                    if network[rp[0]][rp[1]].port < minPort:
                        minPort = network[rp[0]][rp[1]].port
                        lowestPort = rp
                for rp in rootPorts:
                    if rp == lowestPort:
                        continue
                    network[rp[0]][rp[1]].SetAnswer("BP")


def RemoveUnlinkedNetworks(networkWidth, networkHeight):
    global network

    for w in range(networkWidth):
        for h in range(networkHeight):
            if network[w][h].classType == "Network":
                hasActiveEdges = False

                if w > 0:
                    if not network[w - 1][h].IsBlocked():
                        hasActiveEdges = True
                if w < networkWidth - 1:
                    if not network[w + 1][h].IsBlocked():
                        hasActiveEdges = True
                if h > 0:
                    if not network[w][h - 1].IsBlocked():
                        hasActiveEdges = True
                if h < networkHeight - 1:
                    if not network[w][h + 1].IsBlocked():
                        hasActiveEdges = True

                if not hasActiveEdges:
                    network[w][h] = Empty()
                    if w > 0:
                        network[w - 1][h] = Empty()
                    if w < networkWidth - 1:
                        network[w + 1][h] = Empty()
                    if h > 0:
                        network[w][h - 1] = Empty()
                    if h < networkHeight - 1:
                        network[w][h + 1] = Empty()


def RemoveRandomNetworks(networkWidth, networkHeight):
    # Removal count
    maxRemovalCount = 2

    # Find odds to remove a network
    totalNetworks = 0
    for w in range(networkWidth):
        for h in range(networkHeight):
            if network[w][h].classType == "Network":
                totalNetworks += 1
    chance = math.ceil(100.0 / totalNetworks)

    # Remove networks
    removedCount = 0
    for w in range(networkWidth):
        if w == 0 or w == networkWidth - 1:
            continue

        for h in range(networkHeight):
            if h == 0 or h == networkHeight - 1:
                continue

            if network[w][h].classType == "Network":
                if random.randint(0, 100) <= chance:
                    network[w][h] = Empty()
                    if w > 0:
                        network[w - 1][h] = Empty()
                    if w < networkWidth - 1:
                        network[w + 1][h] = Empty()
                    if h > 0:
                        network[w][h - 1] = Empty()
                    if h < networkHeight - 1:
                        network[w][h + 1] = Empty()

                    removedCount += 1
                    if removedCount >= maxRemovalCount:
                        return
                else:
                    # Increase the odds
                    chance *= 3


def GetPaths(aStep, aPreviousSteps, aW, aH, networkWidth, networkHeight):
    global rootPaths
    global rootW
    global rootH

    aStep += 1

    # Make a new array because python re-uses memory
    steps = []
    for step in aPreviousSteps:
        steps.append(step)
    steps.append((aW, aH))

    # Stop if we're at the root
    if aW == rootW and aH == rootH:
        rootPaths.insert(0, steps)
        return

    # Left
    if aW > 0 and (aW - 1, aH) not in steps:
        if network[aW - 1][aH].classType != "Empty":
            GetPaths(aStep, steps, aW - 1, aH, networkWidth, networkHeight)

    # Right
    if aW + 1 < networkWidth - 1 and (aW + 1, aH) not in aPreviousSteps:
        if network[aW + 1][aH].classType != "Empty":
            GetPaths(aStep, steps, aW + 1, aH, networkWidth, networkHeight)

    # Up
    if aH + 1 < networkHeight - 1 and (aW, aH + 1) not in aPreviousSteps:
        if network[aW][aH + 1].classType != "Empty":
            GetPaths(aStep, steps, aW, aH + 1, networkWidth, networkHeight)

    # Down
    if aH > 0 and (aW, aH - 1) not in aPreviousSteps:
        if network[aW][aH - 1].classType != "Empty":
            GetPaths(aStep, steps, aW, aH - 1, networkWidth, networkHeight)


# Main
def main(args=None):
    args = parse_args(args)

    if not args.disable_banner:
        DrawHeader()

    while True:
        # Create exercise field
        while True:
            try:
                GenerateField(args.width, args.height)
                RemoveRandomNetworks(args.width, args.height)
                SolveEdgeLabeling(args.width, args.height)
                RemoveUnlinkedNetworks(args.width, args.height)
                break
            except IndexError:
                # Something went wrong in the generation...
                # I'll let it retry until it just workTM :^)
                pass

        # Ask questions
        AskRootID(args.width, args.height)
        if not args.skip_abbreviations:
            AskAbbreviations()
        AskEdgeLabeling(args.width, args.height, drawheader=True if not args.disable_banner else False)

        # Done!
        print(colored("All done!", "green"))
        inp = input("Would you like to practice again [Y/n]? ").lower()
        if inp != "y":
            print("Bye, good luck with the exam! :)")
            break


def DrawHeader():
    print(colored("#######################################################################\n\
#   _____                         _               _______             #\n\
#  / ____|                       (_)             |__   __|            #\n\
# | (___  _ __   __ _ _ __  _ __  _ _ __   __ _     | |_ __ ___  ___  #\n\
#  \___ \| '_ \ / _` | '_ \| '_ \| | '_ \ / _` |    | | '__/ _ \/ _ \ #\n\
#  ____) | |_) | (_| | | | | | | | | | | | (_| |    | | | |  __/  __/ #\n\
# |_____/| .__/ \__,_|_|_|_|_| |_|_|_| |_|\__, |    |_|_|  \___|\___| #\n\
# |  __ \| |           | | (_)             __/ |                      #\n\
# | |__) |_|_ __ _  ___| |_ _ ___  ___ _ _|___/                       #\n\
# |  ___/ '__/ _` |/ __| __| / __|/ _ \ '__|                          #\n\
# | |   | | | (_| | (__| |_| |(__|  __/ |                             #\n\
# |_|   |_|  \__,_|\___|\__|_\___/\___|_|                             #\n\
#                                                                     #\n\
#######################################################################\n\
#                     Made by Ivar Slotboom :)                        #\n\
#######################################################################", "magenta")
          )


def DrawLabeling():
    print("Labeling:")
    print(colored("\t[XY]: Bridge, where XY is the ID based on its MAC address and configured priority", "magenta"))
    print(colored("\t-XY-: Edge (horizontal), where XY is the port number", "white"))
    print(colored("\t|XY|: Edge (vertical), where XY is the port number", "white"))
    print(colored("\t{XY}: Network, where XY is the network name", "cyan"))


def AskRootID(networkWidth, networkHeight):
    # Root ID
    rootID = int(GetRootID(networkWidth, networkHeight))
    while True:
        print("")
        print("Consider the following network:")
        DrawField(networkWidth, networkHeight)
        while True:
            print("")
            DrawLabeling()
            print("")
            try:
                rootInputID = int(input("Which bridge is the root (number only)? "))
                break
            except ValueError:
                print("Please only type the number of the root bridge.")
        if rootInputID == rootID:
            print(colored("Correct!", "green"))
            break
        else:
            print(colored("Incorrect, try again.", "red"))


def AskAbbreviations():
    # Abbreviations
    # DP
    while True:
        inp = input("What does DP stand for? ").lower()
        if inp == "designated port":
            print(colored("Correct!", "green"))
            break
        else:
            print(colored("Incorrect, try again.", "red"))

    # RP
    while True:
        inp = input("What does RP stand for? ").lower()
        if inp == "root port":
            print(colored("Correct!", "green"))
            break
        elif inp == "research project":
            print(colored("Well yes, but actually no.", "red"))
        else:
            print(colored("Incorrect, try again.", "red"))

    # BP
    while True:
        inp = input("What does BP stand for? ").lower()
        if inp == "blocked port":
            print(colored("Correct!", "green"))
            break
        else:
            print(colored("Incorrect, try again.", "red"))


__TEST_EDGE__ = False


def AskEdgeLabeling(networkWidth, networkHeight, drawheader=True):
    # Wait a bit before clearing the screen
    time.sleep(1)

    if __TEST_EDGE__:
        print("PRE:")
        print("Root bridge: {}".format(colored("[{}]".format(GetRootID(networkWidth, networkHeight)), "magenta")))
        DrawField(networkWidth, networkHeight)
        print("POST:")

    global highlightW
    global highlightH

    # Edge labeling
    for w in range(networkWidth):
        for h in range(networkHeight):
            if network[w][h].classType == "Edge":
                if __TEST_EDGE__:
                    network[w][h].SetEdgeType(network[w][h].answer)
                else:
                    # Clear screen on both *nix-like and Windows
                    try:
                        os.system('cls')
                        os.system('clear')
                    except:
                        # Ignore OS-relates errors
                        pass

                    if drawheader:
                        DrawHeader()

                    # Draw the field
                    print("")
                    print("In the context of the same network:")
                    highlightW = w
                    highlightH = h
                    DrawField(networkWidth, networkHeight)
                    print("")
                    DrawLabeling()
                    print("")

                    # Draw field and let user guess
                    while True:
                        inp = input("What is the type of the {} edge (RP, DP or BP)? ".format(
                            colored("highlighted", highlightColor))).upper()
                        if inp == network[w][h].answer:
                            print(colored("Correct!", "green"))
                            network[w][h].SetEdgeType(inp)
                            time.sleep(1)
                            highlightW = -1
                            highlightH = -1
                            break
                        else:
                            print(colored("Incorrect, try again", "red"))
                        # print("Answer was: {}".format(network[w][h].answer))

    print("")
    print("Final network:")
    DrawField(networkWidth, networkHeight)
    print("")


if __name__ == "__main__":
    # execute only if run as a script
    main()
