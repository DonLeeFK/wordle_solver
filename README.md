# Wordle Solver

A Python program that assists in solving Wordle puzzles by recommending optimal guesses based on entropy and word frequency. Uses pattern matching to efficiently narrow down possibilities.

## Installation

1. **Install Dependencies**  
   Requires Python 3. Run this command:
   ```bash
   pip install numpy scipy wordfreq tqdm
   ```
2. **Download Word List**
Use the provided words file containing valid 5-letter words. Place it in the same directory as the Python script.

## Usage
### Basic Execution
```bash
   python solveWordle.py
```
### How to Play
1. **Start the Solver**  

The first recommended word will appear as R A T E S. Enter this in your Wordle game.

2. **Report Results**

After each guess, input Wordle's color pattern using:

G = 🟩 (correct position)
Y = 🟨 (wrong position)
R/B = 🟥 (not in word - accepts red "R" or black "B" inputs)
Use 5 letters without spaces (e.g., GYBRR or BYGBR).
3. **Follow Suggestions**

The program will recommend the next optimal word. Either:

Press Enter to accept the suggestion
Type your own 5-letter word

4. **Repeat Until Solved**

Continue until you get the all-green (GGGGG) solution.

3. **Example Session**
   ```
   Wordle Solver v0.1
    T A R E S
    INPUT RESPONSE:  # User sees 🟩🟨🟥🟥🟨 in Wordle
    GYRRY  # User types response
    First attempt: C L A N G  score: 4.8
    INPUT WORD:  # User presses Enter to use "CLANG"
    INPUT RESPONSE:  # User got 🟥🟩🟥🟩🟥
    BRGBB  # Alternate input format shown
    ...
    ```

## Perks
Tares is chosen as the first recommended word because it is the word that gives max entropy using my word list. Getting this result requires a fair amount of calculation(about 10 minutes on my machine) because you have to do the most amount of computation without any prior information. So I'll just use it as is to save time. You can always choose you favorite first word like crane by changing the code.