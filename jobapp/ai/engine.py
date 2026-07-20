from jobapp.ai.index import load_index
class SemanticSearchEngine:

    def __init__(self):

        self.index = None
        self.job_ids = None

    def load(self):

        if self.index is None:

            self.index, self.job_ids = load_index()
engine = SemanticSearchEngine()