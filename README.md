markdown
# Linux TcpView

A simple **GTK-based network connection viewer** inspired by Windows' TcpView, built with Python, GTK3, and `psutil`.  
It allows you to monitor active TCP/UDP connections on Linux with filtering options and per-process color coding.

---

## Features
- View **TCP** and **UDP** connections
- Supports both **IPv4** and **IPv6**
- Toggle filters:
  - Active connections only
  - TCP / UDP
  - IPv4 / IPv6
- Each process is highlighted with a unique color
- Auto-refresh every 5 seconds
- Clean GTK3 interface with styled toggle buttons

---

## Requirements
- Python 3.7+
- GTK 3 (`python3-gi`)
- `psutil`

### Install dependencies

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3-gi python3-psutil gir1.2-gtk-3.0
Fedora:

bash
sudo dnf install python3-gobject python3-psutil gtk3
Usage
Clone the repository and run the script:

bash
git clone https://github.com/sohmee/linux-tcpview.git
cd linux-tcpview
python3 tcpview.py
Project Structure
Code
linux-tcpview/
├── tcpview.py   # Main application code
├── README.md    # Project documentation
How It Works
Uses psutil.net_connections() to fetch system connections

Displays them in a GTK TreeView

Filters applied via toggle buttons

Processes are assigned random colors for quick visual distinction

Contributing
Pull requests are welcome! If you’d like to add features (sorting, search, export, etc.), feel free to fork and submit improvements.

License
This project is licensed under the MIT License. See LICENSE for details.

👤 Author: sohmee
