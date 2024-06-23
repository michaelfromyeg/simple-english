import axios from "axios"
import type { PlasmoCSConfig } from "plasmo"

const BASE_URL = "http://127.0.0.1:5000"

// Send a request to simplify with current url - server responds with short summary
const MOCK_SERVER_RESPONSE = `
    Europe is a continent located entirely in the Northern Hemisphere and mostly in the Eastern Hemisphere. It is bordered by the Arctic Ocean to the north, the Atlantic Ocean to the west, Asia to the east, and the Mediterranean Sea to the south.
    Europe is known for its rich history and diverse cultures. It is home to many famous landmarks such as the Eiffel Tower in Paris, the Colosseum in Rome, and the Acropolis in Athens.
    Some key phrases about Europe include <a class="key">continent</a>, <a class="key">diverse cultures</a>, and <a class="key">famous landmarks</a>.
`

const colors = [
  "#6B97C7",
  "#A4C76B",
  "#E4D395",
  "#E7B1E5",
  "#B1CDE7",
  "#CF9BE7"
]

function getRandomColor() {
  return colors[Math.floor(Math.random() * colors.length)]
}

export const config: PlasmoCSConfig = {
  matches: ["https://*.wikipedia.org/*"]
}

export const fetchSimplifiedPage = async (stream: boolean = false) => {
  try {
    const body = document.querySelector("#bodyContent")
    // const body = document.querySelector("#mw-content-text")

    if (!body) {
      console.error("Couldn't find body element")
      return
    }

    body.innerHTML = "<br><br>Loading..."
    const response = await axios.get(
      `${BASE_URL}/simplify?url=${window.location.href}`
    )
    if (response?.status !== 200 || !response?.data?.content) {
      console.error(`Failed to fetch; got status=${response?.status}`, {
        response: response
      })
      return
    }

    if (stream) {
      // TODO(michaelfromyeg): naively stream `response.data.content` by rendering some tokens at a time
      const content = response.data.content
      const tokens = content.split(" ") // or use another delimiter if needed
      body.innerHTML = "" // Clear the loading message

      let index = 0
      const interval = setInterval(() => {
        if (index < tokens.length) {
          body.innerHTML += tokens[index] + " "
          index++
        } else {
          clearInterval(interval)
          document.querySelectorAll(".key").forEach((phrase: HTMLElement) => {
            phrase.onclick = async () => {
              phrase.id = "selected"
              fetchExpand()
            }
            phrase.style.color = "black"
            phrase.style.backgroundColor = getRandomColor()
          })
        }
      }, 100) // Adjust the interval delay as needed
    } else {
      body.innerHTML = response.data.content

      document.querySelectorAll(".key").forEach((phrase: HTMLElement) => {
        phrase.onclick = async () => {
          phrase.id = "selected"
          fetchExpand()
        }
        phrase.style.color = "black"
        phrase.style.backgroundColor = getRandomColor()
      })
    }
  } catch (error) {
    console.error(error)
  }
}

export const fetchExpand = async (stream: boolean = false) => {
  try {
    // fetch the text content of the surrounding <p> tag that the key is in
    const key_phrase = document.querySelector("#selected")
    const surroundingText = key_phrase.closest("p").innerHTML

    const expandResponse = await axios.post(`${BASE_URL}/expand`, {
      content: surroundingText
    })

    console.log("expand response: ", expandResponse.data)

    // Replace the DOM with expanded version of the article
    // TODO: pretty animations
    document.querySelector(`#selected`).innerHTML = expandResponse.data.content
    document.querySelector(`#selected`).id = ""
  } catch (error) {
    console.error(error)
  }
}

fetchSimplifiedPage(true)
