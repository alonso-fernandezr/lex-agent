from dataclasses import dataclass
from typing import Callable

from langchain_core.documents import Document

from eval.golden_set import GoldenQAItem
from eval.metrics import mean_reciprocal_rank, rank_of_correct_chunk, recall


@dataclass
class EvalResults:
    recall: float
    mrr: float
    ranks: list[int | None]


def run_retrieval_eval(
    golden_set: list[GoldenQAItem],
    retrieve_fn: Callable[[str], list[Document]],
) -> EvalResults:
    """Score retrieve_fn against golden_set, matching on exact page_content."""
    ranks = [
        rank_of_correct_chunk(
            [doc.page_content for doc in retrieve_fn(item.question)],
            item.chunk_text,
        )
        for item in golden_set
    ]
    return EvalResults(recall=recall(ranks), mrr=mean_reciprocal_rank(ranks), ranks=ranks)
