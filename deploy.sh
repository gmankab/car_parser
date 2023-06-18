username="ubuntu"
adress="ubuntu@141.145.214.106"
dir="car_parser_7000"

echo "adress = $adress"
echo "dir = $dir"

ssh -t "$adress" "rm -rf ~/$dir ; mkdir ~/$dir"
scp delerships.txt main.py pyrightconfig.json setup.sh start.sh "$adress"":///home/$username/$dir"
ssh -t "$adress" "cd ~/$dir ; ls ; bash setup.sh"

