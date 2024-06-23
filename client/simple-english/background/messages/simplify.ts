import axios from "axios"

import type { PlasmoMessaging } from "@plasmohq/messaging"
import { Storage } from "@plasmohq/storage"

const storage = new Storage()

console.log("hello!")

const handler: PlasmoMessaging.MessageHandler = async (req, res) => {
  console.log("Simplify message received")
  await storage.setItem("simplified_content", "Loading...")
  const currentUrl = await storage.getItem("current_url")

  if (!currentUrl) {
    console.error("No current url found")
    return
  }

  const BASE_URL = await storage.getItem("endpoint_url")
  console.log("Current URL: ", currentUrl)
  const message = await axios.get(`${BASE_URL}/simplify?url=${currentUrl}`)

  if (message?.status !== 200 || !message?.data?.content) {
    console.error(`Failed to fetch; got status=${message?.status}`, {
      response: message
    })
    return
  }

  console.log("Simplified content: ", message.data.content)
  storage.setItem("simplified_content", message.data.content)
}

storage.watch({
  current_url: ({ newValue }) => {
    console.log("Current URL changed to: ", newValue)
  }
})

export default handler
