# Unless explicitly stated otherwise all files in this repository are licensed under the the Apache License Version 2.0.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2021 Datadog, Inc.

from collections import defaultdict
import requests


def to_camel_case(input):
    return "".join(ele.title() for ele in input.split("_"))


URL = "https://raw.githubusercontent.com/DataDog/appsec-event-rules/main/build/recommended.json"

data = requests.get(URL).json()

version = data["version"]

rules_key = {"1.0": "events", "2.1": "rules", "2.2": "rules"}[version]

result = defaultdict(dict)
for event in data[rules_key]:
    name = event["id"]
    name = name.replace("-", "_")

    try:
        result[event["tags"]["type"]][name] = event
    except KeyError:
        print(event)

HEADER = f"""# Unless explicitly stated otherwise all files in this repository are licensed under the the Apache License Version 2.0.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2021 Datadog, Inc.

# Automatic generatiom from:
#    python utils/scripts/extract_appsec_waf_rules.py
"""

with open("utils/waf_rules.py", "w") as f:
    f.write(HEADER)

    for key, rules in result.items():
        f.write(f"\n\nclass {key}:\n")
        for name, rule in rules.items():
            f.write(f"    {name} = \"{rule['id']}\"  # {rule['name']}\n")

with open("utils/interfaces/_library/appsec_data.py", "w") as f:
    f.write(HEADER)

    f.write("\n\nrule_id_to_type = {\n")
    for key, rules in result.items():
        for name, rule in rules.items():
            rule_id = rule["id"]
            f.write(f'    "{rule_id}": "{key}",\n')
    f.write("}\n")
