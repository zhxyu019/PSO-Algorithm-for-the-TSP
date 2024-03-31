## PSO Algorithm for the Travelling Salesman Problem (TSP)
A Modification to the PSO Algorithm for the TSP - Continuous to Discrete Nature

## How to Run 
### 1. Clone the Project
  ```bash
  git clone https://github.com/zhxyu019/PSO-Algorithm-for-the-TSP.git
  ```
### 2. Select the Dataset to run
Find this line of code:  ```towns = load_towns(DATA_NODE_NUMBER)```

Replace ```DATA_NODE_NUMBER``` with the number of nodes in the dataset 

### To add datasets:
- Create File under ```test_data``` & name it ```towns_NUMBER.data```
Replace ```NUMBER``` with the number of nodes in the dataset
- Ensure that your ```.data``` file has the correct number of nodes in the  `(x , y)` coordinate format

Remarks:
- `.txt` files should work
- Ensure that no empty spaces are in the  `.data` file or else the code WILL NOT RUN
- Ensure that there are only two columns in the `.data` file, namely the `x , y` coordinates

### 3. Run the Python file ```tsp.py```

## Datasets Added
- ulysses16, ulysses22, eil51, berlin52, st70, rat99, kroA100, kroA200, a280

## References
- All datasets are the from the TSPLIB (TSP Library)
- Coordinates Taken from: https://github.com/coin-or/jorlib
