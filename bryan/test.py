import json
class myob():
    def __init__(self, ins):
        self.instance = ins
        print(f"New Object Created: {self.instance}")
    def onData(self):
        print("CALLED")

with open('sample.json', 'r') as loader:
    mydic = json.load(loader)

objs = {}
for k in mydic.keys():
    objs[k] = myob(mydic[k]['instance'])

print(objs)
for o in objs.keys():

    objs[o].onData()

