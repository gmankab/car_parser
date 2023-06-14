adress="bogdan@141.145.194.71"
dir="car_parser"

ssh -t "$adress" "rm -rf ~/$dir ; mkdir ~/$dir"
scp delerships.txt main.py pyrightconfig.json setup.sh start.sh "$adress"":///home/bogdan/car_parser"
ssh -t "$adress" "cd ~/$dir ; bash setup.sh"

