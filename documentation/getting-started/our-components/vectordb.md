# 🔮 VectorDB

The vector database is a new type of database that is becoming popular in the world of ML and AI. Vector databases are different from traditional relational databases, like PostgreSQL, which was originally designed to store tabular data in rows and columns. They’re also decidedly different from newer NoSQL databases, such as MongoDB, which store data in JSON documents.

Utilizing the Vector database offers significant advantages, simplifying the process of performing similarity searches in Word embeddings. Within the VectorDB, there exists a key method known as search. This function takes a string, which typically represents a prompt from the user, and leverages vector similarity search techniques to retrieve relevant data from the database.

```py
class BaseVectordb(ConfigLoader):
    module_name = "VectorDB"
    config_key = VECTORDB_CONFIG_KEY

    def __init__(self, config: dict) -> None:
        """
        A wrapper around the weaviate-client and langchain's weaviate class

        Args:
            config: Pass the parsed config file into this class
        """
        super().__init__(name=self.module_name, config=config)
        self.parse_config(self.config_key, self.required_fields)

    def search(self, query: str) -> List[Document]:
        raise NotImplementedError()
```

In our approach, VectorDB serves a dual purpose. Firstly, it facilitates efficient similarity searches, allowing us to find data points with embeddings that closely match the provided input. This functionality is crucial for tasks such as semantic similarity, recommendation systems, and clustering.

Secondly, the VectorDB acts as a reliable memory storage system. It securely stores the vectorized data, to store the chat history.

```py
def _setup_vectordb_memory(self, client: weaviate.Client):
    """
    Get or Create a vectordb index
    """
    try:
        client.schema.get(class_name=MEMORY_INDEX_NAME)
    except UnexpectedStatusCodeException:
        print("Creating memory index class in vector db")
        client.schema.create_class(
        {
            "class": MEMORY_INDEX_NAME,
            "properties": [
                {"name": MEMORY_TEXT_KEY, "dataType": ["text"]},
            ],
        }
    )
```

Currently LLM Stack supports only Weaviate for the Vector Database. In the coming few days, we will also integrate ChromaDB, Milvus and Qdrant.

## Pros of Weaviate:

* Open source & Easily self-hostable
* Relatively good performance
* Unlike the other options, it has modules which can be installed to automatically compute the embeddings from raw objects. - - - Which positions it as a more convenient all-in-one solution

Once the similarity search is performed within the VectorDB, the retrieved data is passed on to the Retrieval class. The Retrieval class is responsible for further processing and presenting the results to the user.