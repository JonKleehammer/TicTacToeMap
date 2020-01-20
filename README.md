# TicTacToeMap
## *An abstract, visual representation of all tic tac toe board states*

### The Problem
Over the weekend I was at a lake without internet and wondered how many different board states there were in Tic-Tac-Toe, so I wrote a program to simulate every board state.

### Why Mathematical Methods didn't work
There were a few ways we could attempt to make math work for us on this problem, but it doesn't work out as expected. 
For instance we could think of the board as having 9 spots each having 3 choices (X placed here, O placed here, or nothing placed here) which would give us 3^9 combinations. But doing that math includes a board with all X's or a board with all O's and everything in between.
We could think of the last board state as having 5 X's and 4 O's, then do the math to see all the permutations for that problem, but similarly that would include boards that have 3 X's in a row AND 3 O's in a row.

### Simplifying the tree
Doing every single board state would be extremely messy, but in fact many board states are equivalent. For instance...
On the first turn of the game the player placing X's could place an X in the top left, but that's no different than placing an X in the bottom left, bottom right, or top left because the board is symmetric and the responses the other player can do are always relative to the other pieces. (There is no top or bottom, left or right. Everything is relative to the other shapes.
For example to illustrate, on the first turn the first player can place an X in a corner, side, or center. There are only 3 different moves on the first turn of the game once we take into account board rotations and symmetry.

## Example Image
![alt text](https://github.com/JonKleehammer/TicTacToeMap/blob/master/ExampleGraph)

### Image explanation
I used networkx (python graphing library) to create a graphical representation of every board state then matplotlib to create the image. I focused more on making it an artistic representation rather than a structured, but more clear, image. Parameters can be altered so the circles are smaller and edges more visible, but that wasn't my intention with this.

Each node represents a unique board state and the edges between them represent an X or O being placed traversing through the graph to a new board state. The colors and size represent which turn of the game it is, starting with warm colors the root board state is a large red node which represents an empty board, 3 nodes are connected which represents an X being placed in a corner, the side, and the center, this continues on until all board states are represented (moving to from large nodes with warm colors to smaller nodes with cooler colors as turns are taken)
