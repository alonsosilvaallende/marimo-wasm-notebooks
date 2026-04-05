import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
async def _():
    import micropip
    await micropip.install("transformers_js_py")
    return


@app.cell
def _():
    import marimo as mo
    import numpy as np
    from transformers_js_py import import_transformers_js

    return import_transformers_js, mo, np


@app.cell
async def _(import_transformers_js):
    transformers = await import_transformers_js()
    return (transformers,)


@app.cell
def _(transformers):
    Tensor = transformers.Tensor
    return (Tensor,)


@app.cell
def _(Tensor, np):
    def tensor_from_list(lst, dtype="int64"):
        arr = np.array(lst, dtype=np.int64)
        dims = list(arr.shape)
        flat = arr.flatten()
        return Tensor(dtype, flat, dims)

    return (tensor_from_list,)


@app.cell
def _():
    model_id = "onnx-community/Qwen2.5-0.5B-Instruct-ONNX"
    return (model_id,)


@app.cell
async def _(model_id, transformers):
    AutoTokenizer = transformers.AutoTokenizer
    tokenizer = await AutoTokenizer.from_pretrained(model_id)

    AutoModelForCausalLM = transformers.AutoModelForCausalLM
    model = await AutoModelForCausalLM.from_pretrained(model_id)
    return model, tokenizer


@app.cell
def _(mo):
    mo.md("""
    # Token importance
    """)
    return


@app.cell
def _(mo):
    text = mo.ui.text_area(label="Input some text:", value="Question: What is the capital of France\nAnswer: The capital of France is", debounce=True, placeholder="Type some text...")
    text
    return (text,)


@app.cell
def _(text, tokenizer):
    inputs = tokenizer(text.value)
    return (inputs,)


@app.cell
def _(inputs):
    input_ids = inputs["input_ids"].tolist()
    return (input_ids,)


@app.cell
def _(input_ids):
    ids = input_ids[0]
    return (ids,)


@app.cell
def _(ids, tokenizer):
    lst = [ids] + [[tokenizer.pad_token_id] + ids[:i] + ids[i+1:] for i in range(len(ids))]
    attention_mask = [[1] * len(ids)] + [[0] + [1] * (len(ids) - 1) for _ in range(len(ids))]
    return attention_mask, lst


@app.cell
async def _(attention_mask, lst, model, tensor_from_list):
    output = await model(input_ids = tensor_from_list(lst), attention_mask = tensor_from_list(attention_mask))
    return (output,)


@app.cell
def _(output):
    output_logits_lst = output["logits"].tolist()
    return (output_logits_lst,)


@app.cell
def _(output_logits_lst):
    last_logits = output_logits_lst[0][-1]
    return (last_logits,)


@app.cell
def _():
    from scipy.special import softmax

    return (softmax,)


@app.cell
def _(last_logits, softmax):
    probs = softmax(last_logits)
    return (probs,)


@app.cell
def _(np, probs):
    selected_token = np.argmax(probs).item()
    return (selected_token,)


@app.cell
def _(probs, selected_token):
    base_prob = probs[selected_token].item()
    return (base_prob,)


@app.cell
def _(base_prob, mo, selected_token, tokenizer):
    mo.Html(f'next token prediction: <span style="color: blue;">{tokenizer.decode([selected_token])}</span><br>next token probability: {base_prob:.3f}')
    return


@app.function
def score_to_color(score: float) -> tuple[int, int, int]:
    """Map score in [-1, 1] to (R, G, B) with red=-1, white=0, blue=1."""
    score = max(-1.0, min(1.0, score))  # clamp

    if score < 0:
        # white (255,255,255) → blue (0,0,255)
        t = score + 1          # 0..1
        r, g, b = int(255 * t), int(255 * t), 255
    else:
        # red (255,0,0) → white (255,255,255)
        t = score              # 0..1
        r, g, b = 255, int(255 * (1 - t)), int(255 * (1 - t))

    return r, g, b


@app.function
def score_to_hex(score: float) -> str:
    r, g, b = score_to_color(score)
    return f"#{r:02x}{g:02x}{b:02x}"


@app.cell
def _(base_prob, ids, output_logits_lst, selected_token, softmax, tokenizer):
    alo = []
    tokens_html = ""
    for k in range(len(output_logits_lst)-1):
        token = tokenizer.decode([ids[k]])
        last_logits_loop = output_logits_lst[k+1][-1]
        probs_loop = softmax(last_logits_loop)
        alo.append({"token": token, "score": f"{-(probs_loop[selected_token].item()-base_prob):.3f}"})
        color = score_to_hex(probs_loop[selected_token].item() - base_prob)
        if '\n' in token:
            token = token.replace("\n", "<br>")
        token_html = f'<span style="background-color: {color};">{token}</span>'
        tokens_html += token_html
    return alo, tokens_html


@app.cell
def _(mo):
    mo.md("""
    ## Token importance (leave-one-out)
    """)
    return


@app.cell
def _(mo, tokens_html):
    mo.Html(tokens_html)
    return


@app.cell
def _(alo, mo):
    mo.ui.table(data=alo, pagination=False, selection=None)
    return


if __name__ == "__main__":
    app.run()
