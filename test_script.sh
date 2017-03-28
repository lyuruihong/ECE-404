echo "Life’s  but  a  walking  shadow,  a  poor  player  that  struts  and  frets  his  hour  upon  the  stage  and
then is heard no more.  It is a tale told by an idiot, full of sound and fury, signifying nothing." > message.txt

echo 'Enter username:'
read name

tar xvf electronicSubmissionsHW6/$name.tar*

echo 'Enter Python Version:'
read ver

echo 'Enter Last name:'
read last

python$ver $last'_RSA_hw06.py' -e message.txt output.txt
python$ver $last'_RSA_hw06.py' -d output.txt decrypted.txt
python$ver $last'_breakRSA_hw06.py' message.txt cracked.txt

echo $'\nMessage is:\n'
cat message.txt

echo $'\ndecrypted output is:\n"
cat decrypted.txt

echo $'\ncracked output is:\n"
cat cracked.txt

rm *txt
