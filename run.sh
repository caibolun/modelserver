ps -eo pid,cmd | grep modelserver | grep -v grep | awk -F' ' '{print $1}' | xargs -I{} -t kill -9 {}
python server.py -c ./method/ping.ini -e "method.ping:Ping" &
wait
