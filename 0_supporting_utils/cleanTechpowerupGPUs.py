import json
import jsonlines

def cleanDict(cur_row):
    cleaned_dict = {}
    try:
        released_year = int(cur_row["Released"].split(",")[-1].strip())
    except:  # "Never Released" (or) "Unknown"
        released_year = -1

    try:
        gpu_chip = cur_row["GPU Chip"].strip()
    except:
        gpu_chip = ""

    try:
        bus_info = cur_row["Bus"].strip()
    except:
        bus_info = ""

    try:
        mem_split_list = cur_row["Memory"].split(",")
        memory_val_mb = int(mem_split_list[0].split()[0])
        memory_size = mem_split_list[0].split()[1]
        if memory_size == "GB":
            memory_val_mb *= 1024

        memory_type = mem_split_list[1].strip()
        memory_bits = int(mem_split_list[2].split()[0])
    except:
        memory_val_mb = -1
        memory_type = ""
        memory_bits = -1

    try:
        gpu_clock_mhz = int(cur_row["GPU clock"].split()[0])
    except:
        gpu_clock_mhz = -1

    try:
        memory_clock_mhz = int(cur_row["Memory clock"].split()[0])
    except:
        memory_clock_mhz = -1

    try:
        shaders_split_list = cur_row["Shaders / TMUs / ROPs"].split("/")
        shader_1 = int(shaders_split_list[0].strip())
        if len(shaders_split_list) == 4:
            shader_2 = int(shaders_split_list[1].strip())
        else:
            shader_2 = -1
        tmus = int(shaders_split_list[-2].strip())
        rops = int(shaders_split_list[-1].strip())
    except:
        shader_1 = -1
        shader_2 = -1
        tmus = -1
        rops = -1

    cleaned_dict["product_name"] = cur_row["Product Name"]
    cleaned_dict["product_url"] = cur_row["product_name_url"]
    cleaned_dict["released_year"] = released_year
    cleaned_dict["gpu_chip"] = gpu_chip
    cleaned_dict["bus_info"] = bus_info
    cleaned_dict["memory_val_mb"] = memory_val_mb
    cleaned_dict["memory_type"] = memory_type
    cleaned_dict["memory_bits"] = memory_bits
    cleaned_dict["gpu_clock_mhz"] = gpu_clock_mhz
    cleaned_dict["memory_clock_mhz"] = memory_clock_mhz
    cleaned_dict["shader_1"] = shader_1
    cleaned_dict["shader_2"] = shader_2
    cleaned_dict["tmus"] = tmus
    cleaned_dict["rops"] = rops

    return cleaned_dict

if __name__ == "__main__":
    inp_file = "../../data_with_ids/techpowerup_gpu_specs.jl"
    out_file = "../../data_with_ids/techpowerup_gpu_specs_cleaned.jl"

    result = []
    with open(inp_file, "r") as f:
        for cur_line in f:
            cur_dict = json.loads(cur_line)
            cur_key = list(cur_dict.keys())[0]
            cur_val = list(cur_dict.values())[0]

            if not bool(cur_val):
                continue

            cleaned_val = cleanDict(cur_val)

            new_dict = {}
            new_dict[cur_key] = cleaned_val
            result.append(new_dict)

    with jsonlines.open(out_file, "w") as f:
        f.write_all(result)

