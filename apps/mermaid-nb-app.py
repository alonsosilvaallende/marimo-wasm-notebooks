import marimo

__generated_with = "0.22.4"
app = marimo.App(width="medium")


@app.cell
async def _():
    import micropip

    await micropip.install("mermaid-nb")
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    from mermaid_nb import Mermaid

    return (Mermaid,)


@app.cell
def _(mo):
    textA = mo.ui.text(value="Hello", debounce=False, label="Top: ")
    textA
    return (textA,)


@app.cell
def _(mo):
    textB = mo.ui.text(value="World", debounce=False, label="Bottom left: ")
    textC = mo.ui.text(value="Name", debounce=False, label="Bottom right: ", placeholder="Enter your name...")
    return textB, textC


@app.cell
def _(mo, textB, textC):
    mo.hstack([textB, textC], gap=2, widths=[1,2])
    return


@app.cell
def _(textA, textB, textC):
    textA_processed = (textA.value).replace(' ', '')
    textB_processed = (textB.value).replace(' ', '')
    textC_processed = (textC.value).replace(' ', '')
    return textA_processed, textB_processed, textC_processed


@app.cell
def _(textA, textA_processed, textB, textB_processed, textC, textC_processed):
    full_text = f"""flowchart TD\n  {textA_processed} --> {textB_processed}\n  {textA_processed} --> {textC_processed}""" if (textA.value != "" and textB.value != "" and textC.value != "") else "flowchart TD\n Missing --> Text"
    return (full_text,)


@app.cell
def _(mo):
    look_dropdown = mo.ui.dropdown(
        options=["classic", "handDrawn"], value="handDrawn", label="choose look:"
    )
    return (look_dropdown,)


@app.cell
def _(mo):
    theme_dropdown = mo.ui.dropdown(
        options=["default", "neutral", "dark", "forest", "base"], value="forest", label="choose theme:"
    )
    return (theme_dropdown,)


@app.cell
def _(look_dropdown, mo, theme_dropdown):
    mo.hstack([look_dropdown, theme_dropdown], gap=2, widths=[1,2])
    return


@app.cell
def _(Mermaid, full_text, look_dropdown, theme_dropdown):
    mo.ui.anywidget(Mermaid(diagram=f"{full_text}", theme=theme_dropdown.value, look=look_dropdown.value))
    return


if __name__ == "__main__":
    app.run()
