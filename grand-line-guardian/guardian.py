import curses
import psutil

def main(stdscr):
    # --- 1. SETUP CURSES (THE UI ENVIRONMENT) ---
    curses.curs_set(0)      # Hide the blinking terminal cursor
    stdscr.nodelay(1)       # Don't pause the program waiting for the user to type
    stdscr.timeout(1000)    # Refresh the screen every 1000 milliseconds (1 second)

    # Infinite loop to keep updating the screen
    while True:
        # Clear the screen for the next frame
        stdscr.clear()

        # --- 2. FETCH SYSTEM DATA ---
        total_procs = len(psutil.pids())
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        # Sort the ships (processes) by CPU usage so the most active ones are at the top
        processes = sorted(processes, key=lambda p: p['cpu_percent'] or 0, reverse=True)

        # --- 3. DRAW THE UI ---
        # Get the current size of the terminal window (so we don't draw outside it)
        max_y, max_x = stdscr.getmaxyx()
        
        # stdscr.addstr(Y_COORDINATE, X_COORDINATE, "TEXT", STYLE)
        stdscr.addstr(0, 0, "🏴‍☠️  GRAND LINE GUARDIAN", curses.A_BOLD)
        stdscr.addstr(1, 0, f"Total Active Ships: {total_procs}")
        stdscr.addstr(1, 35, "Press 'q' to quit", curses.A_DIM)
        
        # Table Header (A_REVERSE makes it look like a highlighted bar)
        header = f"{'PID':<10} | {'NAME':<25} | {'CPU %':<10} | {'MEM %':<10}"
        stdscr.addstr(3, 0, header[:max_x-1], curses.A_REVERSE)

        # Draw the rows
        current_row = 4
        for p in processes:
            # If we reach the bottom of the terminal window, stop drawing!
            if current_row >= max_y - 1:
                break
            
            # Format the data (this fixes the crazy long decimals!)
            pid = p['pid']
            name = str(p['name'])[:24]
            cpu = f"{p['cpu_percent'] or 0.0:.1f}"
            mem = f"{p['memory_percent'] or 0.0:.1f}"
            
            row_str = f"{pid:<10} | {name:<25} | {cpu:<10} | {mem:<10}"
            
            # Try to draw the row. We slice it [:max_x-1] so it doesn't wrap around the screen
            try:
                stdscr.addstr(current_row, 0, row_str[:max_x-1])
            except curses.error:
                pass # Ignore errors if the terminal gets resized weirdly
            
            current_row += 1

        # Push everything we just drew to the actual screen
        stdscr.refresh()

        # --- 4. HANDLE KEYBOARD INPUT ---
        # Check if the user pressed a key
        key = stdscr.getch()
        
        # If they press 'q', break the loop and exit
        if key == ord('q'):
            break

# The wrapper safely starts curses and ensures your terminal goes back to normal 
# if the program crashes. Never run curses without it!
if __name__ == "__main__":
    curses.wrapper(main)