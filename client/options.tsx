import { useEffect, useState, type ReactElement } from "react"

import { StorageKey } from "~constants"

import "./styles/options.css"

export default function Options(): ReactElement {
  const [token, setToken] = useState<string>("")

  useEffect(() => {
    // Retrieve the token from chrome storage on component mount
    chrome.storage.sync.get(StorageKey.OPENAI_TOKEN, (data) => {
      if (data[StorageKey.OPENAI_TOKEN]) {
        setToken(data[StorageKey.OPENAI_TOKEN])
      }
    })
  }, [])

  const saveToken = (): void => {
    chrome.storage.sync.set({ [StorageKey.OPENAI_TOKEN]: token }, () => {
      console.log("Token saved")
      alert("Token saved!")
    })
  }

  return (
    <div className="container">
      <h1 className="title">Simple English</h1>
      <p className="paragraph">
        Enter your OpenAI token here. No information is stored on our servers.
      </p>
      <p className="paragraph">
        Want to check for yourself? View the repository{" "}
        <a
          href="https://github.com/michaelfromyeg/simple-english"
          className="link">
          here
        </a>
        .
      </p>
      <input
        type="text"
        value={token}
        onChange={(e) => setToken(e.target.value)}
        placeholder="Enter your token here"
        className="input"
      />
      <button onClick={saveToken} className="button">
        Save
      </button>
    </div>
  )
}
