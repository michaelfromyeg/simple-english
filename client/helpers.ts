import { COLORS } from "~constants"

export function getRandomColor(): string {
  return COLORS[Math.floor(Math.random() * COLORS.length)]
}

export const chromeStorageSyncGet = (key: string): Promise<any> => {
  return new Promise((resolve, reject) => {
    chrome.storage.sync.get(key, (result) => {
      if (chrome.runtime.lastError) {
        return reject(chrome.runtime.lastError)
      }
      resolve(result)
    })
  })
}

export const chromeStorageSyncSet = (items: object): Promise<void> => {
  return new Promise((resolve, reject) => {
    chrome.storage.sync.set(items, () => {
      if (chrome.runtime.lastError) {
        return reject(chrome.runtime.lastError)
      }
      resolve()
    })
  })
}
