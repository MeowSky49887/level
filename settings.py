import os
import sys

"""VERSIONS_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "versions.json"))
CONFIG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "config.yaml"))
BIN_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "bin"))
CORE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "core"))"""

EXE_7Z = os.path.abspath(os.path.join(os.path.dirname(__file__), "7-Zip", "7za.exe"))

VERSIONS_FILE = os.path.abspath(os.path.join(os.path.dirname(sys.executable), "versions.json"))
CONFIG_FILE = os.path.abspath(os.path.join(os.path.dirname(sys.executable), "config.yaml"))
BIN_DIR = os.path.abspath(os.path.join(os.path.dirname(sys.executable), "bin"))
CORE_DIR = os.path.abspath(os.path.join(os.path.dirname(sys.executable), "core"))
