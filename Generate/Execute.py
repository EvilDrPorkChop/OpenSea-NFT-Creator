import os
import GeneratorScript as GeneratorScript

# Set how many NFTs you want to generate.
NumberOfNFTS = 10
# Do not edit the count.
count = 1

for i in range(NumberOfNFTS):
    GeneratorScript.main(count)
    count = count + 1
    print("reached end of loop")
