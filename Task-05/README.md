# Task 05: Grand Line Guardian

## Description
This is a terminal-based system monitoring tool written in Python, basically a simpler version of htop. It tracks running processes and updates every second, displaying the PID, process name, CPU usage, memory usage, and the total count of active processes.

## My Approach
I used the `psutil` library to fetch the system data and Python's built-in `curses` library to build the terminal UI. `curses` allows you to clear the screen and draw text at specific coordinates so the terminal doesn't just scroll infinitely. I set it up to sort the processes by CPU usage so the heaviest tasks stay at the top.

## Process Management & Linux Virtual Filesystem
A major requirement of this task was understanding how Linux actually gets this data. The Linux kernel uses a virtual filesystem (procfs) located at `/proc`. This isn't a real folder on the hard drive; it's generated dynamically in RAM by the kernel.

Every running process gets its own folder named after its PID (for example, `/proc/1/` for systemd). Inside these folders are files like `stat` and `status`. When my Python script requests CPU or memory data, under the hood, the system is essentially reading those virtual files and doing the math. 

## Things I Learned
* **Virtual Environments:** Setting up `venv` on Linux. Ubuntu actually requires you to install `python3-venv` via apt first to protect the global environment. I also used a .gitignore to keep the heavy venv folder off GitHub.
* **Transient Processes:** Processes start and die extremely fast. I had to use try/except blocks to catch `NoSuchProcess` errors because a process might close in the exact millisecond between finding its PID and reading its memory usage.
* **Curses:** Figuring out basic `curses` functions like hiding the cursor, making the screen refresh every 1000ms, and handling non-blocking keyboard input so the program doesn't freeze while waiting for the user to press 'q'.
* **Git:** Figuring out how to resolve diverged branches and merge conflicts when pushing local changes to a GitHub repo.

## How to run
(The virtual environment is not pushed to the repo, so you will need to set it up locally).

1. Clone the repo and cd into the Task-05 folder.
2. Create a virtual environment: `python3 -m venv venv`
3. Activate it: `source venv/bin/activate`
4. Install the requirements: `pip install -r requirements.txt`
5. Run the script: `python3 guardian.py`
6. Press 'q' to quit the application.
