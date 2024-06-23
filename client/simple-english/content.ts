import axios from 'axios';
import type { PlasmoCSConfig } from "plasmo";

export const config: PlasmoCSConfig = {
  matches: ["https://*.wikipedia.org/*"]
}

// Send a request to simplify with current url - server responds with short summary
const dummyServerResponse = `
    Europe is a continent located entirely in the Northern Hemisphere and mostly in the Eastern Hemisphere. It is bordered by the Arctic Ocean to the north, the Atlantic Ocean to the west, Asia to the east, and the Mediterranean Sea to the south.
    Europe is known for its rich history and diverse cultures. It is home to many famous landmarks such as the Eiffel Tower in Paris, the Colosseum in Rome, and the Acropolis in Athens.
    Some key phrases about Europe include <a class="key">continent</a>, <a class="key">diverse cultures</a>, and <a class="key">famous landmarks</a>.
`;

const fetchSimplifiedPage = async () => {
  try {
    // Request the initial / simplify version of article
    // `http://127.0.0.1:5000/simplify?url=${window.location.href}`
    document.querySelector('#bodyContent').innerHTML = "<br><br>Loading...";
    const simplifiedResponse = await axios.get(`http://127.0.0.1:5000/simplify?url=${window.location.href}`)


    // Replace the DOM with simplified version of the article
    document.querySelector('#bodyContent').innerHTML = simplifiedResponse.data.content;

    // Configure each key phrase/word to be clickable and styled
    document.querySelectorAll('.key').forEach((phrase: HTMLElement) => {
      phrase.onclick = async () => {
        phrase.style.fontWeight = "bold";
        phrase.id = "selected";
        fetchExpand();
      };
      phrase.style.color = "black";
      phrase.style.backgroundColor = "gray";
    });
  }
  catch (e) {
    console.error(e)
  }
}

const fetchExpand = async () => {
  try {
    // fetch the text content of the surrounding <p> tag that the key is in
    // const surroundingText = phrase.closest('p').innerHTML;
    // console.log(surroundingText);
    // const expandResponse = await axios.post('http://127.0.0.1:5000/expand', {
    //   content: document.querySelector('#bodyContent').innerHTML
    // })
    const expandResponse = await axios.get('http://127.0.0.1:5000/status')
    console.log("expand response: ", expandResponse)

    // Replace the DOM with expanded version of the article
    // TODO: pretty animations
    document.querySelector(`#selected`).innerHTML = expandResponse.data.status
    document.querySelector(`#selected`).id = ""
  }
  catch (e) {
    console.error(e)
  }
}

fetchSimplifiedPage()