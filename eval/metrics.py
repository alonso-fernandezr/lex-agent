def rank_of_correct_chunk(retrieved_chunk_ids: list[str], correct_chunk_id: str) -> int | None:
    """1-indexed position of correct_chunk_id in retrieved_chunk_ids, or None if absent."""
    if correct_chunk_id not in retrieved_chunk_ids:
        return None
    return retrieved_chunk_ids.index(correct_chunk_id) + 1


def recall(ranks: list[int | None]) -> float:
    """Fraction of ranks that are not None."""
    if not ranks:
        raise ValueError("ranks must not be empty")
    return sum(1 for r in ranks if r is not None) / len(ranks)


def mean_reciprocal_rank(ranks: list[int | None]) -> float:
    """Average of 1/rank across ranks, treating None as 0."""
    if not ranks:
        raise ValueError("ranks must not be empty")
    return sum(1 / r if r is not None else 0 for r in ranks) / len(ranks)
