import time
from MarketCrawler.MarketSpider import MarketSpider
from MarketCrawler.thread_setup import gatherData
from LinRegEstimation.NN import TrainModel,predict,graphModel,modelMAE
class Menu(object):
	def __init__(self,currency="",thread_amt=4,page_count=1):
		self.__currency = currency
		self.__thread_amt = thread_amt
		self.__page_count = page_count
	def crawl(self):
		gatherData(self.__page_count,self.__thread_amt)
	def createModel(self):
		TrainModel(self.__currency)
	def modelPredict(self,X):
		pred = predict(self.__currency,X)
		if(isinstance(pred,str)):
			print(pred)
		else:
			print("Prediction given current inputs %.5f" % (pred))
	def run(self):
		while(True):
			menuStr = '''
Q: Crawl Pages
R: Choose Currency
W: Set Page Count
E: Set Thread Amount
C: Crawl Specified Currency Page
T: Train Currency Model
Y: Show Currency Model Graph
U: Make Predicitons
A: Show Model Absolute Error

			'''
			print(menuStr)
			menuSelection = input("Select a task to do input N to exit: ").strip()
			if (menuSelection.lower() == "n"):
				print("Thank You for using this! Bye!")
				return
			elif(menuSelection.lower() == "q"):
				self.crawl()
			elif(menuSelection.lower() == "c"):
				MarketSpider.date = {'start':'20120428','end':time.strftime("%Y%m%d")}
				spider = MarketSpider(1,"data/","https://coinmarketcap.com/currencies/"+self.__currency + "/")
				try:
					spider.export_data()
				except ValueError as e:
					print(e)
					continue
			elif(menuSelection.lower() == "w"):
				try:
					newPageCount = int(input("Enter the amount of pages you want to count: ").strip())
				except ValueError:
					print("\nPlease enter a number \n")
					continue
				self.__page_count = newPageCount
			elif(menuSelection.lower() == "e"):
				try:
					newThreadAmt = int(input("Enter the amount of threads you want to use: "))
				except ValueError:
					print("\nPlease enter a number \n")
					continue
				self.__thread_amt = newThreadAmt
			elif(menuSelection.lower() == "r"):
				self.__currency = input("Please type in the name of the currency you want to use: ").lower().strip()
			elif(menuSelection.lower() == "t"):
				self.createModel()
			elif(menuSelection.lower() == "y"):
				graphModel(self.__currency)
			elif(menuSelection.lower() == "u"):
				valuesList = []
				try:
					days_since_release = valuesList.append(int(input("Input the days since " + self.__currency+ " has been released: ")))
					marketOpen = valuesList.append(float(input("Input the current market open price of " + self.__currency + ": ")))
					marketHigh = valuesList.append(float(input("Input the current market high price of "+ self.__currency + ": " )))
					marketLow = valuesList.append(float(input("Input the current market low price of " + self.__currency + ": ")))
					marketClose = valuesList.append(float(input("Input the current market close price of " + self.__currency + ": ")))
					marketVolume = valuesList.append(float(input("Input the current market volume of " + self.__currency + ": ")))
					marketCap = valuesList.append(float(input("Input the current market cap of " + self.__currency + ": ")))
				except ValueError:
					print("\nPlease enter a number \n")
					continue
				self.modelPredict(valuesList)
			elif(menuSelection.lower() == "a"):
				Mae = modelMAE(self.__currency)
				if(isinstance(modelMAE(self.__currency),str)):
					print(Mae)
				else:
					print("Mean Absolute Error of the current model %.5f" %  (Mae[1]))
			
			
if __name__ == "__main__":
	start = Menu()
	start.run()
