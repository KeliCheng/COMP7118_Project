
class User(object):
	"""docstring for User"""
	def __init__(self, u_id):
		self.u_id = u_id
		self.ratings = {}
		self.blacklist = []
		self.whitelist = []

		self.timestamps = {}


