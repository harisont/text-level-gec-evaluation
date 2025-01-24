import os
import random
import json
from multigec_2025_utils import split_to_dict, md_to_dict

# these should become command-line parameters
split = "test"
subcorpus_path = "/home/harisont/Repos/spraakbanken/multigec-2025-data-providers/data/swedish/SweLL_gold"
system_out_path = "/home/harisont/Repos/spraakbanken/multigec-2025-data-providers/final_submissions/UAM-CSI/sv-swell_gold-fluency-hypo-{}.md"
out_path = "annotations/test.json"

team = os.path.normpath(system_out_path).split(os.path.sep)[-2]

subcorpus_dict = split_to_dict(subcorpus_path, split)

with open(system_out_path.format(split)) as system_out_file:
    system_out = system_out_file.read()
system_out_dict = md_to_dict(system_out)

data = []
for essay_id in subcorpus_dict:
    system_info = {}
    system_info[team] = dict(
        output=system_out_dict[essay_id],
        annotators={})
    data.append(dict(
        original=subcorpus_dict[essay_id]["orig"],
        # only use first gold ref
        reference=subcorpus_dict[essay_id]["refs"][0], 
        systems=system_info))
    
item_order = [i for i,_ in enumerate(data)]
random.shuffle(item_order)

metadata = dict(
        next_item=0,
        item_order=item_order,
        data=data)

with open(out_path, 'w') as f:
    json.dump(metadata, f, sort_keys=True, indent=4)