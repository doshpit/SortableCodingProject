#!/usr/bin/python
#author: Danylo Shpit

from shutil import copyfile
import collections
import string
import json
import os

products = {}
matchings = {}
resultFile = "results.txt"

# creates a dictionary : product_name -> [manufacturer,model,family]
def processProducts():
    with open('products.txt') as products_file:
        for line in products_file:
            product = json.loads(line)
            name  = product["product_name"].lower()
            manuf = product["manufacturer"].split(" ")[0].lower()
            model  = product["model"].lower()
            family = product["family"][0].lower() if "family" in product else ""
            products[name] = [manuf,model,family]
            

# iterates through each product, and though a file of listings
# if listing matches the product based on [manufacturer,model,family] then we add it to dictionary of matchings : product_name -> [listings]
# if listing does not match the product, then we add it to another file, which will be used in next iteration of product
# eventually, we will run out of products or listings
def processListings ():
    copyfile("listings.txt", "listings_copy_0.txt")
    open("listings_copy_1.txt", 'w').close()
    fileNumber = 0
    for name in products:
        matchings[name] = []
        manuf = products[name][0]
        model  = products[name][1]
        family = products[name][2]
        other = open('listings_copy_'+str(0 if fileNumber else 1)+'.txt', 'w')
        with open('listings_copy_'+str(fileNumber)+'.txt') as listings_file:
            for line in listings_file:
                listing = json.loads(line)
                title = listing["title"].lower()
                if (manuf in title) and (model in title) and (family in title):
                    matchings[name].append(listing)
                else:
                    other.write(line)
            #switch the listings file for next product
            open("listings_copy_"+str(fileNumber)+".txt", 'w').close()
            fileNumber=int(not(fileNumber))
        listings_file.close()
        other.close()
    os.remove("listings_copy_0.txt")
    os.remove("listings_copy_1.txt")


#output matchings to results.txt
def writeResult():
    open(resultFile, 'w').close()
    resultFD  = open(resultFile, 'w')
    for product_name in matchings:
        line = '{'+'"product_name":"'+product_name+'","listings":'+json.dumps(matchings[product_name])+'}\n'
        resultFD.write(line)
    resultFD.close()



if __name__== "__main__":
    processProducts()
    processListings()
    writeResult()
