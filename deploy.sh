adress="bogdan@141.145.194.71"

ssh -t "$adress" 'rm -rf ~/car_parser ; mkdir ~/car_parser'
scp delerships.txt main.py pyrightconfig.json setup.sh start.sh "$adress"":///home/bogdan/car_parser"
ssh -t "$adress" 'cd ~/car_parser ; bash setup.sh'

