import weaviate
from config import ConfigLoader
from constants.vectordb import RETRIEVAL_CONFIG_VECTORDB
from langchain.vectorstores.weaviate import Weaviate as LangChainWeaviate


class BaseVectordb(ConfigLoader):
    module_name = "VectorDB"
    config_key = "vectordb"

    def __init__(self, config: dict) -> None:
        """
        A wrapper around the weaviate-client and langchain's weaviate class

        Args:
            config: Pass the parsed config file into this class
        """
        super().__init__(name=self.module_name.title(), config=config)
        self.config = config
        self.parse_config(self.config_key, self.compulsory_fields)

    def create_client(self):
        raise NotImplementedError()

    def get_langchain_client(self):
        raise NotImplementedError()