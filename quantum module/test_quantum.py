from qaoa_allocator import quantum_allocate

volunteers = [

{
"id":1,
"skill":"Medical",
"location":"Zone A",
"available":True
},

{
"id":2,
"skill":"Food",
"location":"Zone B",
"available":True
}

]

tasks = [

{
"id":1,
"required_skill":"Medical",
"location":"Zone A",
"urgency":9
},

{
"id":2,
"required_skill":"Food",
"location":"Zone B",
"urgency":8
}

]

allocation = quantum_allocate(volunteers,tasks)

print(allocation)