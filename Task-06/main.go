package main

import (
	"fmt"
	"sort"
)

type Process struct {
	ID             string
	ArrivalTime    int
	BurstTime      int
	CompletionTime int
	TurnAroundTime int
	WaitingTime    int
}

func main() {
	crews := []Process{
		{ID: "P1", ArrivalTime: 0, BurstTime: 5},
		{ID: "P2", ArrivalTime: 1, BurstTime: 3},
		{ID: "P3", ArrivalTime: 2, BurstTime: 8},
		{ID: "P4", ArrivalTime: 4, BurstTime: 6},
	}

	simulateFCFS(copyProcesses(crews))
	simulateSJF(copyProcesses(crews))
	
	// Pass our crews and a Time Quantum of 2
	simulateRoundRobin(copyProcesses(crews), 2)
}

func copyProcesses(src []Process) []Process {
	dst := make([]Process, len(src))
	copy(dst, src)
	return dst
}

func simulateFCFS(processes []Process) {
	fmt.Println("\n🏴‍☠️ --- First Come First Serve (FCFS) ---")
	sort.Slice(processes, func(i, j int) bool { return processes[i].ArrivalTime < processes[j].ArrivalTime })

	currentTime := 0
	totalTAT, totalWT := 0.0, 0.0

	for i := range processes {
		if currentTime < processes[i].ArrivalTime {
			currentTime = processes[i].ArrivalTime
		}
		currentTime += processes[i].BurstTime
		processes[i].CompletionTime = currentTime
		processes[i].TurnAroundTime = processes[i].CompletionTime - processes[i].ArrivalTime
		processes[i].WaitingTime = processes[i].TurnAroundTime - processes[i].BurstTime
		totalTAT += float64(processes[i].TurnAroundTime)
		totalWT += float64(processes[i].WaitingTime)
	}
	printResults(processes, processes, totalTAT, totalWT)
}

func simulateSJF(processes []Process) {
	fmt.Println("\n🏴‍☠️ --- Shortest Job First (SJF - Non-Preemptive) ---")
	n := len(processes)
	isCompleted := make([]bool, n)
	var executionOrder []Process

	currentTime, completedCount := 0, 0
	totalTAT, totalWT := 0.0, 0.0

	for completedCount != n {
		idx, minBurst := -1, 999999
		for i := 0; i < n; i++ {
			if processes[i].ArrivalTime <= currentTime && !isCompleted[i] {
				if processes[i].BurstTime < minBurst {
					minBurst = processes[i].BurstTime
					idx = i
				}
				if processes[i].BurstTime == minBurst && processes[i].ArrivalTime < processes[idx].ArrivalTime {
					idx = i
				}
			}
		}

		if idx != -1 {
			currentTime += processes[idx].BurstTime
			processes[idx].CompletionTime = currentTime
			processes[idx].TurnAroundTime = processes[idx].CompletionTime - processes[idx].ArrivalTime
			processes[idx].WaitingTime = processes[idx].TurnAroundTime - processes[idx].BurstTime
			totalTAT += float64(processes[idx].TurnAroundTime)
			totalWT += float64(processes[idx].WaitingTime)
			isCompleted[idx] = true
			completedCount++
			executionOrder = append(executionOrder, processes[idx])
		} else {
			currentTime++
		}
	}
	sort.Slice(processes, func(i, j int) bool { return processes[i].ID < processes[j].ID })
	printResults(executionOrder, processes, totalTAT, totalWT)
}

// --- ALGORITHM 3: Round Robin ---
func simulateRoundRobin(processes []Process, timeQuantum int) {
	fmt.Printf("\n🏴‍☠️ --- Round Robin (RR) [Time Quantum: %d] ---\n", timeQuantum)

	n := len(processes)
	remBurst := make([]int, n) // We need to track how much time each ship has left!
	for i := 0; i < n; i++ {
		remBurst[i] = processes[i].BurstTime
	}

	sort.Slice(processes, func(i, j int) bool { return processes[i].ArrivalTime < processes[j].ArrivalTime })

	currentTime, completedCount := 0, 0
	totalTAT, totalWT := 0.0, 0.0
	var executionOrder []Process
	var queue []int // This slice will act as our line/queue
	inQueue := make([]bool, n)

	// Jump to the first arrival time if the CPU is idle at 0
	if processes[0].ArrivalTime > currentTime {
		currentTime = processes[0].ArrivalTime
	}
	
	// Add the first ship to the queue
	queue = append(queue, 0)
	inQueue[0] = true

	for completedCount != n {
		if len(queue) == 0 {
			currentTime++
			for i := 0; i < n; i++ {
				if processes[i].ArrivalTime <= currentTime && !inQueue[i] && remBurst[i] > 0 {
					queue = append(queue, i)
					inQueue[i] = true
				}
			}
			continue
		}

		// Pop the first ship from the front of the queue
		idx := queue[0]
		queue = queue[1:]
		inQueue[idx] = false

		// Determine how long it will run (either the Time Quantum, or whatever it has left)
		runTime := timeQuantum
		if remBurst[idx] < timeQuantum {
			runTime = remBurst[idx]
		}

		currentTime += runTime
		remBurst[idx] -= runTime
		executionOrder = append(executionOrder, Process{ID: processes[idx].ID})

		// Check if any NEW ships arrived while this one was running, add them to queue first!
		for i := 0; i < n; i++ {
			if processes[i].ArrivalTime <= currentTime && !inQueue[i] && remBurst[i] > 0 && i != idx {
				queue = append(queue, i)
				inQueue[i] = true
			}
		}

		// If our current ship isn't finished, put it at the BACK of the queue
		if remBurst[idx] > 0 {
			queue = append(queue, idx)
			inQueue[idx] = true
		} else {
			// It finished! Calculate its stats.
			processes[idx].CompletionTime = currentTime
			processes[idx].TurnAroundTime = processes[idx].CompletionTime - processes[idx].ArrivalTime
			processes[idx].WaitingTime = processes[idx].TurnAroundTime - processes[idx].BurstTime
			totalTAT += float64(processes[idx].TurnAroundTime)
			totalWT += float64(processes[idx].WaitingTime)
			completedCount++
		}
	}

	sort.Slice(processes, func(i, j int) bool { return processes[i].ID < processes[j].ID })
	printResults(executionOrder, processes, totalTAT, totalWT)
}

func printResults(gantt []Process, table []Process, totalTAT float64, totalWT float64) {
	fmt.Println("Timeline (Gantt Chart):")
	fmt.Print("|")
	for _, p := range gantt {
		fmt.Printf("== %s ==|", p.ID)
	}
	fmt.Println()

	fmt.Println("\nPID\tArrival\tBurst\tCompletion\tTurnaround\tWaiting")
	fmt.Println("----------------------------------------------------------------")
	for _, p := range table {
		fmt.Printf("%s\t%d\t%d\t%d\t\t%d\t\t%d\n", p.ID, p.ArrivalTime, p.BurstTime, p.CompletionTime, p.TurnAroundTime, p.WaitingTime)
	}

	n := float64(len(table))
	fmt.Printf("\nAverage Turnaround Time: %.2f\n", totalTAT/n)
	fmt.Printf("Average Waiting Time: %.2f\n\n", totalWT/n)
}