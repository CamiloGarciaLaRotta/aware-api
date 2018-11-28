import azure.cosmos.cosmos_client as cosmos_client

'''
    DbClient for connectign to azure cosmos
    Expect Config in the following format
    config = {
        'ENDPOINT': 'FILLME',
        'PRIMARYKEY': 'FILLME',
        'DATABASE': 'CosmosDatabase',
        'CONTAINER': 'CosmosContainer'
    }
'''
class DbClient:
    # Initialize the database
    def __init__(self, config):
        self.config = config
        self.client = cosmos_client.CosmosClient(url_connection=config['ENDPOINT'], auth={
                                    'masterKey': config['PRIMARYKEY']})
        
        # Create a database or fetch it if it exists
        self.db = None
        try:
            self.db = self.client.CreateDatabase({'id': config['DATABASE']})
        except:
            self.db = next((data for data in self.client.ReadDatabases() if data['id'] == config['DATABASE']))

        # Create container options
        options = {
            'offerThroughput': 400
        }

        container_definition = {
            'id': config['CONTAINER']
        }

        # Create a container
        self.container = None
        try:
            self.container = self.client.CreateContainer(self.db['_self'], container_definition, options)
        except:
            self.container = next((data for data in self.client.ReadContainers(self.db['_self']) if data['id'] == config['CONTAINER']))
    
    # Query per ID
    def GetItemById(self, id):
        result_iterable = self.client.QueryItems(self.container['_self'], 'SELECT * FROM c WHERE c.id = "123"')
        for item in iter(result_iterable):
            return item

    # Creates a new Item
    def CreateItem(self, dbEntry):
        return self.client.CreateItem(self.container['_self'], dbEntry)

    # Upsert an Item
    def UpsertItem(self, dbEntry):
        return self.client.UpsertItem(self.container['_self'], dbEntry)

    # Delete an Item
    def DeleteItem(self, dbEntry):
        return self.client.DeleteItem(dbEntry['_self'])

    # Query by a specific query
    def GetItemsByQuery(self, query):
        return self.client.QueryItems(self.container['_self'], query)
