#!/bin/bash

success=0
total=100

for i in $(seq 1 $total); do
  python3 generator.py | python3 vinegar.py
  success=$(($success + $?))
done

echo $(($total - $success))
