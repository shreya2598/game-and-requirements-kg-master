import json
import numpy
import jsonlines
import sys

if __name__ == "__main__":
    inp_file = sys.argv[1]
    cur_data_field = sys.argv[2]
    out_file = sys.argv[3]
    prefix = "mgns_" + cur_data_field + "_{}"
    result = []
    index = 0
    with open(inp_file, "r") as f:
        for cur_line in f:
            cur_dict = json.loads(cur_line)
            cur_prefix_id = prefix.format(index)
            new_dict = {}
            new_dict[cur_prefix_id] = cur_dict
            result.append(new_dict)
            index = index + 1

    with jsonlines.open(out_file, "w") as f:
        f.write_all(result)