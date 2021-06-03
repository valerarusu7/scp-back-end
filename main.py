from flask import Flask, request
from Blockchain import Blockchain
import json
from MerkleTree import create_merkle_tree, validate
from flask_cors import CORS
import hashlib
from utils import generate_pdf, get_hash_of_pdf
from flask_mail import Message, Mail

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USERNAME='viatestemail2021@gmail.com',
    MAIL_PASSWORD='via2021!testemail',
    MAIL_USE_TLS=False,
    MAIL_USE_SSL=True,
)
mail = Mail(app)
CORS(app)
blockchain = Blockchain()


@app.route("/blockchain", methods=['GET'])
def chain():
    if request.method == 'GET':
        chain_data = []
        for block in blockchain.blocks:
            new_block = {"index": block.index,
                         "timestamp": block.timestamp,
                         "data": block.data,
                         "previous_hash": block.previous_hash,
                         "nonce": block.nonce,
                         "hash": block.hash}
            chain_data.append(new_block)
        return json.dumps({"length": blockchain.get_chain_size(),
                           "chain": chain_data})


@app.route("/add-block", methods=['POST'])
def add_block():
    success = False
    if request.method == 'POST':
        json_data = request.json
        merkle_root = None
        block_id = None
        key = hashlib.sha256()
        key.update(str(json_data['student_name']).encode('utf-8'))
        key.update(str(json_data['student_number']).encode('utf-8'))
        key.update(str(json_data['education']).encode('utf-8'))
        if key.hexdigest() == json_data['hash']:
            block_id = str(blockchain.get_chain_size() + 1)
            generate_pdf(json_data=json_data)
            pdf_hash = get_hash_of_pdf(json_data['student_number'] + '.pdf')
            print('Created pdf hash: ' + pdf_hash)
            merkle_tree = create_merkle_tree(json_data['student_name'], json_data['student_number'],
                                             json_data['education'], pdf_hash)
            blockchain.add_block(data=merkle_tree.get_merkle_root(), merkle_tree=merkle_tree)
            merkle_root = merkle_tree.get_merkle_root()
            if blockchain.verify() is not False:
                msg = Message("Congratulation for graduating from VIA University College, have a wonderful life!",
                              sender="viatestemail2021@gmail.com",
                              recipients=[json_data['student_number'] + '@via.dk'])
                file_name = json_data['student_number'] + '.pdf'
                with app.open_resource(file_name) as fp:
                    msg.attach(file_name, "application/pdf", fp.read())
                mail.send(msg)

                success = True
        return {'success': success, 'data': merkle_root, 'index': block_id}


@app.route("/validate-diploma", methods=['POST'])
def validate_diploma():
    if request.method == 'POST':
        file = request.files['file']
        file_hash = hashlib.sha256(file.read()).hexdigest()
        print('Received file hash: ' + file_hash)
        double_hash = hashlib.sha256()
        double_hash.update(str(file_hash).encode('utf-8'))
        print('Received file double hash: ' + double_hash.hexdigest())
        is_valid = False
        for block in blockchain.blocks:
            if block.index != 0:
                merkle_tree = blockchain.blocks[block.index].merkle_tree
                is_valid = validate(target_hash=double_hash.hexdigest(), merkle_tree=merkle_tree)
                if is_valid is not False:
                    break
        return {'is_valid': is_valid}


if __name__ == "__main__":
    app.run(host='127.0.0.1', port='5000')
