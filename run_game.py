import table
import gameFlow
import model

#gameFlow.gameloop(table.Table())
table = table.Table()
model = model.HanabiModel(table.deck, table.player_list)
gameFlow.gameloop(table)