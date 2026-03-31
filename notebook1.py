import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    a = 1
    return (a,)


@app.cell
def _():
    b = 2
    return (b,)


@app.cell
def _(a, b):
    a+b
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
