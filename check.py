import os

whitelist = set()
with open('manuscript_ids.txt', 'r') as f:
    for line in f:
        whitelist.add(line.strip())

downloaded = os.listdir('/home/holypriest/dev/python/analytics/accesses')
#print whitelist.difference(down_set)
down_list = []
for fil in downloaded:
    down_list.append(fil[0:23])
down_set = set(down_list)

with open('lacking.txt', 'w') as f:
    for fil in sorted(whitelist.difference(down_set)):
        f.write(fil)
        f.write('\n')
