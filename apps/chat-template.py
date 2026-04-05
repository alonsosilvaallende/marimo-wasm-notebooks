import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
async def _():
    import micropip

    await micropip.install("transformers_js_py")
    await micropip.install("openai")
    await micropip.install("pydantic")
    return


@app.cell
def _():
    import marimo as mo
    from openai import pydantic_function_tool

    return mo, pydantic_function_tool


@app.cell
def _(mo):
    mo.md("""
    # Chat is an abstraction
    """)
    return


@app.cell
def _(mo):
    model_id = mo.ui.dropdown(
        options=["Qwen/Qwen3-0.6B", "Qwen/Qwen2.5-0.5B-Instruct", "mistralai/Mistral-7B-Instruct-v0.3", "unsloth/gemma-3-270m-it", "Custom model"], value="Qwen/Qwen3-0.6B", label="Choose a model:"
    )
    return (model_id,)


@app.cell
def _(mo, model_id):
    # Conditionally display a text input based on the dropdown's value
    text_input = mo.ui.text() if model_id.value == "Custom model" else None
    # Display the conditional input
    text_input
    return (text_input,)


@app.cell
def _(model_id, text_input):
    model_name = (
        text_input.value.strip()
        if model_id.value == "Custom model"
        else model_id.value
    )
    return (model_name,)


@app.cell
def _():
    from transformers_js_py import import_transformers_js

    return (import_transformers_js,)


@app.cell
async def _(import_transformers_js):
    transformers = await import_transformers_js()
    AutoTokenizer = transformers.AutoTokenizer
    return (AutoTokenizer,)


@app.cell
async def _(AutoTokenizer, model_name):
    tokenizer = await AutoTokenizer.from_pretrained(model_name)
    return (tokenizer,)


@app.cell
def _(mo):
    system_message = mo.ui.text_area("You are a helpful assistant.", rows=1, debounce=False, label="System message:")
    return (system_message,)


@app.cell
def _(mo):
    user_message = mo.ui.text_area("Hi!", rows=2, debounce=False, label="User message:")
    return (user_message,)


@app.cell
def _(system_message, user_message):
    messages = []
    if system_message.value != "":
        messages.append({"role": "system", "content": system_message.value})
    if user_message.value != "":
        messages.append({"role": "user", "content": user_message.value})
    return (messages,)


@app.cell
def _(mo):
    add_generation_prompt = mo.ui.checkbox(label="Add generation prompt:")
    return (add_generation_prompt,)


@app.cell
def _(mo):
    multiselect = mo.ui.multiselect(
        options=["current_time", "multiply"], label="Provide some tools:"
    )
    return (multiselect,)


@app.cell
def _(multiselect, tool_current_time, tool_multiply):
    tools = []
    if "current_time" in multiselect.value:
        tools.append(tool_current_time)
    if "multiply" in multiselect.value:
        tools.append(tool_multiply)
    return (tools,)


@app.cell
def _():
    from pydantic import BaseModel, Field

    return BaseModel, Field


@app.cell
def _(BaseModel, Field):
    class multiply(BaseModel):
        """Multiply two integers together."""

        a: int = Field(..., description="First integer")
        b: int = Field(..., description="Second integer")

    return (multiply,)


@app.cell
def _(multiply, pydantic_function_tool):
    tool_multiply = pydantic_function_tool(multiply)
    return (tool_multiply,)


@app.cell
def _(BaseModel, Field):
    class current_time(BaseModel):
        """Get the current local time as a string."""
        time_now: str = Field(..., description="current local time")

    return (current_time,)


@app.cell
def _(current_time, pydantic_function_tool):
    tool_current_time = pydantic_function_tool(current_time)
    return (tool_current_time,)


@app.cell
def _(add_generation_prompt, messages, mo, tokenizer, tools):
    if messages != []:
        if tools != []:
            output2 = mo.Html(tokenizer.apply_chat_template(messages,
                                                          add_generation_prompt= add_generation_prompt.value,
                                                          tools=tools,
                                                          tokenize=False).replace("\n", "<br>").replace("#", "\#").replace("<s>", "<s\>"))
        else:
            output2 = mo.Html(tokenizer.apply_chat_template(messages,
                                                          add_generation_prompt= add_generation_prompt.value,
                                                          tokenize=False).replace("\n", "<br>").replace("#", "\#").replace("<s>", "<s\>"))
    else:
        output2 = ""
    return (output2,)


@app.cell
def _(
    add_generation_prompt,
    mo,
    model_id,
    multiselect,
    output2,
    system_message,
    user_message,
):
    mo.hstack([mo.vstack([model_id, system_message, user_message, add_generation_prompt, multiselect]), mo.vstack([mo.md("**What the LLM sees:**"), output2], align="start", justify="start")], gap=2, widths=[1,2])
    return


if __name__ == "__main__":
    app.run()
