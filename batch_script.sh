#!/bin/bash

echo 'Enter username:'
read name

tar xvf electronicSubmissionsHW7/$name.tar.*

echo "Testing hash function..."
successes=0
testcases=10

for i in $(seq 1 $testcases) ; do
  echo "=================================================="
  echo "Test Case $i: "
  echo ""
  fortune | tee tmp.txt
  echo ""
  python2.7 hw07.py tmp.txt
  output=$(cat output.txt)
  python2.7 shaHash.py tmp.txt
  expected=$(cat hash.txt)
  diff <(echo $output) <(echo $expected) -y
  if [ $? -eq 0 ] ; then
    printf "\033[0;32mPASSED\n\033[0m"
    (( successes += 1 ))
  else
    printf "\033[0;31mFAILED\n\033[0m"
  fi
done
echo "=================================================="
rm tmp.txt
rm hash.txt
rm output.txt
echo "Results: $successes / $testcases"
