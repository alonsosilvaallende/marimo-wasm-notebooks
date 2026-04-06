import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    mo.md("# `subword-tooltip`")
    return (mo,)


@app.cell
def _(mo):
    mo.md("""
    Hover over the following phrase:
    """)
    return


@app.cell
def _(mo):
    import subword_tooltip

    list_of_words = ["This", " is", " an", " impor", "tant", " example"]
    w = mo.ui.anywidget(subword_tooltip.Widget(list_of_words=list_of_words))
    w
    return list_of_words, w


@app.cell
def _(list_of_words, mo, w):
    mo.md(f"hovered index: {w.hovered_index}\n\nhovered subword: '{list_of_words[w.hovered_index]}'").style({"color": "blue"})
    return


@app.cell
def _(mo):
    mo.md("""
    Installation:

    `pip install subword-tooltip`
    """)
    return


@app.cell
async def _():
    # Function to detect automatically if this is a webassembly notebook
    def is_webassembly_notebook():
        import sys
        return sys.platform == 'emscripten'

    # If it is a webassembly notebook install the package on the fly
    if is_webassembly_notebook():
        import micropip
        await micropip.install("subword-tooltip")
    return


if __name__ == "__main__":
    app.run()
