if [[ $# -ne 1 ]] ; then
    echo "need the congestion interface as an argument"
    exit -1
fi

IF=$1

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


#################### CLASSESS TESTS ####################

clean

run "default: pfifo_fast"

setup


# set up a netem qdisc with delay to ensure setup works properly
sudo tc qdisc add dev $IF parent 1:1 handle 10: netem delay 5ms reorder 25% 50% gap 5
run "200ms delay test"


# set up a pfifo qdisc with 30p buffer
reset_qdisc
sudo tc qdisc add dev $IF parent 1:1 handle 10: pfifo limit 30
run "pfifo w/ 30p buffer"


# set up a fq qdisc
reset_qdisc
sudo tc qdisc add dev $IF parent 1:1 handle 10: fq
run "fair queue"


# set up an sfq qdisc
reset_qdisc
sudo tc qdisc add dev $IF parent 1:1 handle 10: sfq
run "stochastic fair queue"


# set up a hhf qdisc
reset_qdisc
sudo tc qdisc add dev $IF parent 1:1 handle 10: hhf
run "heavy-hitter filter"



