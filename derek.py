import os

#This helps avoid any directory issues.
os.chdir(os.path.dirname(os.path.abspath(__file__)))
print("Current working directory:", os.getcwd())

#This function takes in the .txt file. Has 3 outputs - starting x and y coordinates.
#Also reads in all the following directions. 
def read_route_file(filename):     
    
    try:
        with open(filename, 'r') as file:
            lines = file.read().splitlines() #Stores it in a list whilst getting rid of \n
            if len(lines) < 3: #If it doesn't have the first 3 values then we can't start.
                raise ValueError("File data may be corrupted; Please check file.")
            starting_x, starting_y = int(lines[0]), int(lines[1])
            directions = lines[2:] #List holds all the NESW directions
            return starting_x, starting_y, directions
    #try catch block catches file not found error fails loudly as do the invalid file format error.
    except FileNotFoundError:
        print("File not found")
        return None, None, None
    except ValueError:
        print("Invalid file format")
        return None, None, None


def plot_route(grid_size, starting_x, starting_y, directions):
    
    # Create the grid
    grid=[]
    i=0
    while i <grid_size:
        initial_row=[]
        j=0
        while j <grid_size:
            initial_row.append('.')
            j+=1
        grid.append(initial_row)
        i+=1
    

    # Adjust coordinates for 0-based indexing for row index python grid manipulation.
    x, y = starting_x - 1, grid_size - starting_y  # Flip `y` for plotting at the top
    #Stores the coordinates that we want to see and appends new results. 
    route_coordinates = []

    # Check if starting point is valid.
    if (x <0 or x >= grid_size or y<0 or y >= grid_size):
        print(f"Error: The starting point ({starting_x}, {starting_y}) is out of bounds")
        return -1, "Error: The starting point is outside of the grid"

    grid[y][x] = 'S'  # Mark the starting point. grid[select row][select column]
    route_coordinates.append((starting_x, starting_y))  # Store intial coordinates as 1-based coordinates

    for direction in directions:
        if direction == 'N': #Using the 0-based row index python grid. 
            y -= 1
        elif direction == 'S': #Using the 0-based row index python grid. 
            y += 1
        elif direction == 'E':
            x += 1
        elif direction == 'W':
            x -= 1
        else: #Loudly fail if letter is not in [N,S,E,W]
            return None, f"Error: Invalid direction '{direction}' in the route"

        # Check if the move is within bounds. This is in -based row index python grid system.
        if (x <0 or x >= grid_size or y<0 or y >= grid_size):
            print(f"Now it's out of bounds: ({x},{y})")
            return -1, "Error: The route is outside of the grid now"

        route_coordinates.append((x + 1, grid_size - y))  # Convert back to 1-based coordinates that the user wants to see.
        grid[y][x] = '*'  # Mark the charted path in the internal grid.

    # Mark the finishing point
    grid[y][x] = 'E'

    return grid, route_coordinates


#Function displays the grid. 
def display_grid(grid):
    for row in grid:
        print(' '.join(row))


def main():
    grid_size = 12

    while True:
        filename = input("Enter the next route instructions file (or enter STOP to end): ")
        if filename.upper() == "STOP":
            break

        starting_x, starting_y, directions = read_route_file(filename)
        if starting_x is None:
            continue
        if starting_y is None:
            continue
        if directions is None:
            continue

        grid, result = plot_route(grid_size, starting_x, starting_y, directions)

        if grid is None: #If invalid direction is triggered the current route till now is printed.
            print(result)
        if grid == -1: #Out of bounds then break
            break

        else:
            print("Plot the route:")
            display_grid(grid)
            print("PLot the Coordinates:")
            print(result)


if __name__ == "__main__":
    main()
