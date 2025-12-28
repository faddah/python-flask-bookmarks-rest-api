"""Timer decorator module."""
import time
from datetime import datetime, timedelta


def timer_dec(base_fn):
    """Decorator that measures and prints function execution time."""

    def enhanced_fn(*args, **kwargs):
        """Enhanced function that times the decorated function."""
        start_time = time.time()
        result = base_fn(*args, **kwargs)
        end_time = time.time()
        print(f"Function '{base_fn.__name__}' executed in {end_time - start_time:.9f} seconds")
        return result

    return enhanced_fn

@timer_dec
def brew_tea(tea_type="Green", steep_time=1):
    """Function that simulates brewing tea."""
    print(f"Brewing {tea_type} tea...")
    time.sleep(steep_time)  # Simulate time taken to brew tea
    print("Tea is ready!")

@timer_dec
def brew_matcha():
    """Function that simulates brewing matcha."""
    print("Brewing matcha...")
    time.sleep(2)  # Simulate time taken to brew matcha
    print("Matcha is ready!")
    return f"Please drink your Matcha by {datetime.now() + timedelta(minutes=30)}."

brew_tea("Oolong", 1.25)
brew_tea(tea_type="Green", steep_time=1)
print(brew_matcha())
