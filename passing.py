import re
import json
from datetime import datetime

log_path = "/var/log/auth.log"

result = []

with open(log_path, "r") as f:

    for line in f:

        if "Failed password" in line:

            ip_match = re.search(
                r'from (\d+\.\d+\.\d+\.\d+)',
                line
            )

            time_match = re.search(
                r'^(\d+-\d+-\d+T\d+:\d+:\d+)',
                line
            )

            if ip_match and time_match:

                ip = ip_match.group(1)

                time_str = time_match.group(1)

                dt = datetime.fromisoformat(time_str)

                timestamp = dt.timestamp()

                result.append({

                    "ip": ip,

                    "timestamp": timestamp
                })

with open("logs.json", "w") as f:

    for r in result:

        f.write(json.dumps(r) + "\n")
