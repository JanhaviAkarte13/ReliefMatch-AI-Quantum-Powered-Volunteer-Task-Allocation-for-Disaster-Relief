import time

from scipy.optimize import linear_sum_assignment

from qaoa_allocator import quantum_allocate


def compare(volunteers, tasks):

    start = time.time()

    quantum_result = quantum_allocate(volunteers, tasks)

    quantum_time = time.time() - start

    print("\nQuantum Allocation")

    print(quantum_result)

    print("Quantum Time :", round(quantum_time,4),"seconds")


if __name__ == "__main__":

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

    compare(volunteers,tasks)