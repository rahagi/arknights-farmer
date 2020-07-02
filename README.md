# arknights-farmer

Farming assistant for Arknights.

## Installation

### Prerequisites

* Python >= 3.7.4
* pip
* adb from android platform-tools added to your `$PATH`

If you are installing this from source, you first need to install the dependencies using `pip`.
```bash
$ pip install -r requirements.txt
```

### From Source

Clone this repository using `git clone` command (or just download the `zip` version). 

Run the script using the following command inside the repo directory.
```bash
$ python3 -m arknights-farmer
```
### From PyPi

Soon

## Usage

```
usage: arknights-farmer [-h] [-p] [-s STAGE] [-c] [-r REFILL]

optional arguments:
  -h, --help            show this help message and exit

required args:
  -p, --penguin         use farm route data from penguin-stats.io
                        (experimental do not use)
  -s STAGE, --stage STAGE
                        manually add stage(s) to farm task (e.g. 1-7:100
                        4-4:25 (separated by whitespace))
  -c, --cont            continue from the most recent farming session

optional args:
  -r REFILL, --refill REFILL
                        how many times you want to refill. default is 0
```

### Connect to ADB

Use the `adb devices` command to check if your adb client is connected to your emulator.

Refer to your emulator manual on how to connect your adb client.

### Emulator Setting

Make sure to use the following display settings on your emulator:
* Display Resolution: 1280x720
* DPI: 240 DPI

### Examples

```bash
$ arknights-farmer -s 1-7:100           # runs 1-7 100 times (will stop whenever you run out of sanity)
$ arknights-farmer -s 1-7:100 -r 10     # runs 1-7 100 times with 10 times sanity refill (prioritizes using sanity potion)
$ arknights-farmer -c                   # continues the most recent halted farming session
```

You can safely stop the script using `Ctrl-C`. It will save the ongoing farming task(s) before quitting.

## Contributing
Pull requests are welcome. 

## License
Licensed under the MIT License. See `LICENSE` for more information.

## Disclaimer

It has not been clear whether it is safe to use this tool or not. I am not responsible for what happens to your account.

Use at your own risk.
