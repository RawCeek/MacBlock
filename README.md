# MacBlock
A simple python script that scans and adds selected devices in your network to the Vianet (raisecom variant) router's mac blocklist.

## Requirements
Python libraries: 
**BeautifulSoup**,
**requests**

Other programs:
**arp-scan**

To install the python libraries, use:
```bash
pip3 install bs4 requests
```
If `arp-scan` is not installed, use:

Ubuntu/Debian:
```bash
sudo apt-get install arp-scan
```

Archlinux:
```bash
sudo pacman -S arp-scan
```

## Usage
Just run the python script `macblock.py`.

If you haven't changed the router management page login credentials, the script will use the default login credentials.

If you have changed the login credentials change the **username** and **psd** in line 9 to match yours.
