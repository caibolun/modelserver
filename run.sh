ps -eo pid,cmd | grep mmbizimggeneralclassify_business | grep -v grep | awk -F' ' '{print $1}' | xargs -I{} -t kill -9 {}
python server.py -c ./method/ping.ini -e "method.ping:Ping" -i ./method/mmbizimggeneralclassify_business.conf &
wait
