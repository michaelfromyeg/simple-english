# Server

Extra documentation related to the server.

## Assistants

The old way of doing the OpenAI stuff was using assistants. It worked fairly well, but doesn't generalize to a "bring-your-own-token" use-case, so I want to preserve the code here for reference.

```python
from openai import AssistantEventHandler, OpenAI

client = OpenAI(api_key=token)

# NOTE: this creates an assistant programatically; maybe there's a way to just 'update' one
# ...use it sparingly
assistant = client.beta.assistants.create(
    name="Simple English Wikipedia Assistant",
    instructions="""Your
very
cool
multi-line
prompt.""",
    tools=[],
    model="gpt-4o",
)

# to re-use the same assistants
# ASSISTANT_ID = "asst_asdf"
# EXPAND_ASSISTANT_ID = "asst_qwerty"

# in the endpoint, to do the actual task
thread = client.beta.threads.create()
client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=html_content,
)

run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    # presuming we're reusing the same assistant
    assistant_id=ASSISTANT_ID,
)
print(f"Run for {url} completed with status: {run.status}")

content = ""
if run.status == "completed":
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    for message in messages:
        assert message.content[0].type == "text"
        if message.role == "assistant":
            content += message.content[0].text.value

# do something with it!
print(content)
```

The new way uses the chat completion API, with `gpt-3.5-turbo`. For money reasons!

## Streaming

Another big milestone will be streaming the summary.

To do this, you make a class for the assistant.

```python
class EventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text) -> None:
        print("", end="")

    @override
    def on_text_delta(self, delta, snapshot) -> None:
        print(delta.value, end="")

    @override
    def on_end(self) -> None:
        print("", end="", flush=True)
```

I still need to figure out how to do it with chat completions, _and_ how to handle that on the front-end.
