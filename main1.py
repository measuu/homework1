from fastapi import FastAPI, BackgroundTasks, HTTPException
import requests
import random
import math
from pydantic import BaseModel
import time


app = FastAPI()

data = {}

def get_data(user_id):
    res1 = requests.get(f"https://jsonplaceholder.typicode.com/users/{user_id}")
    res2 = requests.get(f"https://jsonplaceholder.typicode.com/users/{user_id}/posts")
    res3 = requests.get(f"https://jsonplaceholder.typicode.com/users/{user_id}/albums")
    res4 = requests.get(f"https://jsonplaceholder.typicode.com/photos?userId={user_id}&_limit=10")
    data[user_id] = [res1.json(), res2.json(), res3.json(), res4.json()]

@app.get("/user/{user_id}")
async def user(user_id:int, bg_tasks: BackgroundTasks):
    if user_id in data:
        return {'status': data[user_id]}
    bg_tasks.add_task(get_data, user_id)
    return {'status': 'ok'}


class CalcRequest(BaseModel):
    operation: str
    pars: dict


def factorial_task(n):
    if n > 1000:
        raise ValueError("Max factorial is 1000")
    return math.factorial(n)

def primes_task(start, end):
    primes = []
    for num in range(start, end + 1):
        if num > 1:
            for i in range(2, int(num ** 0.5) + 1):
                if num % i == 0:
                    break
            else:
                primes.append(num)
    return primes

def matrix_task(n):
    if n > 200:
        raise ValueError("Max matrix size is 200x200")

    A = [[random.randint(1, 9) for _ in range(n)] for _ in range(n)]
    B = [[random.randint(1, 9) for _ in range(n)] for _ in range(n)]
    C = [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    return C

def stats_task(data):
    n = len(data)
    mean = sum(data) / n
    data_sorted = sorted(data)

    if n % 2 == 1:
        median = data_sorted[n // 2]
    else:
        median = (data_sorted[n // 2 - 1] + data_sorted[n // 2]) / 2

    variance = sum((x - mean) ** 2 for x in data) / n
    std = math.sqrt(variance)
    return {"mean": mean, "median": median, "std": std}


@app.post("/calculate")
async def calculate(request: CalcRequest, background_tasks: BackgroundTasks):
    start = time.time()

    try:
        if request.operation == "factorial":
            result = factorial_task(request.pars["n"])
        elif request.operation == "primes":
            result = primes_task(request.pars["start"], request.pars["end"])
        elif request.operation == "matrix":
            result = matrix_task(request.pars["n"])
        elif request.operation == "stats":
            result = stats_task(request.pars["data"])
        else:
            raise HTTPException(status_code=400, detail="Unknown operation")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    end = time.time()
    execution_time = end - start

    background_tasks.add_task(print, f"Operation '{request.operation}' done in {execution_time}s")

    return {
        "operation": request.operation,
        "result": result,
        "execution_time_sec": execution_time
    }