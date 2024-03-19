from database import Database
from helper.writeAJson import writeAJson

db = Database(database="mercado", collection="compras")

class ProductAnalyzer:

    def __init__(self, db):
        self.db = db

    
    def run_analysis(self):
    
        result = db.collection.aggregate([
            {"$unwind": "$produtos"},
            {"$group": {"_id": "$data_compra", "totalDeVendas": {"$sum": "$produtos.quantidade"}}},
            {"$sort": {"total": -1}}
        ])

        writeAJson(result, "Total de vendas por dia")

        result = db.collection.aggregate([
            {"$unwind": "$produtos"},
            {"$group": {"_id": "$produtos.descricao", "totalVendido": {"$sum": "$produtos.quantidade"}}},
            {"$sort": {"totalVendido": -1}},
            {"$limit": 1},
            {"$project": {"_id": 1, "totalVendido": 1}},
        ])

        writeAJson(result, "Produto mais vendido em todas as compras")

        result = db.collection.aggregate([
            {"$unwind": "$produtos"},
            {"$group": {"_id": "$cliente_id", "gastos": {"$sum": {"$multiply": ["$produtos.quantidade", "$produtos.preco"]}}}},
            {"$sort": {"gastos": -1}},
            {"$limit": 1}
        ])

        writeAJson(result, "Cliente que mais gastou em uma única compra")

        result = db.collection.aggregate([
            {"$unwind": "$produtos"},
            {"$match": {"produtos.quantidade": {"$gt": 1}}},
            {"$group": {"_id": "$produtos.descricao", "totalVendido": {"$sum": "$produtos.quantidade"}}},
            {"$sort": {"totalVendido": -1}},
            {"$project": {"_id": 1, "totalVendido": 1}},
        ])

        writeAJson(result, "Todos os produtos que tiveram quantidade vendida acima de 1 unidade")