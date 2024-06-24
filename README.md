<p style="text-align: center;">
    <img src="./client/assets/SimpleEnglish.svg" alt="Simple English">
</p>

# Simple English

Rabbit-holes for text-based articles.

## About

Turn any Wikipedia page into Simple English. Click into concepts via telescopic text.

TO-DOs...

- [ ] Improve Wikipedia article parsing
- [ ] Preserve more of the original article
- [ ] Use an existing simple translation, if available
- [ ] Add multipage view (i.e., side peek)
- [ ] Improve prompt for summary
- [ ] Improve prompt for in-text expansions
- [ ] Pre-load expansions
- [ ] Smarter caching in some sort of bucket
- [ ] Add "bring your own token" support
- [ ] Deploy the project

## Usage

Run `bash scripts/setup.sh` to get setup for running the server.

Run `source env/bin/activate`.

Add your OpenAI API key in `.env`. Finally, run `make run-server`.

For the client, install `pnpm` (e.g., `brew install pnpm`).

Then run `pnpm install` and `pnpm dev` to build the project.

Load the unpacked extension into Chrome the usual way (`chrome://extensions`).
