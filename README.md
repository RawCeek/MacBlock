# MacBlock
A simple python script that scans and adds currently connected devices in a network to the Vianet (only raisecom variant) router's mac blocklist

## Requirements
Python libraries:
**BeautifulSoup**
**requests**

Other programs:
**arp-scan**

To install the python libraries, use:
```bash
pip3 install bs4 requests
```
if `arp-scan` is not installed, use:

Ubuntu/Debian:
```bash
sudo apt-get install arp-scan
```

Archlinux:
```bash
sudo pacman -S arp-scan
```

## Usage
Just run the python script `macblock.py`
If you haven't changed the router management page login credentials, the script will use the default login credentials.
If you have changed the login credentials change the **username** and **psd** in line 9 to match yours
