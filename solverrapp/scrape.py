import inspect
from solverrapp import connectors as cons


def search_connectors(query:str, tags_exclude=None):
    print(f"Searching for {query}")
    if tags_exclude is None:
        tags_exclude = []

    connectors = cons.Connector.__subclasses__()
    print(connectors)
    
    exclude_cons = []
    
    for tag in tags_exclude:
        for connector in connectors:
            if tag in connector.tags:
                exclude_cons.append(connector)
                
    for con in exclude_cons:
        connectors.remove(con)

    results = []

    for connector in connectors:
        results.append(connector.search(connector, query))

    return results
        
    
                