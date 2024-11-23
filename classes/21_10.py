import sys
import csv
# lambda functions and map functions

# lambda: anonymous function 
# syntax -> lambda arguments: expression 
# usuallly we would use:
def square_function(var):
    return var**2

# print(square_function(2))

# using lambda: 
square=lambda x: x**2 # anonymous function 
# print(square(2))
# lambda functions are useful when you want to apply an expression to a list of values 
# which brings us to
# map function: takes two parameters
# map (function, items)
nums_to_square=(1, 2, 3, 4, 5)
# squared=map(square_function, nums_to_square) # the function we did in def 
# the result cannot be printed immediately: transform it to a list first 
squared=list(map(square_function, nums_to_square))
# print(squared)

# lambda and map often used together, instead of using def 
squared_1=list(map(square, nums_to_square)) # lambda function 
# print(squared_1)


# nums=[2, 5, 8, 9]
#normalizing the value means 
# norm_nums=[(2-2)/7, (5-2)/7, (8-2)/7, (9-2)/7]

# X_norm=(X-min)/(max-min)

# lamda x: (x-min)/(max-min)


# consider the supermarket data of 30_09
# each record contains the number of items that have been sold 
# calculate the normalized quantities of sold items 
# open the file and read the content
with open("/home/ericacappelletti02/phyton/classes/30_09/supermarket.csv", newline="") as f:
    reader = csv.reader(f, delimiter=",")
    records = list(reader)

records.pop(0) # popping away the first item 
print(records[0][1]) # printing name of branch
print(records[0][7]) # printing items sold 

branches=[] # will be the list of branch names
items=[] # will be a list containing all the quantities sold by that branch 

for r in records:
    if r[1] not in branches:
        # if the branch is new
        branches.append(r[1]) # adding to branches the name of the new branch 
        try:
            branch_quantities=[int(r[7])] # i store here the quantities sold by the branch in this record 
            # i transform it into a list - hence the square brackets - that contains 1 item, that corresponds to quantity sold
            # int = the number stored is an integer so that LATER i can sum them all 
        except: 
            branch_quantities=[0] # if the conversion of r[7] is failing 
            # so it means that r[7] cannoty be an integer - then i assume that 0 items are being sold and in r[7] there is a word like no items.  
        items.append(branch_quantities)
    else:
        # the branch is already known
        branch_index=branches.index(r[1])  # i'm looking for the already existing branch's position 
        try:
            items[branch_index].append(int(r[7])) # i add the new element about the already present branch and i add it to items 
        except: 
            items[branch_index].append(0)

# this creates: 
# branches=['Alex', '','']
# items=[[9, 10, 75], [], []]

for b, i in zip(branches, items): # zip: i want to look through the iterables and combine the elements in the same posiiton
    s=sum(i) # summing the values of items sold by b
    print(f"The branch {b} has sold {s}.") 

# print(items[0])
# normalize the series  of values for each branch 
normalized_items=[]
for i in items: 
    min_value=min(i)
    max_value=max(i)

    norm_list=list(map(lambda x:round((x-min_value)/(max_value-min_value), 2), i))
    # execute lambda for all the items contained in i 
    normalized_items.append(norm_list)

print(normalized_items[0])    


sys.exit()