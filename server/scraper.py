import requests as r

result = r.get("https://en.wikipedia.org/wiki/Stanley_Cup_Finals")

print(result)
print(result.text)

# copy result.text into a file called stanley_cup_finals.html
with open("data/stanley_cup_finals.html", "w") as f:
    f.write(result.text)
