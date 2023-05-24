def modify_file(file_path):
    # Read the content of the file
    with open(file_path, 'r') as file:
        content = file.read()

    # Check the first three characters
    if content[1:3] == '][':
        # Remove the first occurrence of ']['
        modified_content = content.replace('][', '', 1)
    else:
        # Replace '}{' with '},{'
        modified_content = content.replace('}{', '},{')

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.write(modified_content)


# Usage
modify_file('testing.json')
