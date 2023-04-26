import jsonlines
import time



if __name__ == '__main__':
    platform_writer = jsonlines.open('../data_er/ER_platform.jl','w')
    st = time.time()
    with jsonlines.open('../data_with_ids/igdb_games.jl') as game_reader:
        for i,obj in enumerate(game_reader):
            if i%100 == 0:
                print("time taken for {} is {}: ".format(i,time.time() - st))
            key,val = list(obj.items())[0][0], list(obj.items())[0][1]
            sim_url = []
            for platform_url in val['platform_urls']:
                with jsonlines.open('../data_with_ids/igdb_platforms.jl') as platform_reader:
                    for platform_obj in platform_reader:
                        platform_key,platform_val = list(platform_obj.items())[0][0], list(platform_obj.items())[0][1]

                        if platform_val['url'] == platform_url:
                            sim_url.append(platform_key)
            platform_writer.write({key:sim_url})



