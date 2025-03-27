class Config():
    model_name: str
    chroma_collection_name: str
    chroma_search_type: str

    def __init__(self, model_name="granite3.2:2b", chroma_collection_name="rag-chroma"):
        self.model_name = model_name
        self.chroma_collection_name = chroma_collection_name
