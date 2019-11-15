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
# | |__) |_|_ __ _  ___| |_ _ ___  ___ _ _|___/                       #
# |  ___/ '__/ _` |/ __| __| / __|/ _ \ '__|                          #
# | |   | | | (_| | (__| |_| \__ \  __/ |                             #
# |_|   |_|  \__,_|\___|\__|_|___/\___|_|                             #
#                                                                     #
#######################################################################
#                     Made by Ivar Slotboom :)		              #
#######################################################################
#######################################################################

# Imports
from termcolor import colored # colored outputs
from random import randrange # random bridge numbers
import sys # stdout without endl
import os # clear screen
import time # sleep

# Globals
networkWidth = 7 # Bridge-Edge-Network-Edge-Bridge
networkHeight = 7 # Same but vertical

network = [] #network[X][Y] = Edge,Network,(or)Bridge

highlightColor = "yellow"
highlightW = -1
highlightH = -1

rootW = -1
rootH = -1

# Classes
class Edge:
	classType = "Edge"
	representation = "-XY-"
	representationHor = "-XY-"
	representationVer = "|XY|"
	type = 0 # 0 = Unassigned; 1 = Root Port; 2 = Designated Port; 3 = Blocked Port;
	typeColors = ["white", "blue", "green", "red"]
	isHor = True
	color = typeColors[0]
	answer = "??"

	def UseVerticalRepresentation(self):
		self.representation = self.representationHor
		self.isHor = True

	def UseVerticalRepresentation(self):
		self.representation = self.representationVer
		self.isHor = False

	def SetEdgeType(self, aName):
		# Naming in representation
		if self.isHor:
			self.representation = self.representationHor.replace("X", aName[0]).replace("Y", aName[1])
		else:
			self.representation = self.representationVer.replace("X", aName[0]).replace("Y", aName[1])

		# Coloring
		if aName == "??":
			self.color = self.typeColors[0]
		if aName == "RP":
			self.color = self.typeColors[1]
		if aName == "DP":
			self.color = self.typeColors[2]
		if aName == "BP":
			self.color = self.typeColors[3]

	def SetAnswer(self, aAnswer):
		self.answer = aAnswer

	def IsBlocked(self):
		return (self.answer == "BP")

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
def GenerateField():
	global network

	# Initialize network array
	for w in range(networkWidth):
		network.append([])
		for h in range(networkHeight):
			network[w].append(None)


	randValues = []
	networkNameCount = 0

	for w in range(networkWidth):
		for h in range(networkHeight):
			# Bridge
			if (w+h) % 4 == 0 and h % 2 == 0:
				# Pick a random number as hop value - make sure it's unique
				number = 0
				while True:
					number = 10 + randrange(89)
					if not number in randValues:
						break

				# Make bridge
				network[w][h] = Bridge()
				network[w][h].SetValue(number)
			# Networks
			elif w % 2 == 0 and h % 2 == 0:
				char = chr(ord('A') + networkNameCount)
				char = "{}{}".format(char, char) # AA, BB, CC, etc
				networkNameCount += 1
				network[w][h] = Network()
				network[w][h].SetName(char)
			# Edges
			elif w % 2 == 0 or h % 2 == 0:
				network[w][h] = Edge()
				if w % 2 != 0:
					network[w][h].UseVerticalRepresentation()
			# Empty
			else:
				network[w][h] = Empty()

def DrawField():
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

def GetRootID():
	# Find root ID based on the lowest bridge value
	lowestID = 99999
	for w in range(networkWidth):
		for h in range(networkHeight):
			if network[w][h].classType == "Bridge":
				if network[w][h].value < lowestID:
					lowestID = network[w][h].value

	# Debug
	#print("Root ID: {}".format(lowestID))

	return lowestID

rootPaths = []
def SolveEdgeLabeling():
	global rootPaths
	global rootW
	global rootH

	# Get root ID
	rootID = int(GetRootID())

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
		#print("Finding paths to root ({}) from bridge {}".format(repr((rootW, rootH)), repr((bridge[0], bridge[1]))))
		path = []
		GetPaths(0, path, bridge[0], bridge[1])
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

		#print("Shortest path length: {} | Total paths: {}".format(shortestLen, len(shortestPaths)))

		# Find shortest path of those based on hop values
		minScore = 99999
		shortestPath = None
		for shortPath in shortestPaths:
			count = 0
			for entry in shortPath:
				if network[entry[0]][entry[1]].classType == "Bridge":
					count += network[entry[0]][entry[1]].value

			if count < minScore:
				shortestPath = shortPath
				minScore = count

		#print("Shortest route: {} | Path: {}".format(minScore, repr(shortestPath)))

		# Solve it
		isFromBridge = True
		for entry in shortestPath:
			if network[entry[0]][entry[1]].classType == "Bridge":
				isFromBridge = True
			elif network[entry[0]][entry[1]].classType == "Network":
				isFromBridge = False
			elif network[entry[0]][entry[1]].classType == "Edge":
				if isFromBridge:
					network[entry[0]][entry[1]].SetAnswer("RP")
				else:
					network[entry[0]][entry[1]].SetAnswer("DP")

def RemoveUnlinkedNetworks():
	global network

	for w in range(networkWidth):
		for h in range(networkHeight):
			if network[w][h].classType == "Network":
				hasActiveEdges = False

				if w > 0:
					if not network[w-1][h].IsBlocked():
						hasActiveEdges = True
				if w < networkWidth - 1:
					if not network[w+1][h].IsBlocked():
						hasActiveEdges = True
				if h > 0:
					if not network[w][h-1].IsBlocked():
						hasActiveEdges = True
				if h < networkHeight - 1:
					if not network[w][h+1].IsBlocked():
						hasActiveEdges = True

				if not hasActiveEdges:
					network[w][h] = Empty()
					if w > 0:
						network[w-1][h] = Empty()
					if w < networkWidth - 1:
						network[w+1][h] = Empty()
					if h > 0:
						network[w][h-1] = Empty()
					if h < networkHeight - 1:
						network[w][h+1] = Empty()

def GetPaths(aStep, aPreviousSteps, aW, aH):
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
		if network[aW-1][aH].classType != "Empty":
			GetPaths(aStep, steps, aW - 1, aH)

	# Right
	if aW + 1 < networkWidth - 1 and (aW + 1, aH) not in aPreviousSteps:
		if network[aW+1][aH].classType != "Empty":
			GetPaths(aStep, steps, aW + 1, aH)

	# Up
	if aH + 1 < networkHeight - 1 and (aW, aH + 1) not in aPreviousSteps:
		if network[aW][aH+1].classType != "Empty":
			GetPaths(aStep, steps, aW, aH + 1)

	# Down
	if aH > 0 and (aW, aH - 1) not in aPreviousSteps:
		if network[aW][aH-1].classType != "Empty":
			GetPaths(aStep, steps, aW, aH - 1)

# Main
def main():
	global highlightW
	global highlightH

	print( colored("#######################################################################\n\
#   _____                         _               _______             #\n\
#  / ____|                       (_)             |__   __|            #\n\
# | (___  _ __   __ _ _ __  _ __  _ _ __   __ _     | |_ __ ___  ___  #\n\
#  \___ \| '_ \ / _` | '_ \| '_ \| | '_ \ / _` |    | | '__/ _ \/ _ \ #\n\
#  ____) | |_) | (_| | | | | | | | | | | | (_| |    | | | |  __/  __/ #\n\
# |_____/| .__/ \__,_|_|_|_|_| |_|_|_| |_|\__, |    |_|_|  \___|\___| #\n\
# |  __ \| |           | | (_)             __/ |                      #\n\
# | |__) |_|_ __ _  ___| |_ _ ___  ___ _ _|___/                       #\n\
# |  ___/ '__/ _` |/ __| __| / __|/ _ \ '__|                          #\n\
# | |   | | | (_| | (__| |_| \__ \  __/ |                             #\n\
# |_|   |_|  \__,_|\___|\__|_|___/\___|_|                             #\n\
#                                                                     #\n\
#######################################################################\n\
#                     Made by Ivar Slotboom :)                        #\n\
#######################################################################", "magenta")
	)

	while True:
		# Create exercise field
		while True:
			try:
				GenerateField()
				SolveEdgeLabeling()
				RemoveUnlinkedNetworks()
				break
			except:
				# Something went wrong in the generation...
				# I'll let it retry until it just workTM :^)
				pass

		# Ask questions
		AskRootID()
		AskAbbreviations()
		AskEdgeLabeling()

		# Done!
		print(colored("All done!", "green"))
		inp = input("Would you like to practise again [Y/n]? ").lower()
		if (inp != "y"):
			print("Bye, good luck with the exam! :)")
			break

def AskRootID():
	# Root ID
	rootID = int(GetRootID())
	while True:
		DrawField()
		while True:
			try:
				rootInputID = int(input("Which bridge is the root? "))
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
def AskEdgeLabeling():

	# Wait a bit before clearing the screen
	time.sleep(1)

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

					# Draw the field
					highlightW = w
					highlightH = h
					DrawField()

					print("(Note that some answers could theoretically be correct, but is routed differently instead in this exercise.)")

					# Draw field and let user guess
					while True:
						inp = input("What is the type of the {} edge (RP, DP or BP)? ".format(colored("highlighted", highlightColor))).upper()
						if inp == network[w][h].answer:
							print(colored("Correct!", "green"))
							network[w][h].SetEdgeType(inp)
							time.sleep(1)
							highlightW = -1
							highlightH = -1
							break
						else:
							print(colored("Incorrect, try again", "red"))
							#print("Answer was: {}".format(network[w][h].answer))

	DrawField()


if __name__ == "__main__":
    # execute only if run as a script
    main()
