#!/bin/bash

# from: https://community.openai.com/t/delete-assistants-via-api-or-mass-delete-in-front-end/517979/4
API_KEY="..."

# Initialize list length to 100 to start the loop
listlen=100

# Continue looping while list length is greater than or equal to 100
while [ $listlen -ge 100 ]; do
    echo "Listing all assistants..."

    # Fetch the list of assistants (maximum 100 at a time)
    assistants=$(curl -s -H "Authorization: Bearer $API_KEY" \
        -H "Content-Type: application/json" \
        -H "OpenAI-Beta: assistants=v1" \
        "https://api.openai.com/v1/assistants?limit=100")

    # Extract IDs of all assistants
    ids=$(echo "$assistants" | jq -r '.data[].id')

    # Determine the number of assistants returned
    listlen=$(echo "$ids" | wc -l)

    # If no assistants are found, exit the loop
    if [ -z "$ids" ]; then
        echo "No assistants to delete."
        break
    fi

    # Loop through each assistant ID and delete it
    for id in $ids; do
        echo "Deleting assistant with ID: $id"
        delete_response=$(curl -s -X DELETE -H "Authorization: Bearer $API_KEY" \
            -H "Content-Type: application/json" \
            -H "OpenAI-Beta: assistants=v1" \
        "https://api.openai.com/v1/assistants/$id")
        echo $delete_response
    done
done

echo "All assistants have been deleted."

unset API_KEY
