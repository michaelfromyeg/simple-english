import { AnimatePresence, motion } from "framer-motion"
import { useState } from "react"

import "./style.css"

let tabs = [
  { id: "default", label: "Default" },
  { id: "talktohelp", label: "Talk2Help" }
]
function DefaultTabContent() {
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
        type="button"
        className="w-full inline-flex items-center px-10 py-2.5 text-sm font-medium text-center text-black bg-opacity-50 bg-sky-200 rounded-lg hover:bg-sky-400 focus:outline-none focus:ring-sky-300 dark:bg-sky-300 dark:hover:bg-sky-500 dark:focus:ring-sky-600 hover:bg-opacity-75 hover:backdrop-blur-md">
        Simplify Page
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

function AnimatedTabs() {
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
        {activeTab === "default" && <DefaultTabContent />}
        {activeTab === "talktohelp" && <TalkToHelpTabContent />}
      </motion.div>
    </div>
  )
}

export default function IndexPopup() {
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
          <AnimatedTabs />
        </div>
      </motion.div>
    </AnimatePresence>
  )
}
