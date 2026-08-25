# Task 06: Pirate King's Scheduler

## Description
This is a CPU scheduling simulator written in Go. It takes a list of processes (representing pirate crews) with different arrival and burst times and runs them through three different scheduling algorithms: First Come First Serve (FCFS), Shortest Job First (SJF - Non-Preemptive), and Round Robin (RR). It then calculates and outputs the Completion Time, Turnaround Time, and Waiting Time for each process, along with a Gantt chart showing the execution order.

## My Approach
I used Go `structs` to define the blueprint for a process, storing variables like ID, ArrivalTime, and BurstTime. All processes are stored in a slice (Go's version of a dynamic array). I wrote separate functions for each algorithm. Since Go passes slices by reference, I wrote a helper function to create a fresh copy of the process slice for each algorithm so they wouldn't mess up each other's calculations.

## Things I Learned
Since this was my first time using Go, I learned a lot of the basic syntax and concepts:
* **Structs and Slices:** How to define data structures and manage dynamic arrays in a statically typed language.
* **The `make` function:** I used this to create boolean arrays of a specific size to keep track of which processes were completed in SJF and Round Robin.
* **Pass by Reference:** I learned that modifying a slice inside a function modifies the original array globally. I had to explicitly create copies of my arrays so the algorithms wouldn't overwrite each other.
* **Queues:** For Round Robin, I used a standard slice as a queue. I learned how to append new processes to the back (`append(queue, id)`) and pop them from the front (`queue = queue[1:]`).

## How to run
1. Clone this repository and `cd` into the Task-06 folder.
2. Make sure Golang is installed on your system.
3. Run the simulator using: `go run main.go`
