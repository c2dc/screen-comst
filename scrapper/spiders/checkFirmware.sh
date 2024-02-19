#!/bin/bash

`mkdir "/tmp/firmware"`

files="$(cat $1)"
for file in $files
do
    `touch "/tmp/firmware/$file"`

    #if [[ ! $(grep "$file" $2) ]]
    #then
    #   echo $file
    #fi
done

exit 0