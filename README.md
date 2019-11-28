# SpanningTreePractiser
Helps you understand the inner workings of the Spanning Tree protocol. An algorithm was used to solve the tree for you, where you get questions on how each edge should be defined.

There are 3 types of questions in this script:

1. Identifying the root bridge
2. Definitions of the edge type abbreviations
3. Identifying edge types in a network

Example image:

![Spanning Tree Practiser - Root identification](https://raw.githubusercontent.com/f13rce/SpanningTreePractiser/master/STPExampleImage.png)

It is possible to scale up the network by modifying the global variables "networkWidth" and "networkHeight". Be sure to make it an uneven amount larger than 5, since you need 3 components per connection: Bridge <-> Edge <-> Network (<-> Edge <-> Bridge).

# Installation

Clone the repository:

SSH: ``git clone git@github.com:/f13rce/SpanningTreePractiser.git && cd SpanningTreePractiser``

HTTPS: ``git clone https://github.com/f13rce/SpanningTreePractiser.git && cd SpanningTreePractiser``

Install the required packages:

``pip3 install -r requirements.txt --user``

If this doesn't work try:

``python3.6 -m pip install -r requirements.txt --user``

Then run the script:

``python3 stp.py``

# Usage

The script allows one to modify its network size, as well as skipping abbreviation questions. Use the ``--help`` command to find out how to use this:

```
$ python stp.py --help
usage: This script will help you practise with spanning tree protocol topologies
       [-h] [--disable-banner] [-s] [-w {3,5,7,9,11}] [-H {3,5,7,9,11}]

optional arguments:
  -h, --help            show this help message and exit
  --disable-banner      Disable script banner
  -s, --skip-abbreviations
                        Do not ask abbreviation questions

Network size:
  Specify the network size parameters, these can be between 3 and 11 bridges
  and it has to be an odd number of bridges

  -w {3,5,7,9,11}, --width {3,5,7,9,11}
                        The width of the topology in bridges (default: 7)
  -H {3,5,7,9,11}, --height {3,5,7,9,11}
                        The height of the topology in bridges (default: 7)
```

# Requirements

See requirements.txt. Also requires a terminal with non-personalized output colors for proper coloring, which is needed to answer questions about highlighted sections.

To install the requirements, type in your terminal: ``pip3 install -r requirements.txt --user``
