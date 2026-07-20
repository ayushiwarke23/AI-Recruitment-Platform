import faiss
import numpy as np
from jobapp.models import Job
from jobapp.ai.embedding import get_embedding
from jobapp.ai.engine import engine

def build_index():

    jobs = Job.objects.filter(
        is_active=True
    )
    embeddings = []
    job_ids = []
    for job in jobs:

        text = f"""
        {job.title}
        {job.description}
        {job.skills_required}
        {job.location}
        """
        vector = get_embedding(text)
        embeddings.append(vector)
        job_ids.append(job.id)

    embeddings = np.array(
        embeddings,
        dtype="float32")
    
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    faiss.normalize_L2(embeddings)
    index.add(embeddings)

    return index, job_ids

def semantic_search(query, top_k=100):

    engine.load()

    query_embedding = get_embedding(query)

    query_embedding = np.array(
        [query_embedding],
        dtype="float32"
    )

    faiss.normalize_L2(
        query_embedding
    )

    scores, indices = engine.index.search(
        query_embedding,
        top_k
    )

    results = []

    for i, idx in enumerate(indices[0]):

        if idx == -1:
            continue

        results.append({
        "job_id": engine.job_ids[idx],
        "semantic_score": float(scores[0][i])})

    return results