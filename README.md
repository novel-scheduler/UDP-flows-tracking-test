# UDP Flow Tracking Test

## How To Test
The simplest way to get started is to use run `automate_full_test.sh`:
```
bash automate_full_test.sh [number of client connections] [port number] [qdisc name]
```
Example 1:
```
bash automate_full_test.sh 7 5000 FIFO
```
Example 2:
```
bash automate_full_test.sh 7 5000 REORDER
```
<br/>

## Sample Results
FIFO:
```
Client Input & Desired (Expected) Match => True
Client & Server Match => True
Server & Desired (Expected) Match => True
```
REORDER: 
```
Client Input & Desired (Expected) Match => True
Client & Server Match => False
Server & Desired (Expected) Match => False
```

<br/>

## Notes
On the high level, the automated full test does the following:

- Generate random and desired flow sequences
- Run server and client programs
- Compare the flow sequence outputs on the server side and the client side

You can take a look inside `automate_full_test.sh` to view each python program being executed.
By manually running the programs one by one, you can have more control over the test, such as different types of input flows, names of the files being used, type of randomness, etc. Use --help to view available arguments for each program:
```
python3 generate_flow_seq.py -h

usage: generate_flow_seq.py [-h] [-n NUM_CONN] [-l ITERATIONS]
                            [-r RANDOM_FLOW_SEQ_FILE]
                            [-d DESIRED_FLOW_SEQ_FILE] [-c {desired,random}]
                            [-i INPUT_FLOW_SEQ_FILE]
                            [-m {grouped,independent}]

optional arguments:
  -h, --help            show this help message and exit
  -n NUM_CONN, --num-conn NUM_CONN
                        Number of client connections
  -l ITERATIONS, --iterations ITERATIONS
                        Number of iterations. The length of the flow sequence
                        is equal to num_conn * iterations. (ex: 3 * 40 = 120
                        lines)
  -r RANDOM_FLOW_SEQ_FILE, --random-flow-seq-file RANDOM_FLOW_SEQ_FILE
                        Name of file to store randomly generated flow sequence
  -d DESIRED_FLOW_SEQ_FILE, --desired-flow-seq-file DESIRED_FLOW_SEQ_FILE
                        Name of file to store desired flow sequence
  -c {desired,random}, --chosen-seq-type {desired,random}
                        Type of flow sequence to store to the file that
                        contains input flow sequence for the client side
  -i INPUT_FLOW_SEQ_FILE, --input-flow-seq-file INPUT_FLOW_SEQ_FILE
                        Name of file to store input flow sequence for client
  -m {grouped,independent}, --mode {grouped,independent}
                        Mode on which the random generation runs. In grouped
                        mode, all flows will paced equally so that no flow
                        number appears twice before the other flow numbers
                        have appeared an equal number of times. In independent
                        mode, the flow order will be comletely random, where a
                        flow number may appear multiple times in a row and
                        break the equal pace shared among other flows
```