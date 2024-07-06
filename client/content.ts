import axios from "axios"
import type { PlasmoCSConfig } from "plasmo"

import { Storage } from "@plasmohq/storage"

import { BASE_URL, StorageKey } from "~constants"
import { chromeStorageSyncGet, getRandomColor } from "~helpers"

const storage = new Storage({
  copiedKeyList: ["shield-modulation"]
})

/**
 * Configuration for the content script.
 *
 * Only runs on Wikipedia pages, excluding simple.wikipedia.org.
 */
export const config: PlasmoCSConfig = {
  matches: ["*://*.wikipedia.org/wiki/*"],
  exclude_matches: ["*://simple.wikipedia.org/wiki/*"]
}

/**
 * Expand the selected keyword by sending a request to the server
 * and replacing the HTML content appropriately.
 */
export const expandKeyword = async (stream: boolean = false) => {
  try {
    const tokenObject = await chromeStorageSyncGet(StorageKey.OPENAI_TOKEN)
    const token = tokenObject[StorageKey.OPENAI_TOKEN]
    if (!token) {
      console.error("No OpenAI token found!")
      return
    }

    const keyword = document.querySelector<HTMLElement>("#selected")
    const surroundingText = keyword.closest("p").innerHTML

    keyword.onclick = () => {}

    const expandResponse = await axios.post(
      `${BASE_URL}/expand?token=${token}`,
      {
        content: surroundingText
      }
    )

    // Create a new span element to replace the <a> `selectedPhrase` element
    const spanElement = document.createElement("span")
    spanElement.innerHTML = expandResponse.data.content

    // Replace the <a> element with the new <span> element in the DOM
    keyword.parentNode.replaceChild(spanElement, keyword)

    // register new key words identified in the LLM response
    registerNewKeywords()
  } catch (error) {
    console.error("An error occurred while trying to expand the text", error)

    // reset the onclick handler if an error occurred
    const keyword = document.querySelector<HTMLElement>("#selected")
    keyword.onclick = () => {
      keyword.id = "selected"
      expandKeyword()
    }
  }
}

/**
 * Traverse all the key phrases in the content and register them for expansion
 * (with the appropriate onclick handler and CSS).
 */
const registerNewKeywords = () => {
  document.querySelectorAll(".key").forEach((phrase: HTMLElement) => {
    phrase.onclick = async () => {
      phrase.id = "selected"
      expandKeyword()
    }
    phrase.style.color = "black"

    // TODO(michaelfromyeg): instead of a random color, use progressively darker shades
    // (...representing the depths of the query)
    phrase.style.backgroundColor = getRandomColor()
  })
}

// watch for changes in the body content; update as necessary
storage.watch({
  bodyContent: ({ newValue }) => {
    console.log("Updating body content with new value!")

    const body = document.querySelector("#bodyContent")
    body.innerHTML = newValue

    registerNewKeywords()
  }
})

// TODO(michaelfromyeg): see if this can come as an argument from `sendToBackground` instead
const updateUrls = async () => {
  await storage.set(StorageKey.WINDOW_URL, window.location.href)
}

updateUrls()

console.log("Content script loaded!")
