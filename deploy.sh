adress="bogdan@141.145.194.71"
dir="car_parser"

echo "adress = $adress"
echo "dir = $dir"

ssh -t "$adress" "rm -rf ~/$dir ; mkdir ~/$dir"
scp delerships.txt main.py pyrightconfig.json setup.sh start.sh "$adress"":///home/bogdan/$dir"
ssh -t "$adress" "cd ~/$dir ; ls ; bash setup.sh"

