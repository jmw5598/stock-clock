# Stock Clock

Simple clock for day trading.  Text changes color to red for the last 5 seconds of each minutes.  Also beeps the last 5 seconds before a new 5 minute.

## Requirements

- Python 3

## Running Instructions

- Clone the repo, `git clone git@github.com:jmw5598/stock-clock.git`.
- Navigate to the cloned repo in a terminal/cmd prompt, `cd <path-to-cloned-repo>/stock-clock`
- Create a python virtual env, `python3 -m venv .venv`
- Install dependencies `pip3 install -r requirements.txt`
- Run the application `python3 stock_clock.py`

The clock is moveable by click an dragging the clock. To close the clock, right clicking on the clock gives you a context menu with an exit option.  The settings options in this context menu currently doesn't do anything.  In the future I plan to be able to configure setting such as font color, background color, beep sound, etc.
