#/usr/bin/python3
# 
# erc1337 Coffee
# 
# Made with love for Dman on ApeReunion's discord :)
import asyncio
from web3 import Web3, IPCProvider, HTTPProvider
import json
from hexbytes import HexBytes

#######################################################################################
# CLASSES
#######################################################################################
class ETH_Node(object):
	"""
	An object used to interact with a RPC node.
	"""
	def __init__(self):
		super(ETH_Node, self).__init__()
		# If you use a custom HTTP provider:
		#self.w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
		# 
		# Else if you want to use Infura as provider for mainnet:
		self.w3 = Web3(HTTPProvider("https://mainnet.infura.io/v3/YOUR_PROJECT_ID"))
		#
		# Or Infura on Rinkeby (testnet):
		#self.w3 = Web3(HTTPProvider("https://rinkeby.infura.io/v3/YOUR_PROJECT_ID"))
		#
		# Link to some documentation about providers: https://web3py.readthedocs.io/en/stable/overview.html#providers
		#
		# Or use a local IPC Provider and provide the path to the ipc file:
		#self.w3 = Web3(Web3.IPCProvider('/tmp/jsonrpc.ipc'))
	def handle_event(self,event):
		try:
			tx_data = dict(event)
			###################
			# Signatures List #
			###################
			# 
			# You can filter the type of tx you want to process by filtering
			# on tx_data["topics"][0] for the wanted signatures.
			#
			# Cancelled order: 0x5152abf959f6564662358c2e52b702259b78bac5ee7842a0f01937e670efcc7d
			# New sale: 0xc4109843e0b7d514e4c093114b863f8e7d8d9a458c372cd51bfe526b588006c9
			# 
			if(tx_data["topics"][0] == HexBytes("0xc4109843e0b7d514e4c093114b863f8e7d8d9a458c372cd51bfe526b588006c9")):

				# If the tx is a sale, gather the full tx data from the blockchain 
				# I only do this to get the 'value' field to know the sale price
				tx = dict(self.w3.eth.getTransaction(tx_data['transactionHash']))

				# Gather the receipt from the blockchain 
				raw_receipt = self.w3.eth.getTransactionReceipt(tx_data['transactionHash'])
				receipt = dict(raw_receipt)

				# My parsing is kinda bad but it's working so who cares
				# It's ok for ERC721, to parse ERC1150 you'll have to tweak a bit as the parameters are
				# not organised the same way 
				collection_address  = receipt["logs"][1]["address"]
				collection 			= self.w3.eth.contract(address=collection_address, abi='[{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"}]')
				collection_name 	= collection.functions.name().call()
				# ERC1150 will have 'Wyvern Exchange Contract' as their name, for this example I skip them
				# Delete this if you want to show ERC1150 sales too
				if(collection_name == "Wyvern Exchange Contract"):
					return
				seller 	 			= "0x" + receipt["logs"][1]["topics"][1].hex()[26:]
				buyer  				= "0x" + receipt["logs"][1]["topics"][2].hex()[26:]
				token_id			= int(receipt["logs"][1]["topics"][3].hex(), 16)
				# Convert Wei to ETH
				# (my parser is not great because it assumes the currency is ETH but there's apecoin & other things on OpenSea)
				price 				= float(tx["value"]/ (10**18))

				# Print all the info about that tx :)
				data = """
----
Tx Hash: %s
Buyer: %s
Seller: %s
Collection: %s (%s)
Token_id: #%s
Price: %sETH
----

				""" % (tx_data['transactionHash'].hex(), buyer, seller, collection_name, collection_address, token_id, price)
				print(data)
		except Exception as err:
			# Ignore exceptions, because that's the best way to deal with errors. If you don't see the error there's no error.
			pass
	async def log_loop(self, event_filter, poll_interval):
		# On new block event, call the handle_event function passing the tx_data as arg, sleep then keep doing this
		while True:
			for event in event_filter.get_new_entries():
				self.handle_event(event)
			await asyncio.sleep(poll_interval)
	def startWorker(self):
		# Subscribe to new block events & only care about tx from Wyvern Contract (would need to add the new Seaport contract but ¯\_(ツ)_/¯)
		block_filter = self.w3.eth.filter({'address':'0x7f268357A8c2552623316e2562D90e642bB538E5','fromBlock':'latest', 'fromBlock':'latest', 'full_transactions':True})
		loop = asyncio.get_event_loop()
		try:
			loop.run_until_complete( asyncio.gather(self.log_loop(block_filter, 2) ))
		finally:
			loop.close()

#######################################################################################
# MAIN
#######################################################################################
def main():
	node = ETH_Node()
	try:
		node.startWorker()
	except Exception as err:
		print(err)

if __name__ == '__main__':
	main()
