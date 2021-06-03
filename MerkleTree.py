from merkletools import MerkleTools


def create_merkle_tree(data1, data2, data3, data4):
    merkle_tree = MerkleTools()
    merkle_tree.add_leaf(data1, True)
    merkle_tree.add_leaf(data2, True)
    merkle_tree.add_leaf(data3, True)
    merkle_tree.add_leaf(data4, True)
    merkle_tree.make_tree()
    return merkle_tree


def validate(target_hash, merkle_tree):
    print('Student name hash: ' + merkle_tree.get_leaf(0))  # student_name
    print('Student number hash: ' + merkle_tree.get_leaf(1))  # student_number
    print('Student education hash: ' + merkle_tree.get_leaf(2))  # education
    print('Student pdf hash: ' + merkle_tree.get_leaf(3))  # pdf_hash

    return merkle_tree.validate_proof(merkle_tree.get_proof(3), target_hash, merkle_tree.get_merkle_root())
