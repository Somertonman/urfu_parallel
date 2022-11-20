from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from transformers import pipeline


class Sentence(BaseModel):
    min_score: Optional[float] = 0
    sentence: str
    n_of_results: Optional[int] = 5
    words_only: Optional[bool] = False


unmasker = pipeline("fill-mask", model="bert-base-uncased")

app = FastAPI()


@app.post("/get_suggestions")
async def root(request: Sentence):
    """String with * required to return list of completed strings with provided masked symbol."""

    min_score = request.min_score
    q = request.sentence
    n_of_results = request.n_of_results
    words_only = request.words_only

    # min_score check
    if min_score < 0 or min_score > 1:
        return {
            "status": "error",
            "details": "min_score should be a real number in [0,1)",
        }

    # n_of_results check
    if n_of_results < 1 or n_of_results > 5:
        return {
            "status": "error",
            "details": "n_of_results should be a real number in [1,5]",
        }

    # count of masked symbols check
    if q.count("*") == 0:
        return {"status": "error", "details": "Masked symbol * not found"}
    elif q.count("*") > 1:
        return {
            "status": "error",
            "details": f"Masked symbol * found {q.count('*')} times",
        }

    try:
        q = q.replace("*", "[MASK]")
        result = unmasker(q)[:n_of_results]
        result = [x for x in result if x["score"] >= min_score]

        if len(result) == 0:
            return {
                "status": "error",
                "details": "No results to return. Probably min_score is too high.",
            }

        if words_only:
            result = {"status": "ok", "data": [x["token_str"] for x in result]}
        else:
            result = {"status": "ok", "data": result}

        return result

    except Exception as e:
        return {"status": "error", "details": e.args}
