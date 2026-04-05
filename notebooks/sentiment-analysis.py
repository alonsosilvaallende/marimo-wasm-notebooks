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
async def _():
    import marimo as mo
    from transformers_js_py import import_transformers_js

    transformers = await import_transformers_js()
    pipeline = transformers.pipeline

    pipe = await pipeline('sentiment-analysis')
    return mo, pipe


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Sentiment Analysis
    """)
    return


@app.cell
def _(mo):
    text = mo.ui.text_area(label="Input some text:", value="I love transformers!", debounce=False, placeholder="Type some text...")
    text
    return (text,)


@app.cell
async def _(pipe, text):
    out = await pipe(f'{text.value}')
    return (out,)


@app.cell
def _(out):
    color = "green" if out[0]["label"] == "POSITIVE" else "red"
    return (color,)


@app.cell
def _(color, mo, out):
    mo.md(f"sentiment: {out[0]['label']}\n\nscore: {out[0]['score']}").style({"color": f"{color}"})
    return


if __name__ == "__main__":
    app.run()
