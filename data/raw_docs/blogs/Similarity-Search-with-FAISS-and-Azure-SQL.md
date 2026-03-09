# Similarity Search with FAISS and Azure SQL

Author: Muazma Zahid
Source: https://devblogs.microsoft.com/azure-sql/faiss-and-azure-sql/
Retrieved on: March 2026  

---

In today’s data-driven world, finding similar items within large datasets is a common challenge. Whether it’s recommending products, identifying similar documents, or clustering data points, efficient similarity search is crucial. This blog post will explore how to leverage FAISS (Facebook AI Similarity Search) and Azure SQL to perform similarity searches on Wikipedia movie plots data. The blog will also cover sample code to help you get started. Check out [Data exposed video](https://youtu.be/FrR3jZE9z8Y) for quick overview and follow along with the code sample.

What is Faiss​?
[FAISS](https://github.com/facebookresearch/faiss) (Facebook AI Similarity Search) is a library that allows developers to quickly search for embeddings of multimedia documents that are similar to each other. It solves limitations of traditional query search engines that are optimized for hash-based searches and provides more scalable similarity search functions.​

FAISS was developed by Facebook AI Research (FAIR) and was first released as an open-source project in February 2017​

​Learn More:

https://github.com/facebookresearch/faiss
https://github.com/facebookresearch/faiss/wiki
Faiss is a library for efficient similarity search and clustering of dense vectors. It supports various algorithms for searching in sets of vectors. Faiss can handle data sizes that do not fit in RAM. It provides complete Python/numpy wrappers and GPU implementations. The library is written in C++ with a focus on performance and scalability.

Supported Indexes​
FAISS supports various indexes: https://github.com/facebookresearch/faiss/wiki/Faiss-indexes for efficient similarity search and clustering of dense vectors. Let’s explore some of the key index types:​

Flat Indexes:​

These indexes encode vectors into fixed-size codes and store them in an array.​

They are simple baselines and do not store vector IDs.​

Examples:​

IndexFlatL2 (“Flat”): Performs exact search based on Euclidean distance (L2 norm).​
IndexFlatIP (“Flat”): Compares vectors using the inner product (dot product) similarity.​
IndexScalarQuantizer (“SQ8”): Quantizes vectors to 8-bit integers.​
IndexPQ (“PQx”): Splits vectors into sub-vectors and quantizes them (usually to 8 bits).​
Hierarchical Navigable Small World (HNSW):​

IndexHNSWFlat (“HNSW,Flat”): Uses a graph exploration approach for fast search.​
Supports scalar quantization and product quantization.​
Inverted File Indexes:​

These indexes assign vectors to inverted lists and perform search efficiently.​

Examples:​

IndexIVFFlat (“IVFx,Flat”): Uses another index to assign vectors to inverted lists.​
IndexIVFScalarQuantizer (“IVFx,SQ4” or “IVFx,SQ8”): Combines scalar quantization with inverted file structure.​
IndexIVFPQ (“IVFx,PQy”): Uses product quantization on residuals.​
GPU Acceleration:​

Some indexes are implemented on the GPU for faster execution.​

Examples:​

GpuIndexIVFFlat: GPU version of IndexIVFFlat.​
GpuIndexIVFPQ: GPU version of IndexIVFPQ.​
Other Indexes:​

IndexLSH: Locality-Sensitive Hashing (binary flat index).​
IndexIVFPQR: Similar to IndexIVFPQ, with re-ranking based on codes.
Choosing the right index depends on your specific requirements, such as the size of your dataset and the desired trade-off between speed and accuracy.​

​FAISS with SQL Database
Using Movie Plots in Azure SQL Database
For this example, we’ll use Wikipedia movie plots dataset containing [Wikipedia movie plots](https://www.kaggle.com/datasets/jrobischon/wikipedia-movie-plots) data stored in Azure SQL. We’ll encode these movie plots into dense vectors using a pre-trained model and then create a FAISS index to perform similarity searches.

SELECT * FROM [dbo].[movie_plots];
Here is the what the data looks like:
[Image omitted: Diagram explaining Data 5]
Sample Code
I have split the sample notebooks into two separate parts. The first notebook, which focuses on creating the FAISS Index, can be found [here](https://github.com/Azure-Samples/SQL-AI-samples/blob/main/AzureSQLFaiss/Azure%20SQL_and_Faiss_Index_Creation.ipynb). The second notebook, which covers Similarity Search on the created index, is available [here](https://github.com/Azure-Samples/SQL-AI-samples/blob/main/AzureSQLFaiss/Faiss_inference.ipynb). This separation is due to the varying frequency of index creation, which depends on how often your data is updated. You can also consider the trade-off between the total cost of maintaining indexes and the accuracy of the results to decide how often to update the index.

[Note: These notebooks are designed to run in Microsoft Fabric with PySpark. You can adjust the Python code to suit other notebook environments].

Create FAISS Index ([Sample Code](https://github.com/Azure-Samples/SQL-AI-samples/blob/main/AzureSQLFaiss/Azure%20SQL_and_Faiss_Index_Creation.ipynb))
Here’s a step-by-step guide to creating a FAISS index and performing similarity searches running on Microsoft Fabric (PySpark).

First, we will have to load data and choose model.

[Image omitted: Data 8]

The all-MiniLM-L6-v2 model from SentenceTransformers is a compact and efficient transformer model designed for generating high-quality sentence embeddings. It balances performance and speed, making it ideal for tasks like semantic search and clustering. This model is particularly useful for applications where computational resources are limited but high-quality embeddings are still required.

Next, we will create FAISS Index. See sample code here.

[Image omitted: Data 9]

The IndexFlatIP in FAISS (Facebook AI Similarity Search) is a simple and efficient index for performing inner product (dot product) similarity searches. It stores all vectors in a flat array and computes the inner product between the query vector and all stored vectors to find the most similar ones.

When to use IndexFlatIP?
High Accuracy: It provides exact nearest neighbor search results, making it suitable for applications where accuracy is critical.
Small to Medium Datasets: Best used for datasets that fit into memory, as it performs a linear scan over all vectors.
Similarity Search: Ideal for tasks like semantic search, recommendation systems, and clustering where inner product similarity is relevant.
Performing Similarity Search ([Sample Code](https://github.com/Azure-Samples/SQL-AI-samples/blob/main/AzureSQLFaiss/Faiss_inference.ipynb))
To perform a similarity search, we’ll define a function that encodes the input query, searches the FAISS index, and retrieves the top results. See sample code:

[Image omitted: Data 7]

Query and Result
[Image omitted: Data 6]

And there you have it, the top 5 heist movies that are sure to keep you on the edge of your seat!🍿

You can also explore other types of searches, such as finding similar movies based on genre, director, or even specific actors. May be try ‘A mysterious murder in a small town’ or ‘Documentary about groundbreaking scientific discoveries’. The possibilities are endless, so have fun experimenting with different criteria to discover new favorites!

Conclusion and Next Steps
FAISS is a powerful tool for performing similarity searches on large datasets. By integrating FAISS with Azure SQL and Microsoft Fabric, you can efficiently search for similar items within your data. The sample notebook provided here should help you get started with implementing similarity search in your own projects.

Feel free to experiment with different FAISS indexes and encoding models to optimize the performance and accuracy of your searches. Apply the techniques learned here to your data, and try various searches, including hybrid searches with filters on other columns like genre, cast, etc.

Happy searching!

References and Resources
DataSet: [Wikipedia Movie Plots](https://www.kaggle.com/datasets/jrobischon/wikipedia-movie-plots)
Check the SQL AI samples at [aka.ms/sqlaisamples](http://aka.ms/sqlaisamples). The sample notebooks can be found [here](https://github.com/Azure-Samples/SQL-AI-samples/blob/main/AzureSQLFaiss/Azure%20SQL_and_Faiss_Index_Creation.ipynb) and [here](https://github.com/Azure-Samples/SQL-AI-samples/blob/main/AzureSQLFaiss/Faiss_inference.ipynb).
YouTube: https://youtu.be/FrR3jZE9z8Y
Microsoft Learn: https://learn.microsoft.com/en-us/shows/data-exposed/similarity-search-with-faiss-and-azure-sql-data-exposed
Check SQL AI documentation [aka.ms/sqlai](http://aka.ms/sqlai)
Microsoft Fabric Notebooks: [How to use notebooks – Microsoft Fabric | Microsoft Learn](https://learn.microsoft.com/en-us/fabric/data-engineering/how-to-use-notebook)