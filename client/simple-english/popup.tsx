import { AnimatePresence, motion } from "framer-motion"
import { useReducer, useState } from "react"

// import logo from "./assets/SimpleEnglish.svg"

import "./style.css"

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
          <h2 className="text-gray-900 font-bold text-xl mb-2">
            Let's break it down
          </h2>
          <input onChange={(e) => setData(e.target.value)} value={data} />
          <button
            onClick={() => increase()}
            type="button"
            className="inline-flex items-center px-5 py-2.5 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
            Simplify Page
          </button>
        </div>
      </motion.div>
      )
    </AnimatePresence>
  )
}

export default IndexPopup
