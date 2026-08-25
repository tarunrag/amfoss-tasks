import psutil

# 1. Get the total number of running processes (PIDs)
total_processes = len(psutil.pids())
print(f"Total Ships (Processes) on the Grand Line: {total_processes}\n")

# 2. Print a nice header for our columns
print(f"{'PID':<10} | {'NAME':<25} | {'CPU %':<10} | {'MEM %':<10}")
print("-" * 65)

# 3. Fetch data for running processes
count = 0
# process_iter() is the safest/fastest way to loop through running tasks
for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
    try:
        # proc.info contains the data we asked for above
        info = proc.info
        
        # Format the variables
        pid = info['pid']
        name = str(info['name'])[:24] # We cut the name off at 24 characters so it fits neatly
        cpu = info['cpu_percent'] or 0.0
        mem = info['memory_percent'] or 0.0
        
        # Print the row
        print(f"{pid:<10} | {name:<25} | {cpu:<10} | {mem:<10}")
        
        # We only want to print 10 processes for this quick test
        count += 1
        if count >= 10:  
            break
            
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        # Processes open and close in milliseconds on Linux.
        # If a process dies while we are trying to read it, this try/except 
        # safely ignores the error and moves to the next one!
        pass