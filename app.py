from elastic_transport import NodeConfig
from elasticsearch import Elasticsearch, NotFoundError

# Example of creating a NodeConfig instance
from elasticsearch.helpers import bulk

options = {
    'scheme': 'http',
    'host': '192.168.1.21',
    'port': 9200,
}

node_config = NodeConfig(**options)

es = Elasticsearch([node_config])

document = {
    "Name": "janki",
    "Age": 25,
    "Marks": 88,
    "Address": "Ahmedabad"
}
index_name = 'student1'
doc_id = 1

# Create & add document
res = es.index(index=index_name, id=doc_id, body=document)
print("Index Created and added document in index", res)

res = es.get(index=index_name, id=doc_id)

print("Retrieve(Read) a doc student1", res['_source'])

# Update
update_body = {
    "doc": {
        "Marks": 90
    }
}
res = es.update(index=index_name, id=doc_id, body=update_body)


print("Updated Marks in doc student1", res)


update_script = {
    "script": {
        "source": "ctx._source.Age = params.new_age",
        "params": {
            "new_age": 21
        }
    }
}
res = es.update(index=index_name, id=doc_id, body=update_script)


res1 = es.get(index=index_name, id=doc_id)

print("Retrieve(Read) a doc student1 after update", res1['_source'])


print("Updated Age in doc student1", res)

#Search
search_query = {
    "query": {
        "match": {
            "Name": "Tae"
        }
    }
}

res = es.search(index=index_name, body=search_query)

print("Search results:", res)


actions = [
    {"_index": "student1", "_id": "2", "_source": {"Name": "Tae", "Age": 27, "Marks": 90, "Address": "Seoul"}},
    {"_index": "student1", "_id": "3", "_source": {"Name": "JK", "Age": 25, "Marks": 90, "Address": "Busan"}},
    {"_index": "student1", "_id": "4", "_source": {"Name": "RM", "Age": 27, "Marks": 87, "Address": "Seoul"}},
    {"_index": "student1", "_id": "5", "_source": {"Name": "Jimin", "Age": 25, "Marks": 88, "Address": "Busan"}}
]

#bulkApi
success, failed = bulk(es, actions, index='student1', raise_on_error=True)


print(f"Successful index operations: {success}")
print(f"Failed index operations: {failed}")


doc = {
    "query": {
        "match_all": {}
    }
}
res = es.search(index="student1", body=doc)
for hit in res['hits']['hits']:
    print(hit['_source'])

aggregation = {
    "size": 0,
    "aggs": {
        "min_of_age": {
            "min": {
                "field": "Age"
            }
        },
        "max_of_age": {
            "max": {
                "field": "Age"
            }
        },
        "avg_of_marks": {
            "avg": {
                "field": "Marks"
            }
        },
        "sum_of_marks": {
            "sum": {
                "field": "Marks"
            }
        }
    }
}
res = es.search(index=index_name, body=aggregation)
print("Aggregation")
print(f"Min Age: {res['aggregations']['min_of_age']['value']}")
print(f"Max Age:{res['aggregations']['max_of_age']['value']}")
print(f"Avg of Marks:{res['aggregations']['avg_of_marks']['value']}")
print(f"Sum of Marks:{res['aggregations']['sum_of_marks']['value']}")

count = {
    "size": 0,
    "aggs": {
        "age_count": {
            "terms": {
                "field": "Age"
            }
        },
        "marks_count": {
            "terms": {
                "field": "Marks"
            }
        },
        "add_count": {
            "terms": {
                "field": "Address.keyword"
            }
        }
    }
}

res = es.search(index=index_name, body=count)
print("count:")
print("Age Counts:")
for bucket in res['aggregations']['age_count']['buckets']:
    print(f"Age {bucket['key']}: {bucket['doc_count']}")

print("Marks Counts:")
for bucket in res['aggregations']['marks_count']['buckets']:
    print(f"Marks {bucket['key']}: {bucket['doc_count']}")

print("Address Counts:")
for bucket in res['aggregations']['add_count']['buckets']:
    print(f"Address {bucket['key']}: {bucket['doc_count']}")



# Delete
# Check if the index exists before deleting (optional but recommended)
# if es.indices.exists(index=index_name):
#     try:
#         # Delete the index
#         es.indices.delete(index=index_name)
#         print(f"Index '{index_name}' deleted successfully.")
#     except NotFoundError:
#         print(f"Index '{index_name}' not found.")
# else:
#     print(f"Index '{index_name}' does not exist.")
