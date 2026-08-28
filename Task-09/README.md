In this task, I developed a terminal-based Python application to implement, verify, and benchmark three different approaches to matrix multiplication. The goal was to observe the practical performance differences between standard and recursive algorithms. The application includes manual matrix entry, random generation, and an automated benchmarking suite that tests varying sizes, exports data to JSON, and generates comparative performance graphs.
Algorithms Implemented and Time Complexity

I implemented the following three algorithms for comparison:
Method	Time Complexity	Recurrence Relation
Naive Matrix Multiplication	O(N^3)	N/A
Divide and Conquer	O(N^3)	T(N) = 8T(N/2) + O(N^2)
Strassen's Algorithm	O(N^2.81)	T(N) = 7T(N/2) + O(N^2)

    Naive Matrix Multiplication: The standard mathematical approach utilizing three nested loops to multiply rows by columns.

    Divide and Conquer: A recursive approach that divides the matrices into four sub-matrices, executing 8 recursive multiplications and 4 additions.

    Strassen's Algorithm: An optimized recursive approach that reduces the number of recursive multiplications from 8 to 7 by utilizing algebraic combinations of the sub-matrices.

Benchmarking Approach

To ensure accurate testing, I designed the benchmarking suite with the following parameters:

    High-Resolution Timing: I used Python's time.perf_counter() to measure execution time down to fractions of a millisecond.

    Averaging: Since execution times fluctuate based on system resource allocation, the application runs each algorithm through multiple iterations and calculates the average elapsed time.

    Memory Tracking: I utilized Python's built-in tracemalloc library to track peak memory consumption during the execution of the algorithms.

    Verification: The output of the Naive algorithm acts as the baseline. Every time a recursive algorithm finishes, its output is verified against the baseline using numpy.array_equal to ensure mathematical accuracy.

Challenges Faced and Solutions

    Dimension Constraints (Powers of 2):
    Both the Divide & Conquer and Strassen's algorithms inherently rely on dividing matrices perfectly in half. This requires matrix dimensions to be exact powers of 2.
    Solution: I implemented dynamic matrix padding. Before running the recursive algorithms, the program calculates the next power of 2 and pads the matrix with zeros. After the calculation, the resulting matrix is "unpadded" back to its original dimensions.

    Python Recursion Overhead:
    While Strassen's algorithm is theoretically faster, Python's deep call stack makes raw recursion extremely slow for small matrices.
    Solution: I implemented a crossover threshold. For sub-matrices of size N <= 16, the recursive algorithms automatically fall back to the Naive method. This drastically improves real-world performance while maintaining the overall time complexity for large matrices.

Resources Used and Concepts Learned

    Concepts: I deepened my understanding of Divide and Conquer paradigms, Asymptotic Time Complexity analysis using the Master Theorem, and memory allocation profiling in Python.

    Resources: I referenced Introduction to Algorithms (Cormen, Leiserson, Rivest, Stein) to ensure Strassen's 7 algebraic equations were implemented perfectly, and utilized the official NumPy documentation for efficient array slicing and stacking techniques.

Additional Features Completed

    Added support for randomly generated matrices of varying sizes.

    Configured the program to execute each algorithm multiple times to display a true average execution time.

    Implemented automatic generation of performance comparison line graphs using Matplotlib.

    Added functionality to export benchmark results to a JSON file for external analysis.

    Integrated memory consumption profiling for each algorithm.

    Built a comprehensive CLI menu to allow automatic benchmarking across multiple matrix sizes without manual input.

How to Run

    Set up a Python virtual environment

code Bash

python3 -m venv venv
source venv/bin/activate

    Install the required software:
    

pip install -r requirements.txt

    Run the application:

code Bash

python3 main.py
