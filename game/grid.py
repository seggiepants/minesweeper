from random import randint
from enum import Enum
from game.cell import Cell, State

class GameState(Enum):
    """Enumeration of states of the game.
    PLAYING = Initial state when you have not won or lost.
    WIN = The current grid has exposed all non-bomb cells without exposing a bomb
    LOSE = The user opened a bomb when there are remaining normal cells to open
    """
    PLAYING = 0 # Default state, game is being played.
    WIN = 1     # You won the game.
    LOSE = 2    # You lost the game.

class Grid:
    """A minesweeper grid. Models the play area for minesweeper.
    You can reference grid locations and return a cell object for that 
    location as well as compute the number of bombs in neighboring cells
    for a location on the grid.
    """
    def __init__(self, width, height):
        """Intialize the grid and set it up for the desired width and height"""
        self._width = width
        self._height = height
        self._cells = [[Cell() for i in range(self._width)] for j in range(self._height)]
        self._state = GameState.PLAYING
        self.clear()
    
    def __eq__(self, other):
        """
        Check if two cell objects are the same.
        Parameters:
        * other: Cell object to compare against.
        Returns:
        * True if equavalent False if there are differences.
        Exceptions:
        * Will throw a type error if the other object is not a Cell.
        """
        if type(other) != Grid:
            raise TypeError(f'Expected Grid object, not a {type(other)}.')
        
        if self.width != other.width or \
           self.height != other.height or \
           self.state != other.state:
          return False

        for j in range(self.height):
          for i in range(self.width):
            if self.get(i, j) != other.get(i, j):
              return False
        
        return True
    
    def clear(self):
      """
      Clear all cells in the grid reset to default values.
      """
      for row in self._cells:
        for cell in row:
          cell.clear()
      self._state = GameState.PLAYING

    @property
    def width(self):
      """Return the width of the grid"""
      return self._width
  
    @property
    def height(self):
      """Return the height of the grid"""
      return self._height
  
    @property
    def state(self):
      """Return the current game state for the grid"""
      return self._state
    
    def get(self, col, row):
      """Returns the cell object at the given coordinates.
      Parameters:
      * col: The column (or x-coordinate) for the location on the grid to check.
        this runs from 0 to width - 1
      * row: The row (or y-coordinate) for the location on the grid to check.
        this runs from 0 to height - 1
      Returns:
      * Cell object for the grid at that location.
      Exceptions:
      * Raises a value error if the location at col, row is not on the grid.
      """
      if col < 0 or col >= self.width or row < 0 or row >= self.height:
          raise ValueError(f'location [{col}][{row}] is out of bounds.')
      
      return self._cells[row][col]
    
    def get_count_bombs(self):
      """Return the total number of bombs on the grid."""
      return sum(1 for row in self._cells for cell in row if cell.is_bomb)
    
    def get_count_remaining_to_open(self):
      """Return the total number of cells that need to be opened to win the game.
      Bombs are not counted."""
      return sum(1 for row in self._cells for cell in row if cell.is_bomb == False and cell.state != State.OPEN )

    def get_bomb_count(self, col, row):
      """Count up the number of bombs in neighboring cells for the given cell
      Parameters:
      * col: The column (or x-coordinate) for the location on the grid to check.
        this runs from 0 to width - 1
      * row: The row (or y-coordinate) for the location on the grid to check.
        this runs from 0 to height - 1
      Returns:
      * The count of bombs in neighboring cells. Note that it does not count the
        given cell. Neighboring cells that would not be on the grid are also not counted.
      Exceptions:
      * Raises a value error if the location at col, row is not on the grid.
      """
      if col < 0 or col >= self.width or row < 0 or row >= self.height:
          raise ValueError(f'location [{col}][{row}] is out of bounds.')
      
      bomb_count = 0
      for j in range(-1, 2):
          for i in range(-1, 2):
              # Skip the cell we are testing
              if i != 0 or j != 0:
                  # Skip if out of bounds
                  if row + j >= 0 and row + j < self.height and col + i >= 0 and col + i < self.width:
                      if self._cells[row + j][col + i].is_bomb:
                          bomb_count += 1
      return bomb_count
  
    def toggle_flagged(self, col, row):
      """Toggle the state of the cell at the given coordinates between 
      flagged and default state. Will not work unless the game state 
      is PLAYING. Cells also do not toggle if they are opened.
      Parameters:
      * col: The column (or x-coordinate) for the location on the grid to check.
        this runs from 0 to width - 1
      * row: The row (or y-coordinate) for the location on the grid to check.
        this runs from 0 to height - 1
      Exceptions:
      * Raises a value error if the location at col, row is not on the grid.
      """
      if col < 0 or col >= self.width or row < 0 or row >= self.height:
          raise ValueError(f'location [{col}][{row}] is out of bounds.')
      
      if self.state == GameState.PLAYING:
        self._cells[col][row].toggle_flag()
    
    def seed_grid(self, num_bombs):
      """
      Clear the grid and place the given number of bombs.
      Parameters:
      * num_bombs: The number of bombs to add to the grid.
      Exceptions:
      * raises an value error num_bombs >= width * height
      * raises a type error if num_bombs is not an integer
      """
      if num_bombs >= self.width * self.height:
        raise ValueError("Too many bombs to seed.")
      
      if type(num_bombs) != int:
        raise TypeError("num_bombs should be a positive integer.")
      
      self.clear()
      for _ in range(num_bombs):
        while True:
          # Get a random location on the grid.
          # it is acceptable if it is not already a
          # bomb
          x = randint(0, self.width - 1)
          y = randint(0, self.height - 1)
          if self.get(x, y).is_bomb == False:
            self.get(x, y).is_bomb = True
            break

    def open(self, col, row):
      """Open a cell, setting it to state OPEN and also recursively open 
      any unopened non-bomb neighbor cells if you have no neighboring bombs.
      Parameters:
      * col: The column (or x-coordinate) for the location on the grid to check.
        this runs from 0 to width - 1
      * row: The row (or y-coordinate) for the location on the grid to check.
        this runs from 0 to height - 1
      Exceptions:
      * Raises a value error if the location at col, row is not on the grid.
      """
      if col < 0 or col >= self.width or row < 0 or row >= self.height:
          raise ValueError(f'location [{col}][{row}] is out of bounds.')
      
      if self.state != GameState.PLAYING:
        # Do nothing if game over/won.
        return
      
      current = self.get(col, row)
      bomb_count = self.get_bomb_count(col, row)

      if current.state == State.OPEN:
        # Do nothing if we are already open.
        return
      
      if current.state == State.FLAGGED:
        # Don't open a flagged cell.
        return

      # Open it up now.
      current.state = State.OPEN
      
      if current.is_bomb: 
        # Change to game over state
        self._state = GameState.LOSE
      
      if bomb_count == 0:
        # Recursively set North, South, East and West non-bomb neighbors
        # North
        if row - 1 >= 0:
          neighbor = self.get(col, row - 1)
          if neighbor.is_bomb == False and neighbor.state == State.DEFAULT:
            self.open(col, row - 1)
        
        # South
        if row + 1 < self.height:
          neighbor = self.get(col, row + 1)
          if neighbor.is_bomb == False and neighbor.state == State.DEFAULT:
            self.open(col, row + 1)
        
        # West
        if col - 1 >= 0:
          neighbor = self.get(col - 1, row)
          if neighbor.is_bomb == False and neighbor.state == State.DEFAULT:
            self.open(col - 1, row)
        
        # East
        if col + 1 < self.width:
          neighbor = self.get(col + 1, row)
          if neighbor.is_bomb == False and neighbor.state == State.DEFAULT:
            self.open(col + 1, row)
      
      if self.get_count_bombs() == 0:
        self._state = GameState.WIN
