export const BASE_URL =
  process.env.NODE_ENV === "development"
    ? "http://localhost:5000"
    : "https://plasmo.vercel.app"

// Send a request to simplify with current url - server responds with short summary
export const MOCK_SERVER_RESPONSE = `
    Europe is a continent located entirely in the Northern Hemisphere and mostly in the Eastern Hemisphere. It is bordered by the Arctic Ocean to the north, the Atlantic Ocean to the west, Asia to the east, and the Mediterranean Sea to the south.
    Europe is known for its rich history and diverse cultures. It is home to many famous landmarks such as the Eiffel Tower in Paris, the Colosseum in Rome, and the Acropolis in Athens.
    Some key phrases about Europe include <a class="key">continent</a>, <a class="key">diverse cultures</a>, and <a class="key">famous landmarks</a>.
`
export const COLORS = [
  "#6B97C7",
  "#A4C76B",
  "#E4D395",
  "#E7B1E5",
  "#B1CDE7",
  "#CF9BE7"
]

export enum StorageKey {
  // for whatever reason, using this enum is giving me problems
  BODY_CONTENT = "bodyContent",
  WINDOW_URL = "windowUrl",
  OPENAI_TOKEN = "openaiToken"
}
