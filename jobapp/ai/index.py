import faiss
import pickle
import numpy as np
from jobapp.models import Job
from jobapp.ai.embedding import get_embedding


INDEX_FILE = "jobapp/ai/jobs.index"

JOB_IDS_FILE = "jobapp/ai/job_ids.pkl"

def build_and_save_index():

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
        dtype="float32"
    )

    faiss.normalize_L2(
        embeddings
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(
        dimension
    )

    index.add(
        embeddings
    )

    faiss.write_index(
        index,
        INDEX_FILE
    )

    with open(
        JOB_IDS_FILE,
        "wb"
    ) as f:

        pickle.dump(
            job_ids,
            f
        )

def load_index():

    index = faiss.read_index(
        INDEX_FILE
    )

    with open(
        JOB_IDS_FILE,
        "rb"
    ) as f:

        job_ids = pickle.load(f)

    return index, job_ids