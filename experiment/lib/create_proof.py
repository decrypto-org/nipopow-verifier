import argparse

def import_proof(filename='proof.pkl'):
    import pickle
    pickle_in = open(filename,'rb')
    proof = pickle.load(pickle_in)
    return proof

def create_proof(blocks=450000, filename='proof.pkl'):
    import pickle
    import create_blockchain_new as blockchain_utils
    header, headerMap, mapInterlink = blockchain_utils.create_blockchain(blocks=blocks)
    proof = blockchain_utils.make_proof(header, headerMap, mapInterlink)
    pickle_out = open(filename, 'wb')
    pickle.dump(proof, pickle_out)
    pickle_out.close()
    print("Proof was written in " + filename)
    return proof

def make_proof_file_name(blocks):
    return str('../proofs/proof_'+str(blocks)+'.pkl')

def get_proof(blocks):
    proof_file_name = make_proof_file_name(blocks)
    f = None
    try:
        f = open(proof_file_name)
        print('File', proof_file_name, 'already exists. Importing...')
        proof = import_proof(proof_file_name)
        f.close()
    except IOError:
        print('File', proof_file_name, 'does not exist. Creating...')
        proof = create_proof(blocks, proof_file_name)
    finally:
        print('...ok')

    return proof

def create_mainproof_and_forkproof(mainblocks, fork_index, forkblocks):
    import create_blockchain_new as blockchain_utils
    header, headerMap, mapInterlink = blockchain_utils.create_blockchain(blocks=mainblocks)
    proof = get_proof(mainblocks)
    header_f, headerMap_f, mapInterlink_f = blockchain_utils.create_fork(header,
                                                     headerMap,
                                                     mapInterlink,
                                                     fork=fork_index,
                                                     blocks=forkblocks)

    proof_f = blockchain_utils.make_proof(header_f, headerMap_f, mapInterlink_f)

    import pickle
    pickle_out = open(make_proof_file_name(mainblocks), 'wb')
    pickle.dump(proof, pickle_out)
    pickle_out.close()

    pickle_out = open('../proofs/'+str(fork_index)+'_fork_of_proof_'+str(mainblocks)+'.pkl', 'wb')
    pickle.dump(proof_f, pickle_out)
    pickle_out.close()

    return proof, proof_f

def main():
    parser=argparse.ArgumentParser(description='Create and store proof from create_blockchain_new.py')
    parser.add_argument('--blocks', required=True, type=int, help='Number of blocks')
    args=parser.parse_args()
    blocks=args.blocks
    proof=get_proof(blocks)
    print('Proof size:', len(proof))

if __name__ == "__main__":
    main()