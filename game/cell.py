from enum import Enum

class State(Enum):
    """Enumeration of states for a Cell object.
    DEFAULT = Initial state a unknown cell.
    FLAGGED = The cell has been flagged, not yet opened. Used to mark potential bombs
    OPEN = The cell has been exposed (for better or worse)
    """
    DEFAULT = 0 # Initial state of the cell
    FLAGGED = 1 # Flagged as a potential bomb.
    OPEN = 2    # Cell has been clicked exposed.

class Cell:
    """Models a cell in a minesweeper grid. It has a current state
    and a flag that says wether it is a bomb or not.
    """
    def __init__(self, is_bomb = False, state = State.DEFAULT):
        """Create the cell object with the given state.
        Parameters:
        * is_bomb: Say if the cell is a bomb or not defaults to false.
        * state: Set the cell's current state, defaults to State.DEFAULT
        """
        self.is_bomb = is_bomb
        self.state = state
    
    def clear(self):
        """
        Reset the cell to default state.
        """
        self.is_bomb = False
        self.state = State.DEFAULT
    
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
        if type(other) != Cell:
            raise TypeError(f'Expected Cell object, not a {type(other)}.')
        
        return self.is_bomb == other.is_bomb and self.state == other.state

    def toggle_flag(self):
        """
        Toggle the state between Flagged and Default.
        Will not switch states if the cell is OPEN.
        """        
        if self.state == State.FLAGGED:
            self.state = State.DEFAULT
        elif self.state == State.DEFAULT:
            self.state = State.FLAGGED        
