from SPARQLWrapper import SPARQLWrapper, JSON


def generate_visualization_data_discrete(class_name,property_name):
    '''
    :param class_name: Name of class in the KG
    :param property_name: Name of the property in the KG
    :return: tuple of form (a,b) where
    a is a list of tuples of the form (x,y) and is sorted on y ---> x is label and y is count
    b is a string either "continuous" or "discrete"
    depending on the type
    '''
    store_result = list()
    if (class_name == 'Game') and (property_name == 'hasGenre' or property_name == 'hasTheme' or property_name == 'hasGameMode'):

        sparql.setQuery('''
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX mgns: <http://inf558.org/games#> 
        PREFIX schema: <http://schema.org/>
        SELECT ?label (count(?label) as ?countLabel)
        WHERE{
          ?game a mgns:'''+class_name+''' .
          ?game mgns:'''+property_name+''' ?genre .
          ?genre rdfs:label ?label
        }
        group by ?label
        order by desc(?countLabel) 
        LIMIT 20
        ''')
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()


    if (class_name == 'Game') and (property_name == 'soldBy' or property_name == 'developedBy' or property_name == 'publisherBy'):
        sparql.setQuery('''
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX mgns: <http://inf558.org/games#> 
        PREFIX schema: <http://schema.org/>
        
        SELECT ?label (count(?label) as ?countLabel)
        WHERE{
          ?game a mgns:Game .
          ?game mgns:'''+property_name+''' ?s .
          ?s schema:name ?label . 
          
        }
        group by ?label
        order by desc(?countLabel) 
        LIMIT 20
        ''')
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

    if (class_name == 'Game') and (property_name == 'memory_MB' or property_name == 'diskSpace_MB'):
        sparql.setQuery('''
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX mgns: <http://inf558.org/games#> 
        PREFIX schema: <http://schema.org/>
        
        SELECT ?label (count(?label) as ?countLabel)
        WHERE{
          ?game a mgns:Game .
          ?game mgns:hasMSD ?s .
          ?s mgns:'''+property_name+''' ?label . 
          
        }
        group by ?label
        order by desc(?countLabel) 
        LIMIT 20
        ''')
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

    if (class_name == 'Game') and (property_name == 'ratingValue'):
        sparql.setQuery('''
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX mgns: <http://inf558.org/games#> 
                PREFIX schema: <http://schema.org/>
                SELECT ?label (count(?label) as ?countLabel)
                WHERE{
                  ?game a mgns:Game .
                  ?game mgns:ratingValue ?label .

                }
                group by ?label
                order by desc(?countLabel) 
                LIMIT 20
                ''')
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

    #print(results)
    for result in results['results']['bindings']:
        store_result.append((result['label']['value'],result['countLabel']['value']))
    type_of_key = results['results']['bindings'][0]['label']
    if ('xml:lang' in type_of_key) or ('datatype' in type_of_key and 'integer' in type_of_key['datatype']):
        return store_result, "discrete"
    if ('datatype' in type_of_key and 'decimal' in type_of_key['datatype']):
        return store_result, "continuous"



if __name__ == '__main__':
    sparql = SPARQLWrapper("http://localhost:3030/games/query")
    class_name,property_name = '',''
    '''
    works for 
    1. Game ---> hasGenre
    2. Game ---> hasTheme
    3. Game ---> hasGameMode
    4. Game ---> soldBy
    5. Game ---> developedBy
    6. Game ---> publishedBy
    7. Game ---> memory_MB
    8. Game ---> diskSpace_MB
    9. Game ---> ratingValue
    '''
    results = generate_visualization_data_discrete("Game","ratingValue")

    print(results)