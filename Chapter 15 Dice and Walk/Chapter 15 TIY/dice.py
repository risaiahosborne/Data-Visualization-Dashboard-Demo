from random import randint

class Dice:
    """A class representing a single die."""
    
    def __init__(self, num_sides = 6):
        """Six sided die."""
        self.num_sides = num_sides
        
    def roll(self):
        """Return a random value"""
        return randint(1, self.num_sides)
    
    def get_results(self, num_rolls = 1000):
        """Return a list of results from rolling the die."""
        results = []
        for roll_num in range(num_rolls):
            result = self.roll()
            results.append(result)
        return results
