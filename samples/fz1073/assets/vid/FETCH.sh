#!/bin/sh
# Real footage is not committed (mp4 is gitignored). Re-fetch from Wikimedia Commons with credits:
cd "$(dirname "$0")/../.."
python3 commons.py getvid "File:Airplane inside while taking off.webm" cabin_takeoff 20 16
python3 commons.py getvid "File:Clouds from Airplane Window 1 2016-08-29.webm" window_clouds 0 18
python3 commons.py getvid "File:Up in the Clouds - May 2019.webm" above_clouds 0 20
python3 commons.py getvid "File:Landing aircraft - Haneda - 2021 3 31.webm" landing_haneda 0 13
