curl -X POST \
    'localhost:5000/expand?url=https://en.wikipedia.org/wiki/Stanley_Cup_Finals' \
    -H 'Content-Type: application/json' \
    -d '{
        "sentence": "This is an example sentence.",
        "word": "example"
}'
