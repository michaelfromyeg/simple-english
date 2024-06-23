import { AnimatePresence, motion } from "framer-motion"
import { useState } from "react"

import { sendToBackground } from "@plasmohq/messaging"

import "./style.css"

let tabs = [
  { id: "default", label: "Default" },
  { id: "talktohelp", label: "Talk2Help" }
]
function DefaultTabContent({
  setLoading
}: {
  setLoading: (loading: boolean) => void
}) {
  const [buttonText, setButtonText] = useState("Simplify Page")
  const handleClick = async () => {
    console.log("Simplify button clicked! Sending message to background.")
    setButtonText("Simplified!")
    await sendToBackground({
      name: "simplify"
    })
  }

  window.close()

  return (
    <motion.div
      exit={{
        y: -20,
        opacity: 0,
        filter: "blur(5px)",
        transition: { ease: "easeIn", duration: 0.22 }
      }}
      initial={{ opacity: 0, y: -15 }}
      animate={{
        opacity: 1,
        y: 0,
        filter: "blur(0px)",
        transition: { type: "spring", duration: 0.7 }
      }}>
      <button
        onClick={handleClick}
        type="button"
        className="w-full inline-flex items-center px-10 py-2.5 text-sm font-medium text-center text-black bg-opacity-50 bg-blue-700 rounded-lg hover:bg-blue-800 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800 hover:bg-opacity-75 hover:backdrop-blur-md">
        {buttonText}
      </button>
    </motion.div>
  )
}

function TalkToHelpTabContent() {
  return (
    <motion.div
      exit={{
        y: -20,
        opacity: 0,
        filter: "blur(5px)",
        transition: { ease: "easeIn", duration: 0.22 }
      }}
      initial={{ opacity: 0, y: -15 }}
      animate={{
        opacity: 1,
        y: 0,
        filter: "blur(0px)",
        transition: { type: "spring", duration: 0.7 }
      }}>
      <h1>Talk2Help Tab</h1>
      <p>This is the content for the Talk2Help tab.</p>
    </motion.div>
  )
}

function AnimatedTabs({
  setLoading
}: {
  setLoading: (loading: boolean) => void
}) {
  let [activeTab, setActiveTab] = useState(tabs[0].id)

  return (
    <div className="flex flex-col items-center justify-center p-1 ">
      <div>
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`${
              activeTab === tab.id ? "" : "hover:text-black/60"
            } relative rounded-full px-3 py-1.5 text-sm font-medium outline-sky-400 transition focus-visible:outline-2 ${activeTab === tab.id ? "text-white" : "text-gray-400 hover:text-gray-600"}`}
            style={{
              WebkitTapHighlightColor: "transparent"
            }}>
            {activeTab === tab.id && (
              <motion.span
                layoutId="bubble"
                className="absolute inset-0 z-10 bg-sky-100 mix-blend-difference"
                style={{ borderRadius: 9999 }}
                transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
              />
            )}
            {tab.label}
          </button>
        ))}
      </div>
      <motion.div className=" flex flex-col items-center justify-center pt-5 w-[275px]">
        {activeTab === "default" && (
          <DefaultTabContent setLoading={setLoading} />
        )}
        {activeTab === "talktohelp" && <TalkToHelpTabContent />}
      </motion.div>
    </div>
  )
}

export default function IndexPopup() {
  const [loading, setLoading] = useState(false)
  return (
    <AnimatePresence>
      <motion.div
        exit={{
          y: -20,
          opacity: 0,
          filter: "blur(5px)",
          transition: { ease: "easeIn", duration: 0.22 }
        }}
        initial={{ opacity: 0, y: -15 }}
        animate={{
          opacity: 1,
          y: 0,
          filter: "blur(0px)",
          transition: { type: "spring", duration: 0.7 }
        }}
        className="card flex flex-col items-center justify-center p-1 w-[275px]">
        <div
          className="flex flex-col items-center justify-center space-y-4"
          style={{
            padding: 16,
            width: 200,
            borderRadius: 8
          }}>
          <div className="logo text-base font-medium py-2">Simple English</div>
          {loading ? (
            <div className="flex flex-col items-center justify-center">
              <AnimatePresence>
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{
                    y: -20,
                    opacity: 0,
                    filter: "blur(5px)",
                    transition: { ease: "easeIn", duration: 0.22 }
                  }}
                  transition={{ duration: 0.5 }}>
                  <div className="loader"></div>
                  <motion.div
                    animate={{ opacity: [1, 0.5, 1] }}
                    transition={{
                      delay: 0.5,
                      duration: 1,
                      ease: "easeInOut",
                      repeat: Infinity,
                      repeatType: "mirror"
                    }}>
                    <p>Generating Simplification...</p>
                  </motion.div>
                </motion.div>
              </AnimatePresence>
            </div>
          ) : (
            <AnimatedTabs setLoading={setLoading} />
          )}
        </div>
      </motion.div>
    </AnimatePresence>
  )
}
