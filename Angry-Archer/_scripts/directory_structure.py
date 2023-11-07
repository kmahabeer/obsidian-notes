import os


# Function to create directories recursively
def create_directories(base_path, lines, index, parent_indentation):
    while index < len(lines):
        line = lines[index].rstrip()
        indentation = len(line) - len(line.lstrip())
        line = line.lstrip()

        if not line:
            return index

        if indentation > parent_indentation:
            # Create a sub-directory
            path = os.path.join(base_path, line)
            os.makedirs(path)
            index += 1
            index = create_directories(path, lines, index, indentation)
        else:
            # Move up one level
            return index


# Define the name of the plaintext file
structure_file = "directory_structure.txt"

# Get the directory of the script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Define the relative path to the target directory
relative_path = "../"  # Adjust as needed

# Combine the script directory and the relative path to get the target directory
target_directory = os.path.join(script_directory, relative_path)

# Read the structure from the plaintext file
with open(structure_file, "r") as file:
    lines = file.readlines()

# Change directory to the target directory
os.chdir(target_directory)

# Start creating directories from the root folder
create_directories(".", lines, 0, -1)

print("Directory structure created in", os.getcwd())
