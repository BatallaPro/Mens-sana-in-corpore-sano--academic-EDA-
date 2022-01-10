# For quick empty list assignment
def mklist(n):
    for i in range(n):
        yield []
        
# To easily add very data to the correct list
def item_to_lists(item, lists):
    for i in range(len(item)):
        lists[i].append(item[i])
        
    return lists
        
# To return the name of an object
def nameof(obj, namespace):
    return [name for name in namespace if namespace[name] is obj][0]