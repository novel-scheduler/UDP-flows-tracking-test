# Quickstart script for running a full test

# Validate number of arguments
if [[ $# -ne 3 ]] ; then
    echo "Need all three arguments"
    exit -1
fi

# Default network interface is local host
IF="lo"

#################### FUNCTIONS ####################

clean () {
	echo "======================================"
	echo "Cleaning qdiscs to setup..."

	sudo tc qdisc del dev $IF root

	echo "All qdiscs have been reset"
	echo "======================================"
}

# remove current qdisc on router, but keep the htb max link rate
reset_qdisc () {

	echo "======================================"
	echo "Resetting qdisc for next test..."
  
	sudo tc qdisc del dev $IF parent 1:1

	echo "The qdisc has been reset"
	echo "======================================"
}

# set max link rate to 50 Mbps with htb qdisc; this will remain throughout all the tests
setup () {
	sudo tc qdisc add dev $IF root handle 1: htb default 1

	sudo tc class add dev $IF parent 1: classid 1:1 htb rate 50Mbit
}

# pause to allow user to run patient/surgeon scripts
run () {
	echo "Please run client/server programs now [$1]"

	read -p "Once ready, press any key to continue... " -n1 -s

	echo ""
}

run () {
	echo "[$1]"
	read -p "Once ready, press any key to continue... " -n1 -s
	echo ""
}

#################### RUN TEST ####################

# User-defined variables
NUM_CONN=$1
PORT=$2
QDISC=$3
printf "(User Input) Number of Connections: $NUM_CONN\n"
printf "(User Input) Port: $PORT\n"
printf "(User Input) Qdisc: $QDISC\n"
printf "\n\n"

# Start of test
run "Full Test Automation"

# Clean qdisc
clean

if [ "$QDISC" = "FIFO" ]; then
	run "Chosen QDISC: FIFO"
elif [ "$QDISC" = "REORDER" ]; then
	setup
	sudo tc qdisc add dev $IF parent 1:1 handle 10: netem delay 500ms reorder 100% 50% gap 3
	run "Chosen QDISC: REORDER"
else 
	run "Default QDISC: FIFO"
fi

# Generate flow sequences
python3 generate_flow_seq.py -n $NUM_CONN

run "Random & Desired Flows Generated"

# Server does not know when the client has stopped sending packets, so the user
# may have to manually terminate the server program with ctrl + c 
(trap 'kill 0' SIGINT; python3 multi_server.py & python3 multi_client.py -n $NUM_CONN)

run "Client & Server Have Interacted"

# Compapre flow sequences
python3 compare_flow_sequence.py

run "Flow Order Comparison Finished"

printf "\n---------- (Result): ----------\n"
cat compare_result.txt
printf "\n\n"


