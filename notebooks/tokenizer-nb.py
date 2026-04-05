import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
async def _():
    # Function to detect automatically if this is a webassembly notebook
    def is_webassembly_notebook():
        import sys
        return sys.platform == 'emscripten'

    # If it is a webassembly notebook install the package on the fly
    if is_webassembly_notebook():
        import micropip
        await micropip.install("transformers_js_py")
    return


@app.cell
def _():
    import random

    return (random,)


@app.cell
def _():
    from transformers_js_py import import_transformers_js

    return (import_transformers_js,)


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    model = mo.ui.dropdown(
        options=["Qwen/Qwen3-0.6B", "mistralai/Mistral-7B-Instruct-v0.3", "unsloth/gemma-3-270m-it", "Custom model"], value="Qwen/Qwen3-0.6B", label="Choose a model:"
    )
    model
    return (model,)


@app.cell
def _(mo, model):
    # Conditionally display a text input based on the dropdown's value
    text_input = mo.ui.text() if model.value == "Custom model" else None
    # Display the conditional input
    text_input
    return (text_input,)


@app.cell
async def _(import_transformers_js):
    transformers = await import_transformers_js()
    AutoTokenizer = transformers.AutoTokenizer
    return (AutoTokenizer,)


@app.cell
def _(mo):
    text = mo.ui.text_area(label="Input some text:", value="The dog eats the apples", debounce=False, placeholder="Type some text...")
    text
    return (text,)


@app.cell
async def _(AutoTokenizer, model, random, text, text_input):
    number_of_tokens = 0
    tokens_html = ""
    spans_1 = ""
    message = ""
    try:
        model_name = (
            text_input.value.strip()
            if model.value == "Custom model"
            else model.value
        )

        if not model_name:
            pass
        else:
            try:
                tokenizer = await AutoTokenizer.from_pretrained(model_name)
                message = ""
            except Exception as e:
                message = f'❌ {e}'
            encoded_tokens = tokenizer.encode(text.value)
            number_of_tokens = len(encoded_tokens)
            for i, token in enumerate(encoded_tokens):
                decoded_token = tokenizer.decode([token]).replace("<", "&lt;").replace(">", "&gt;")
                random.seed(token)
                random_color = ''.join([random.choice('0123456789ABCDEF') for k in range(6)])
                token_html = f'<span style="color: #{random_color};">{token}</span>'
                tokens_html += f" {token_html}"
                spans_1 += " " + f"""<span style="
                      padding: 5px;
                      border-right: 3px solid white;
                      line-height: 3em;
                      font-family: courier;
                      background-color: #{random_color};
                      color: white;
                      position: relative;
                    "><span style="position: absolute; top: 5ch; line-height: 1em; left: 0.5px; font-size: 0.45em">{token}</span>{decoded_token}</span>"""
    except:
        feedback = None
        pass
    return message, number_of_tokens, spans_1, tokens_html


@app.cell
def _(mo, tokens_html):
    mo.Html(tokens_html)
    return


@app.cell
def _(mo, spans_1):
    mo.Html(spans_1)
    return


@app.cell
def _(mo, number_of_tokens, text):
    mo.md(f"""
    Tokens: **{number_of_tokens}**

    Characters: **{len(text.value)}**
    """)
    return


@app.cell
def _(message, mo):
    mo.md(message)
    return


if __name__ == "__main__":
    app.run()

