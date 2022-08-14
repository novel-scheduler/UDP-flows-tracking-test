# Quickstart script for running a full test
# The qdisc test (qdisc_test.sh) should be running before this script is 
# executed so that different qdiscs can be tested

run () {
	echo "[$1]"
	read -p "Once ready, press any key to continue... " -n1 -s
	echo ""
}

run "Full Test Automation"

python3 generate_flow_seq.py

run "Random & Desired Flows Generated"

(trap 'kill 0' SIGINT; python3 multi_server.py & python3 multi_client.py)

run "Client & Server Have Interacted"

python3 compare_flow_sequence.py

run "Flow Order Comparison Finished"

cat compare_result.txt


