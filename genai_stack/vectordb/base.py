from typing import Callable, Union
from pydantic import BaseModel

from genai_stack.stack.stack_component import StackComponent, StackComponentConfig


class BaseVectorDBConfigModel(BaseModel):
    """Base Data Model for VectorDB"""

    pass


class BaseVectorDBConfig(StackComponentConfig):
    """Base VectorDB Config Stack Component Config"""

    data_model = BaseVectorDBConfigModel


class BaseVectorDB(StackComponent):
    """Base VectorDB Stack Component"""

    config_class = BaseVectorDBConfig

    @property
    def client(self):
        raise NotImplementedError()

    @property
    def lc_client(self):
        raise NotImplementedError()

    def create_index(self, *args, **kwargs):
        raise NotImplementedError()

    def add_documents(self, documents):
        return self.lc_client.add_documents(documents)

    def search_method(self, query: str):
        search_methods = {
            "similarity_search": self.similarity_search,
            "max_marginal_relevance_search": self.mmr,
        }
        search_results = search_methods.get(self.config.search_method.value)(
            query=query
        )
        return search_results

    def similarity_search(self, query: str):
        """
        Return docs based on similarity search

        Args:
            query: Document or string against which you want to do the search
        """
        return self.lc_client.similarity_search(
            query=query,
            **self.config.search_options,
        )

    def mmr(self, query: str):
        """
        Return docs selected using the maximal marginal relevance.
        Maximal marginal relevance optimizes for similarity to query AND diversity
        among selected documents.

        Args:
            query: Document or string against which you want to do the search
        """
        return self.lc_client.max_marginal_relevance_search(
            query=query, **self.config.search_options
        )

    def search(self, query: str):
        return self.search_method(query)

    def get_collection(self, collection_name: str):
        """
        This method returns the vectordb collection.
        """
        raise NotImplementedError()

    def get_document(self, id: Union[str, int], **kwargs) -> Union[dict, None]:
        """
        This method returns a document that matches with the provided id.
        """
        raise NotImplementedError()

    def create_document(
        self, id: Union[str, int], document: Union[str, dict], **kwargs
    ) -> dict:
        """
        This method used to create a new document in vectordb.
        """
        raise NotImplementedError()

    def update_document(
        self, id: Union[str, int], document: Union[str, dict], **kwargs
    ) -> None:
        """
        This method used to update the existing document in vectordb.
        """
        raise NotImplementedError()
