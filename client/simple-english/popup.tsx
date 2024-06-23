import { AnimatePresence, motion } from "framer-motion"
import { useReducer, useState } from "react"

import "./style.css"

let tabs = [
  { id: "default", label: "Default" },
  { id: "talktohelp", label: "Talk2Help" }
]

function AnimatedTabs() {
  let [activeTab, setActiveTab] = useState(tabs[0].id)

  return (
    <div className="flex space-x-1">
      {tabs.map((tab) => (
        <button
          key={tab.id}
          onClick={() => setActiveTab(tab.id)}
          className={`${
            activeTab === tab.id ? "" : "hover:text-black/60"
          } relative rounded-full px-3 py-1.5 text-sm font-medium text-white outline-sky-400 transition focus-visible:outline-2`}
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
  )
}

function IndexPopup() {
  const [data, setData] = useState("")
  const [count, increase] = useReducer((c) => c + 1, 0)

  return (
    <AnimatePresence>
      (
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
        className="card">
        <div
          style={{
            padding: 16
          }}>
          <AnimatedTabs />
          <h2 className="text-gray-900 font-bold text-xl mb-2">
            Let's break it down
          </h2>
          <input onChange={(e) => setData(e.target.value)} value={data} />
          <button
            onClick={() => increase()}
            type="button"
            className="inline-flex items-center px-5 py-2.5 text-sm font-medium text-center text-black bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
            Simplify Page
          </button>
        </div>
      </motion.div>
      )
    </AnimatePresence>
  )
}

export default IndexPopup
