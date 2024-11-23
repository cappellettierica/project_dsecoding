# tuples are lists that you can't modify 
my_string='erica'
print(my_string[1]) #character r

my_list=['one', 'two','three']
print(my_list[1])
my_list[1]="four"

my_tuple=('alfa', 'beta', 'gamma')
print(my_tuple[1])
# can't modify the tuple. more efficient in terms of memory than lists because it has fewer methods and functionalities. 
# useful when you want to iterate and use its values without editing

my_tuple.index("gamma") # index of gamma, 2
# 'my_touple.' to see all the things you can do. none of them editing. 


# sets
fruits={"apple", "banana", "cherry"}
fruits.add("strawberry") # an item is added
fruits.add("apple") # already present so nothing happens 
fruits.remove("banana") # an item is dropped 

if "peach" in fruits:
    fruits.remove("peach") # removing in item not in the set generates an error 

fruits.discard("peach") # no errors raised even if peach not in the set 

print(fruits)

# sets ensure object uniqueness and no duplication. 
# if you wnt to remove duplication in a list, transform it in a set and then back to a list
my_list1=['one', 'two', 'three', 'one']
print(my_list1)
my_list1=list(set(my_list1))
print(my_list1)

# sets support basic sets operations; intersect, union... 
odds={1, 3, 5, 7}
even={2, 4, 6, 8}
primes={1, 2, 3, 5}
print(odds.union(even))
print(even.union(odds)) # the same 
print(odds.intersection(primes))
print(odds.difference(primes)) # A-B where A is odds and B is primes 