from SPARQLWrapper import SPARQLWrapper, JSON
from collections import defaultdict

def get_games_based_on_genre(genre,sparql):
    sparql.setQuery('''
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX mgns: <http://inf558.org/games#> 
        PREFIX schema: <http://schema.org/>
        SELECT ?game ?game_name
        WHERE{
        ?game a mgns:Game .
        ?game mgns:hasGenre ?genre . 
        ?genre a mgns:Genre .
        ?genre rdfs:label ''' +str(genre)+'''@en .
        ?game schema:name ?game_name .
        }
        LIMIT 20
        ''')
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

def get_games_having_rating_higher(rating,sparql):
    sparql.setQuery('''
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX mgns: <http://inf558.org/games#> 
        PREFIX schema: <http://schema.org/>
        SELECT ?game ?game_name ?rating
        WHERE{
        ?game a mgns:Game .
        ?game mgns:ratingValue ?rating .
        FILTER(?rating > ''' +str(rating)+''')
        ?game schema:name ?game_name .
        }
        LIMIT 20
    ''')
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

def get_game_based_on_price_and_seller_url(lower_price,higher_price,sparql):
    sparql.setQuery('''
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX mgns: <http://inf558.org/games#> 
    PREFIX schema: <http://schema.org/>
    SELECT ?game ?game_name ?price ?seller_url
    WHERE{
    ?game a mgns:Game .
    ?game mgns:price_USD ?price .
    FILTER(?price > '''+str(lower_price)+ ''' && ?price < ''' + str(higher_price) + ''')
    ?game schema:name ?game_name .
    ?game mgns:sellerURL ?seller_url
    }
    LIMIT 20
    ''')
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

def get_info(game_id):
    sparql.setQuery('''
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX mgns: <http://inf558.org/games#> 
    PREFIX schema: <http://schema.org/>
    
    #SELECT ?game_summary ?name ?released_year ?platform_name ?developer_name ?publisher_name ?game_mode_label ?genre_label ?theme_label ?#rating ?seller_name ?price ?discount ?url
    SELECT ?game_summary ?name ?released_year ?platform_name ?developer_name ?publisher_name ?game_mode_label ?genre_label ?theme_label ?rating ?seller_name ?price ?discount ?url
    WHERE{
      mgns:'''+game_id+''' a mgns:Game ;
                 schema:name ?name ;
                 schema:description ?game_summary ;
                 schema:datePublished ?released_year ;
  OPTIONAL{mgns:'''+game_id+''' mgns:supportedPlatform ?platform ;
                      mgns:platformName ?platform_name} .
  OPTIONAL{mgns:'''+game_id+''' mgns:developedBy ?developer ;
                      schema:name ?developer_name } .
  OPTIONAL{mgns:'''+game_id+''' mgns:publishedBy ?publisher ;
                      schema:name ?publisher_name} .
  OPTIONAL{mgns:'''+game_id+''' mgns:hasGameMode ?game_mode ;
                      rdfs:label ?game_mode_label }.
  OPTIONAL{mgns:'''+game_id+''' mgns:hasGenre ?genre ;
                      rdfs:label ?genre_label }.
  OPTIONAL{mgns:'''+game_id+''' mgns:hasTheme ?theme ;
                      rdfs:label ?theme_label}.
  OPTIONAL{mgns:'''+game_id+''' mgns:ratingValue ?rating} .
  OPTIONAL{mgns:'''+game_id+''' mgns:soldBy ?seller;
                      schema:name ?seller_name} .
  OPTIONAL{mgns:'''+game_id+''' mgns:price_USD ?price} .
  OPTIONAL{mgns:'''+game_id+''' mgns:discount_percent ?discount} .
  OPTIONAL{mgns:'''+game_id+''' mgns:sellerURL ?url} .
  
  
}
      

    ''')
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

def released_year_query(released_year,sparql):
    sparql.setQuery('''
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX mgns: <http://inf558.org/games#> 
    PREFIX schema: <http://schema.org/>
    
    select ?game ?name ?date
    where{
      ?game a mgns:Game .
      ?game schema:name ?name .
      ?game schema:datePublished ?date .
      FILTER(?date = 2009)
    }
    ''')
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    res = defaultdict(lambda:list())
    for result in results['results']['bindings']:
        res[result['game']['value']].append((result['name']['value'],result['date']['value']))
    return res

def genre(genre,sparql):
    sparql.setQuery('''
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX mgns: <http://inf558.org/games#> 
    PREFIX schema: <http://schema.org/>
    
    select ?game ?name ?genre
    where{
      ?game a mgns:Game .
      ?game schema:name ?name .
      ?game mgns:hasGenre ?genre .
      ?genre rdfs:label ''' +str(genre)+'''@en .
      }
    '''
    )
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    res = defaultdict(lambda: list())
    for result in results['results']['bindings']:
        res[result['game']['value']].append((result['name']['value'], genre))
    return res



if __name__ == '__main__':
    sparql = SPARQLWrapper("http://localhost:3030/games/query")
    # Query games based on genre
    '''genre = '"Adventure"'
    results = get_games_based_on_genre(genre,sparql)
    for result in results['results']['bindings']:
        print("Game URI: ",result['game']['value'],end = ' ')
        print("Game Name: ",result['game_name']['value'])'''

    # Query game names based on rating
    '''rating = 80
    results = get_games_having_rating_higher(rating,sparql)
    for result in results['results']['bindings']:
        print("Game URI: ", result['game']['value'], end=' ')
        print("Game Name: ", result['game_name']['value'], end = ' ')
        print("Rating: ", result['rating']['value'])'''

    # Query game and seller url based on price range
    '''lower_price = 10
    higher_price = 20
    results = get_game_based_on_price_and_seller_url(lower_price,higher_price,sparql)
    for result in results['results']['bindings']:
        print("Game URI: ", result['game']['value'], end=' ')
        print("Game Name: ", result['game_name']['value'], end = ' ')
        print("Game Price: ",result['price']['value'], end = ' ')
        print('Seller URL: ',result['seller_url']['value'])'''

    # Query games based on game id
    '''results = get_info('mig_3')
    game_info_dict = defaultdict(lambda: set())
    for result in results['results']['bindings']:
        for key in result.keys():
            game_info_dict[key].add(result[key]['value'])
    for key in game_info_dict.keys():
        game_info_dict[key] = list(game_info_dict[key])
    print(game_info_dict)'''

    # Query based on released year
    release_y = released_year_query(2009,sparql)
    gen = genre('"Adventure"',sparql)
    int_key = set(list(release_y.keys())).intersection(set(list(gen.keys())))
    print(len(int_key))



