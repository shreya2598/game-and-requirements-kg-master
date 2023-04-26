import jsonlines
import time



if __name__ == '__main__':
    enterprise_writer = jsonlines.open('../data_er/ER_companies.jl','w')
    st = time.time()
    with jsonlines.open('../data_with_ids/igdb_games.jl') as game_reader:
        for i,obj in enumerate(game_reader):
            if i%100 == 0:
                print("time taken for {} is {}: ".format(i,time.time() - st))
            key,val = list(obj.items())[0][0], list(obj.items())[0][1]
            developer_sim_url = []
            publisher_sim_url = []
            for company_url in val['developer_url']:
                with jsonlines.open('../data_with_ids/igdb_companies.jl') as company_reader:
                    for company_obj in company_reader:
                        company_key,company_val = list(company_obj.items())[0][0], list(company_obj.items())[0][1]

                        if company_val['url'] == company_url:
                            developer_sim_url.append(company_key)
            for publisher_url in val['publisher_url']:
                with jsonlines.open('../data_with_ids/igdb_companies.jl') as company_reader:
                    for company_obj in company_reader:
                        company_key, company_val = list(company_obj.items())[0][0], list(company_obj.items())[0][1]

                        if company_val['url'] == publisher_url:
                            publisher_sim_url.append(company_key)
            enterprise_writer.write({key:{'developer':developer_sim_url,'publisher':publisher_sim_url}})



