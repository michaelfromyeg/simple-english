# Read the file
with open("data/response.html", "r") as file:
    content = file.read()

# Replace literal '\n' with actual newlines
content = content.replace("\\n", "\n")

# Write the modified content back to disk
with open("data/response.html", "w") as file:
    file.write(content)
