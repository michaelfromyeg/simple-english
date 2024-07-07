import axios from "axios"

import type { PlasmoMessaging } from "@plasmohq/messaging"
import { Storage } from "@plasmohq/storage"

import { BASE_URL, StorageKey } from "~constants"
import { chromeStorageSyncGet } from "~helpers"

const storage = new Storage({
  copiedKeyList: ["shield-modulation"]
})

const handler: PlasmoMessaging.MessageHandler = async (request, response) => {
  const tokenObject = await chromeStorageSyncGet(StorageKey.OPENAI_TOKEN)
  const token = tokenObject[StorageKey.OPENAI_TOKEN]
  if (!token) {
    console.error("No OpenAI token found!")

    response.send("error")
    return
  }

  const windowUrl = await storage.getItem(StorageKey.WINDOW_URL)
  if (!windowUrl) {
    console.error("No window URL found!")

    response.send("error")
    return
  }

  // TODO(michaelfromyeg): how to make axios not throw errors on non-200 status codes?
  try {
    const message = await axios.get(
      `${BASE_URL}/simplify?url=${windowUrl}&token=${token}`
    )
    if (message?.status !== 200 || !message?.data?.content) {
      console.error(`Failed to fetch; got status=${message?.status}`, {
        response: message
      })

      response.send("error")
      return
    }

    // for some reason, putting the enum value here makes things break
    // ...I need to investigate
    console.log("Setting body content...")
    await storage.setItem("bodyContent", message.data.content)

    response.send("ok")
  } catch (error) {
    console.error(
      "An error occurred while trying to simplify the on-screen text!",
      error
    )

    if (error?.response?.status === 401) {
      console.log("sending unauthorized...")
      response.send("unauthorized")
    } else {
      response.send("error")
    }
  }
}

export default handler
