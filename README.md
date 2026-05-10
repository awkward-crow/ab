# battery operator prototype

## installation

After cloning the repo, run

```sh
uv sync
```

## a short example

Try running

```sh
uv run example.py
```

It should give the following output,

      period     balance      charge
           0      200.00        0.00
           1      200.00        0.00
           2      200.00        0.00
           3      200.00        0.00
           4      200.00        0.00
           5      200.00        0.00
           6      200.00        0.00
           7      161.44        0.95
           8      161.44        1.90
           9       81.30        2.85


## a longer example

A simulation using the market data provided can be run as follows,

```sh
uv run main.py --plot
```

This should produce two plots, one of the balance of the battery operator the other of the charge of the battery over a time span of 100 periods i.e. 50 hours. A longer span can be plotted by adding the flag `--n`, for example `uv run main.py --plot --n=500` for 500 time periods.

This simulation uses a battery with the specifications given in the problem description and the market data provided. 

It can be inspected interactively by running

```sh
uv run python -i main.py
```

and consulting `main.py`.

## approach to the problem

The problem centred around how to handle the different time periods of the two markets. I chose to make this quite general rather than specific to two markets with 30 minute and 60 minute time periods. The action taken at any point is described by a `Contract`. It consists of one or more `Transactions` for successive periods of time. A contract for market 2 is made up of two transactions. Transactions can be to discharge or charge depending on whether the rate is positive or negative. The `Battery` only concerns itself with charge and cycles, it knows nothing of contracts. The strategy for operating the battery is simple. It is charged if the price in the previous period was below a certain threshold and there is capacity to charge it. Similarly, if the price is above a threshold and there is capacity, discharge.

 
#### end
