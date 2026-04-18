import marimo

__generated_with = "0.22.4"
app = marimo.App(width="medium")


@app.cell
async def _():
    # Function to detect automatically if this is a webassembly notebook
    def is_webassembly_notebook():
        import sys
        return sys.platform == 'emscripten'

    # If it is a webassembly notebook install the packages on the fly
    if is_webassembly_notebook():
        import micropip
        await micropip.install("graphviz")
        await micropip.install("graphviznb")
    return


@app.cell
def _():
    import graphviz
    import graphviznb
    import marimo as mo

    return graphviz, graphviznb, mo


@app.cell
def _(mo):
    textA = mo.ui.text(value="Hello", debounce=False, label="Top: ")
    textA
    return (textA,)


@app.cell
def _(mo):
    textB = mo.ui.text(value="World", debounce=False, label="Bottom left: ")
    textB
    return (textB,)


@app.cell
def _(mo):
    textC = mo.ui.text(value="", debounce=False, label="Bottom right: ", placeholder="Enter your name...")
    textC
    return (textC,)


@app.cell
def _(graphviz, textA, textB, textC):
    graph = graphviz.Digraph()
    graph.edge(textA.value, textB.value)
    graph.edge(textA.value, textC.value)
    return (graph,)


@app.cell
def _(graph, graphviznb, mo):
    w = mo.ui.anywidget(graphviznb.Widget())
    w.source = graph.source
    w
    return


if __name__ == "__main__":
    app.run()
