# Import any Packages Used
import os
import pandas as pd  # Adds in Data for Blockchain initialization
import base64  # For converting Images to Strings
import hashlib as hasher  # Create Hashcodes
import datetime as date  # Create Dates
from PIL import Image  # Print image
from csv import writer

genesis_hash = "76b0cdd60141d895de100892604f7ab5c84847b0bac32c9e533a728bf050cd80"
# BASENAME = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(os.path.abspath(__file__))


# Open csv file and return a dataframe
def Import_Dataset(csv_name):
    Registry_Dataset = pd.read_csv(csv_name)
    df_Registry = pd.DataFrame(Registry_Dataset)
    return (df_Registry, len(Registry_Dataset))


# Open a file and return a string of that file (this string is stored in the file encode.bin)
def File_to_String(file_name, index):
    with open(file_name, "rb") as image2string:
        converted_string = base64.b64encode(image2string.read())
    with open("encode%s.bin" % index, "wb") as file:
        file.write(converted_string)
    converted_string = str(converted_string)
    return converted_string


# Pass Block index and return a pop-up with the image
def String_to_Image(index):
    file = open("encode%s.bin" % index, "rb")
    byte = file.read()
    file.close()

    decodeit = open("file%s.jpeg" % index, "wb")
    decodeit.write(base64.b64decode((byte)))
    decodeit.close()

    img = Image.open("file%s.jpeg" % index)
    img.show()

    return


# Define what a Block is
class Block:
    # All of the attributes of the block
    def __init__(
        self,
        index,
        timestamp,
        street_name,
        date,
        consideration,
        town_code,
        guarantor_lname,
        guarantor_fname,
        guarantee_lname,
        guarantee_fname,
        signed_doc,
        previous_hash,
    ):
        # Define each attribute
        self.index = index
        self.timestamp = timestamp
        self.street_name = street_name
        self.date = date
        self.consideration = consideration
        self.town_code = town_code
        self.guarantor_lname = guarantor_lname
        self.guarantor_fname = guarantor_fname
        self.guarantee_lname = guarantee_lname
        self.guarantee_fname = guarantee_fname
        self.signed_doc = signed_doc
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def __repr__(self):
        # Return all of the attributes of the block as strings
        return """Index: %05d;
Timestamp: %s;
Street Name: %s;
Date: %s;
Consideration: %s;
Town Code: %s;
Guarentor: %s %s;
Guarentee: %s %s;
Signed Doc: %s;
Previous Hash: %s;
""" % (
            self.index,
            str(self.timestamp),
            str(self.street_name).upper(),
            str(self.date),
            str(self.consideration),
            str(self.town_code).upper(),
            str(self.guarantor_fname).upper(),
            str(self.guarantor_lname).upper(),
            str(self.guarantee_fname).upper(),
            str(self.guarantee_lname).upper(),
            str(self.signed_doc),
            str(self.previous_hash),
        )

    # generate a hash code
    def hash_block(self):
        sha = hasher.sha256()
        sha.update(repr(self).encode("ascii"))
        return sha.hexdigest()


# Generate genesis block
def create_genesis_block():
    # Manually construct a block with
    # index zero and arbitrary previous hash
    return Block(
        0,
        date.datetime.now(),
        "Genesis Block",
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "0",
    )


# Generate all later blocks in the blockchain
def next_block(last_block):
    this_index = last_block.index + 1
    this_timestamp = date.datetime.now()

    this_str_name = df_Registry["str_name"][last_block.index]
    this_date = df_Registry["date"][last_block.index]
    this_consideration = df_Registry["consideration"][last_block.index]
    this_town_code = df_Registry["town_code"][last_block.index]
    this_guarantor_lname = df_Registry["guarantor_lname"][last_block.index]
    this_guarantor_fname = df_Registry["guarantor_fname"][last_block.index]
    this_guarantee_lname = df_Registry["guarantee_lname"][last_block.index]
    this_guarantee_fname = df_Registry["guarantee_fname"][last_block.index]
    this_signed_doc = df_Registry["file"][last_block.index]

    this_hash = last_block.hash
    # Added the new attributes
    return Block(
        this_index,
        this_timestamp,
        this_str_name,
        this_date,
        this_consideration,
        this_town_code,
        this_guarantor_lname,
        this_guarantor_fname,
        this_guarantee_lname,
        this_guarantee_fname,
        this_signed_doc,
        this_hash,
    )


def Add_blocks_from_CSV(number_of_blocks):
    blockchain = [create_genesis_block()]
    previous_block = blockchain[0]
    for i in range(0, number_of_blocks):
        block_to_add = next_block(previous_block)
        blockchain.append(block_to_add)
        previous_block = block_to_add
    print("CSV successfully converted to blockchain")
    return blockchain


# Run to save all current Blockchain Hashcodes
def Save_hashcodes(blockchain, genesis_hash):
    if blockchain[0].hash == genesis_hash:
        file = open(os.path.join(PARENT_DIR, "blockchain.txt"), "w")
        for i in range(0, len(blockchain)):
            hash_i = blockchain[i].hash
            file.write(
                """%s
            """
                % hash_i
            )
        file.close()
    else:
        Return_hashcodes(blockchain)
    return


# Return Hashcodes from first run to blocks
def Return_hashcodes(blockchain):
    file = open(os.path.join(PARENT_DIR, "blockchain.txt"), "r")
    text = file.readlines()
    file.close()
    for i in range(0, len(blockchain)):
        blockchain[i].hash = text[i].strip()
    for i in range(1, len(blockchain)):
        blockchain[i].previous_hash = text[i - 1].strip()
    file.close()
    return


# Validate the blockchain & the original_genesis_hash should be used before saved out to txt
def validate_blockchain(in_blockchain, original_genesis_hash):
    if in_blockchain[0].hash != original_genesis_hash:
        print("Blockchain is invalid!")
    else:
        for current_position in range(1, len(in_blockchain)):
            previous_position = current_position - 1
            if (
                in_blockchain[previous_position].hash
                == in_blockchain[current_position].previous_hash
            ):
                i = 1
            else:
                print(
                    "Block %d is invalid! (%s)"
                    % (current_position, repr(in_blockchain[current_position]))
                )
                i = 2
                break

        if i == 1:
            val = "Blockchain Valid"
        else:
            val = "Blockchain Invalid"
    return val


# Query the Blockchain for specific strings
def Query_BC(blockchain, subs):
    subs = subs.upper()
    new_bc = [str(i) for i in blockchain]
    res = list(filter(lambda x: subs in x, new_bc))

    Index = []
    Index.clear()
    Hashcodes = []
    Hashcodes.clear()
    Street_name = []
    Street_name.clear()
    Gor_name = []
    Gor_name.clear()
    Gee_name = []
    Gee_name.clear()
    pre_hash = []
    pre_hash.clear()
    hashh = []
    hashh.clear()

    for i in res:
        txt = i
        end = txt.find("\n")
        Index.append(txt[7 : end - 1])
        print(Index)
    for i in Index:
        int_i = int(i)
        Street_name.append("%s" % str(blockchain[int_i].street_name))
        Gor_name.append(
            "%s %s"
            % (
                str(blockchain[int_i].guarantor_fname),
                str(blockchain[int_i].guarantor_lname),
            )
        )
        Gee_name.append(
            "%s %s"
            % (
                str(blockchain[int_i].guarantee_fname),
                str(blockchain[int_i].guarantee_lname),
            )
        )
        pre_hash.append("%s" % str(blockchain[int_i].previous_hash))
        hashh.append("%s" % str(blockchain[int_i].hash))

    df = pd.DataFrame()
    df["Block Index"] = Index
    df["Address"] = Street_name
    df["Guarantor Name"] = Gor_name
    df["Guarantee Name"] = Gee_name
    df["Previous Hash Code"] = pre_hash
    df["Hash Code"] = hashh

    df = df.to_dict("records")
    return df, len(Index)


# Add a user input into the Blockchain
def user_block(
    blockchain,
    street_name,
    consideration,
    town_code,
    guarantor_lname,
    guarantor_fname,
    guarantee_lname,
    guarantee_fname,
    file,
):
    # file = File_to_string(last_block.index + 1)
    # Define attributes and format correctly
    index = len(blockchain)
    last_block = blockchain[index - 1]
    this_index = last_block.index + 1
    this_timestamp = date.datetime.now()
    this_str_name = street_name
    this_date = str(this_timestamp)[:10]
    this_consideration = consideration
    this_town_code = town_code
    this_guarantor_lname = guarantor_lname
    this_guarantor_fname = guarantor_fname
    this_guarantee_lname = guarantee_lname
    this_guarantee_fname = guarantee_fname
    this_signed_doc = file
    this_hash = last_block.hash

    # Create Block
    new = Block(
        this_index,
        this_timestamp,
        this_str_name,
        this_date,
        this_consideration,
        this_town_code,
        this_guarantor_lname,
        this_guarantor_fname,
        this_guarantee_lname,
        this_guarantee_fname,
        this_signed_doc,
        this_hash,
    )

    # Add new block to blockchain
    blockchain.append(new)

    # Save all hashcodes including new block
    Save_hashcodes(blockchain, blockchain[0].hash)

    # Add new row to data CSV
    New_row = [
        this_str_name,
        "office",
        this_timestamp,
        "doc_num",
        "volm",
        "page",
        this_consideration,
        this_town_code,
        this_guarantor_lname,
        this_guarantor_fname,
        this_guarantee_lname,
        this_guarantee_fname,
        this_signed_doc,
    ]

    with open(
        os.path.join(PARENT_DIR, os.path.join(PARENT_DIR, "RegistryDataset.csv")),
        "a",
        newline="",
    ) as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(New_row)
        f_object.close()

    validate_blockchain(blockchain, blockchain[0].hash)
    return new


# ----------------------------Creation of Blockchain----------------------------

# Import registry dataset
df_Registry, number_of_blocks = Import_Dataset(
    os.path.join(PARENT_DIR, os.path.join(PARENT_DIR, "RegistryDataset.csv"))
)

# Creates the blockchain
blockchain = Add_blocks_from_CSV(number_of_blocks)

# For prototype - we save the hashcodes so every time the code is run, the same blockchain is created
Save_hashcodes(blockchain, genesis_hash)

# Blockchain validation
val = validate_blockchain(blockchain, genesis_hash)
print(val)

# Code to break the blockchain
# blockchain.pop(20)
# val = validate_blockchain(blockchain,genesis_hash)

# ----------------------------Creation of Flask App----------------------------

from flask import Flask, render_template, request, redirect

app = Flask(__name__, static_folder="static", template_folder="static/templates")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/index.html")
def index():
    return render_template("index.html")


@app.route("/form.html")
def form():
    return render_template("form.html")


@app.route("/SearchBlocks.html")
def SearchBlocks():
    return render_template("SearchBlocks.html")


@app.route("/AboutUs.html")
def AboutUs():
    return render_template("AboutUs.html")


@app.route("/form.html", methods=["POST", "GET"])
def add_Block():
    guarantor_fname = request.form.get("guarantor_fname")
    guarantor_lname = request.form.get("guarantor_lname")
    guarantee_fname = request.form.get("guarantee_fname")
    guarantee_lname = request.form.get("guarantee_lname")
    address = request.form.get("address")
    city = request.form.get("city")
    consideration = request.form.get("consideration")
    fake_file = "no file given"

    val = validate_blockchain(blockchain, blockchain[0].hash)

    if val == "Blockchain Valid":
        new = user_block(
            blockchain,
            address,
            consideration,
            city,
            guarantor_lname,
            guarantor_fname,
            guarantee_lname,
            guarantee_fname,
            fake_file,
        )

        result = {
            "Hash Code": new.hash,
            "Index": new.index,
            "Address": new.street_name,
            "Grantor FName": new.guarantor_fname,
            "Grantor LName": new.guarantor_lname,
            "Grantee FName": new.guarantee_fname,
            "Grantee LName": new.guarantee_lname,
            "Previous Hash Code": new.previous_hash,
        }
    else:
        result = "null"

    val = validate_blockchain(blockchain, blockchain[0].hash)

    return render_template("add_block_results.html", result=result, val=val)


@app.route("/SearchBlocks.html", methods=["POST", "GET"])
def search_Blocks():
    user_input = request.form.get("search_input")
    df, count = Query_BC(blockchain, user_input)
    val = validate_blockchain(blockchain, blockchain[0].hash)
    return render_template("query_results.html", df=df, count=count, val=val)


if __name__ == "__main__":
    app.run(debug=True)
