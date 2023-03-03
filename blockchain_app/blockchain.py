

#Import registry data
import pandas as pd


Registry_Dataset = pd.read_csv('RegistryDataset.csv')
df_Registry = pd.DataFrame(Registry_Dataset)
df_Registry


#How to pull one cell from the matrix
#df_Registry["str_name"][1]


#Convert Tiff File to String
"""""
import base64
with open("test_tiff.tiff", "rb") as image2string:
    converted_string = base64.b64encode(image2string.read())

  
with open('encode.bin', "wb") as file:
    file.write(converted_string)
"""    
#newFile = str(converted_string)
newFile = "placeholder"
newFile


import hashlib as hasher
import datetime as date

# Define what a Snakecoin block is
class Block:
  #All of the attributes of the block
  def __init__(self, index, timestamp, street_name, date, consideration, town_code, garentor_lname, \
               garentor_fname, garentee_lname, garentee_fname, signed_doc, previous_hash):
    #Define each attribute
    # Attributes already included in code
    self.index = index
    self.timestamp = timestamp
    
    
    #Attributes I added
    self.street_name = street_name
    self.date = date
    self.consideration = consideration
    self.town_code = town_code
    self.garentor_lname = garentor_lname
    self.garentor_fname = garentor_fname
    self.garentee_lname = garentee_lname
    self.garentee_fname = garentee_fname
    self.signed_doc = signed_doc
    
    #Attributes already Included
    self.previous_hash = previous_hash
    self.hash = self.hash_block()
    
  def __repr__(self):
        #Return all of the attributes of the block as strings
    return "%04d: %s, %s, %s, %s, %s, %s, %s, %s, %s, %s : %s" % (self.index,str(self.timestamp),str(self.street_name),\
                                                              str(self.date),str(self.consideration),str(self.town_code),\
                                                              str(self.garentor_lname),str(self.garentor_fname),\
                                                              str(self.garentee_lname), str(self.garentee_fname), \
                                                              str(self.signed_doc), str(self.previous_hash))
  def hash_block(self):
  #generate a hash code
    sha = hasher.sha256()
    sha.update(repr(self).encode('ascii'))
    return sha.hexdigest()


# Generate genesis block
def create_genesis_block():
  # Manually construct a block with
  # index zero and arbitrary previous hash
  return Block(0, date.datetime.now(), "Genesis Block","a","b","c","d","e","f","g","h", "0")



#I didn't edit this one
# Create the blockchain and add the genesis block
blockchain = [create_genesis_block()]
previous_block = blockchain[0]
# Show the blockchain
#blockchain
#print("Hash: {}\n".format(blockchain[0].hash))


# Generate all later blocks in the blockchain
def next_block(last_block):
  this_index = last_block.index + 1
  this_timestamp = date.datetime.now()
  
      
  #Include how we will define the new attributes      
  this_str_name = df_Registry["str_name"][last_block.index]
  this_date = df_Registry["date"][last_block.index]
  this_consideration = df_Registry["consideration"][last_block.index]
  this_town_code = df_Registry["town_code"][last_block.index]
  this_garentor_lname =  df_Registry["garentor_lname"][last_block.index]
  this_garentor_fname = df_Registry["garentor_fname"][last_block.index]
  this_garentee_lname = df_Registry["garentee_lname"][last_block.index]
  this_garentee_fname = df_Registry["garentee_fname"][last_block.index]
  this_signed_doc = newFile

        
  
  this_hash = last_block.hash
  #Added the new attributes
  return Block(this_index, this_timestamp, this_str_name, this_date, this_consideration, this_town_code,
               this_garentor_lname,this_garentor_fname, this_garentee_lname, this_garentee_fname, this_signed_doc, this_hash)



# How many blocks should we add to the chain
# after the genesis block
num_of_blocks_to_add = 20

# Add blocks to the chain
for i in range(0, num_of_blocks_to_add):
  block_to_add = next_block(previous_block)
  blockchain.append(block_to_add)
  previous_block = block_to_add
  # Tell everyone about it!
  #print("Block #{} has been added to the blockchain!".format(block_to_add.index))
  #print("Hash: {}\n".format(block_to_add.hash))

print("done")

"""""
# https://www.scaler.com/topics/python-write-list-to-file/
# Run to save all current Blockchain Hashcodes
file = open('blockchain.txt','w')
for i in range (0, len(blockchain)):
    hash_i = blockchain[i].hash
    file.write(hash_i + '\n' )
file.close()



file = open('blockchain.txt','r')
file.readlines(2)


#Source for readlines
# https://www.w3schools.com/python/ref_file_readlines.asp

file = open('blockchain.txt','r')
for i in range (0, len(blockchain)):
    blockchain[i].hash = file.readlines(i)
file.close()



#Use to check the info is correct
#blockchain[8]

#Use to check the info is correct
#df_Registry.iloc[8]
"""


from warnings import warn
def validate_blockchain(in_blockchain):
    if in_blockchain[0].hash != '51648e4eb7648ea856ea812370449045de057681164ce3595018ccb0496a83ae':
        warn('Blockchain is invalid!')
    else:
        for current_position in range(1, len(in_blockchain)):
            previous_position = current_position - 1
            if in_blockchain[previous_position].hash_block() == in_blockchain[current_position].previous_hash:
                i = 1
            else:
                warn('Block %d is invalid! (%s)' % (current_position, repr(in_blockchain[current_position])))
                i = 2
                break

        if i == 1:
            print('Blockchain Valid')


blockchain[0].hash = '51648e4eb7648ea856ea812370449045de057681164ce3595018ccb0496a83ae'
validate_blockchain(blockchain)


from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():
    print(request.form)
    return render_template("form.html")



"""""
#I didn't change

old_block_10_data = blockchain[10].hash
new_block_10_data = "Hey I'm an invalid data"
blockchain[10].hash = new_block_10_data
validate_blockchain(blockchain)
# replace the original, so we can try something else
blockchain[10].hash = old_block_10_data





validate_blockchain(blockchain)




#Pull Pieces of a String
Block_A = str(blockchain[1])
Block_A[3:20]




#Source
#         https://www.geeksforgeeks.org/python-finding-strings-with-given-substring-in-list/

#Query the Blockchain for specific strings
 

new_bc = [str(i) for i in blockchain]
 
# initializing substring
subs = 'SOPHIE'
 
# using filter() + lambda
# to get string with substring
res = list(filter(lambda x: subs in x, new_bc))
 
# printing result
print("All strings with given substring are : " + str(res))

blockchain[2]

"""
