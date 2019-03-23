# importing os module
import os
import re


# Function to rename multiple files
def main():
    i = 0

    for file_name in os.listdir("."):
        print(file_name)
        new_name = re.sub(' ', '_', file_name)
        os.rename(file_name, new_name)

# Driver Code
if __name__ == '__main__':
    # Calling main() function
    main()