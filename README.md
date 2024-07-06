<p align="center">
    <img src="./client/assets/SimpleEnglish.svg" alt="Simple English">
</p>

# Simple English 🌐

Explore rabbit holes for text-based articles.

## About

Turn any Wikipedia page into Simple English. Expand interesting concepts further via telescopic text.

See a brief demo [here](https://youtube.com/watch?v=-xgwcf60wR8).

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

Want to help? See [CONTRIBUTING.md](./CONTRIBUTING.md).

## Usage

A guide to running the project on your local machine.

### Server

1. Run `bash scripts/setup.sh` to get setup for running the server.
2. Run `source env/bin/activate`.
3. Add your OpenAI API key in `.env`. Finally, run `make run-server`.

## Client

1. Install `pnpm` (e.g., `brew install pnpm`).
2. Then run `pnpm install` and `pnpm dev` to build the project.
3. Load the unpacked extension into Chrome the usual way (`chrome://extensions`).

Note that `plasmo` supports hot reloading the development version of the extension.
