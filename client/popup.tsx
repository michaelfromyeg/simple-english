import { useEffect, useState, type ReactElement } from "react"

import { sendToBackground } from "@plasmohq/messaging"

import "./styles/popup.css"

type PageState = "init" | "loading" | "done" | "error" | "unauthorized"

export default function Popup(): ReactElement {
  const [pageState, setPageState] = useState<PageState>("init")
  const [errorMessage, setErrorMessage] = useState<string>("")

  const pageStateToButtonText = (state: PageState): string => {
    switch (state) {
      case "init":
        return "Simplify"
      case "loading":
        return "Loading..."
      case "done":
        return "Done!"
      case "unauthorized":
      case "error":
        return "Error!"
      default:
        return "Simplify"
    }
  }

  const handleClick = async (): Promise<void> => {
    try {
      setPageState("loading")

      const response = await sendToBackground({
        name: "simplify"
      })

      if (response === "error" || response === "unauthorized") {
        setPageState(response)
      } else {
        setPageState("done")
      }
    } catch (error) {
      console.error(
        "An error occurred while trying to simplify the on-screen text!",
        error
      )
      setPageState("error")
    }
  }

  useEffect(() => {
    if (pageState === "unauthorized") {
      setErrorMessage("Your request was unauthorized. Check your OpenAI token!")
    } else {
      setErrorMessage("")
    }
  }, [pageState])

  return (
    <>
      <button
        onClick={handleClick}
        type="button"
        className={`button ${pageState}`}>
        {pageStateToButtonText(pageState)}
      </button>
      {errorMessage.length > 0 && (
        <p className={`error-message`}>{errorMessage}</p>
      )}
    </>
  )
}
