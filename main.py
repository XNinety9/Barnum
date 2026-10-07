#!/usr/bin/env python3
"""Point d'entrée sans installation : python3 main.py [signe] [options].

Une fois installé (pip install -e .), la commande `barnum` fait la même chose.
"""
import sys

from barnum.cli import main

if __name__ == "__main__":
    sys.exit(main())
