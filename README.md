# SpanningTreePractiser
Helps you understand the inner workings of the Spanning Tree protocol. An algorithm was used to solve the tree for you, where you get questions on how each edge should be defined.

There are 3 types of questions in this script:

1. Identifying the root bridge
2. Definitions of the bridge type abbreviations
3. Identifying bridge types

Where bridges are printed as [XY], edges are printed as |XY| (vertical) or -XY- (horizontal) and networks are printed as {XY}, where XY is their ID, abbreviation or name respectively.

It is possible to scale up the network by modifying the global variables "networkWidth" and "networkHeight". Be sure to make it an uneven amount larger than 5, since you need 3 components per connection: Bridge <-> Edge <-> Network (<-> Edge <-> Bridge).

Example images:

![Spanning Tree Practiser - Root identification](https://raw.githubusercontent.com/f13rce/SpanningTreePractiser/master/STPExampleImage.png)

# Installation

Clone the repository:

SSH: ``git clone git@github.com:/f13rce/SpanningTreePractiser.git && cd SpanningTreePractiser``

HTTPS: ``git clone https://github.com/f13rce/SpanningTreePractiser.git && cd SpanningTreePractiser``

Install the required packages:

``pip3 install -r requirements.txt``

If this doesn't work try:

``python3.6 -m pip install -r requirements.txt --user``

Then run the script:

``python3 stp.py``

# Requirements

See requirements.txt. Also requires a terminal with non-personalized output colors for proper coloring, which is needed to answer questions about highlighted sections.

To install the requirements, type in your terminal: ``pip3 install -r requirements.txt``
