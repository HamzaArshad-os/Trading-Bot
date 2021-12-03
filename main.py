"""
README

First Github repository of a Project , This is my first time creating a project and putting it on the
internet for the world to see .so sorry if i didn't set stuff up properply in github, this is also my first
project in Python. So excuse  bad coding habits etc:..

This is a set of tools .Non API based that can be used to automate trading on the Libertex trading platform
that at the date of writing this 18/11/2020 does not have an API . This is  a Selenium based alternative

Some of the tools included in this source code are included below. More detail of requirements and Importance of not
changing parts of this source will be explained later ..Basically i suffered writing this code so you dont have to :)


.Accessing the platform  trading website.
.Logging into your account
.Accessing the Demo Account. To not go to the demo account simply comment its calling in bootup1()
.Accessing your specific list of trades that are already opened in your account.
.Opening each of your trades in its own tab ..Yes Ram demanding but Selenium is slightly limiting in some places and this is the
    best way to do it that i could figure out .
.From the code provided here more or less full safety in the sense that all errors that i could find will be recognised and resolved.
.Get data of each trade including
    .BoughtPrice
    .Live Price/Current Price
    .Amount Invested
    .Multiplier Value
    .Current Profit/Loss
    .Trade direction
    .Commsission total
    .Set and Edit the SL value
    .Special Number ..explained later on
    .Reboots the entire program after x amount of time to decrease the chance of depleting
        functionality(Dont know if this is a real thing but the program works better as it
        is designed to run for long periods of time if it is rebooted every now and then.)
    .If trading hours or not for the specific trade
    .If trade has closed
    .If new trades has been opened
    .Setting the Stop Loss Value ..Price based

Other Functionality includes
    .I have left some code that can partially open a trade for you .. In the sense set the Invest Amount, Multiplier Value
        but if you would like that full functionality it will have to be done by yourself ..Add it to the repository if you would like.
        SetupTrade(),triggershort(),triggerlong()

The basic architecture of the program is as proceeds.

Upon running program.
Bootup1()-->Accesses the trading platform in your browser,
            Logs in for you

            Transfers to Demo Acc (Defualt, Comment out the call if want to run program on real account)

            Reads all currently opened trades

            Sets the first tab as a control tab that is returned to here and there to check for data such as new trades

            1!. Open a trades details in its own tab at a time.

                Gets the data required ..Including the special number

                    The special number being how close you can set the SL value to the current price.For a visual explanation
                    Have a trade open and Set the SL to something extreme like ....9999999999 and click anywhere in the white area.
                    A red box with  white writing will show you.

                All this data is stored in a list for each trade.Originally i did do it using a db so it wasnt volatile.

                But i did not have much experience with db's and failed with it.,after careful consideration i transferred the system onto a mySQL db

                The same is done for each trade.

                For each trade this can take upto 10-40 seconds to open the tab ,extract the data.around 20 seconds+ if you want
                    to  set the stop Loss intantly upon the program detecting a new trade

            Once a tab has been opened for each opened trade.

                The Trading Logic subroutine is entered (This is an infinite loop tecnically)

                    Here you can implement your own tecnique, strategy  for trading (I have removed mine because it is my own
                    personal strategy) after each index to trade,reading data , update if required and running your strategy.A
                    check is done for if any new trades have been created .. if so then the program will return to point 1!.
                    and open a tab for it . After it has done so it proceeds with the traidng logic loop.

                    If after indexing to a trade and the trade is closed ...the program can detect that the trade is closed
                    and remove it from the list of trades and db, and close the tab . Of course you can change this to do something else

                    After x amount of time defined by time_end The program will reboot starting from the beginning.each tme it restarts it will 
                    crosscheck the db to see if the data already exists




"""











import itertools
import random
import sqlite3

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import undetected_chromedriver as uc







def ScrollingVisibleList(i):
    driver1.execute_script("arguments[0].scrollIntoView()", driver1.find_element(By.CSS_SELECTOR,
                                                                                 ".visible-list > .row:nth-child(" + str(
                                                                                     i) + ")> .investment-item"))
    print("Scrolling to " + str(i) + "in Visible list")

def Clickonindexedtradevisible(i):
    try:
        driver1.find_element(By.CSS_SELECTOR,
                             ".visible-list > .row:nth-child(" + str(i) + ")> .investment-item").click()

    except:
        print("Visiblelist limit reached")

def ScrollingOverflowlist(i):

    print("Scrolling to "+str(i)+"in Overflow list")
    driver1.execute_script("arguments[0].scrollIntoView()", driver1.find_element(By.XPATH,
                      "//body/div[1]/aside[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[5]/div[1]/div[2]/div["+str(i)+"]/div[1]"))

def ClickonindexedtradeOverflow(i):

    driver1.find_element(By.XPATH,"//body/div[1]/aside[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[5]/div[1]/div[2]/div["+str(i)+"]/div[1]").click()

def FirstTab():
    print("Opening first tab")
    driver1.get("https://app.libertex.com/")
    driver1.maximize_window()

def Wait(SelectorType,Selector):

    if SelectorType =="CSS":
        try:
            WebDriverWait(driver1, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, Selector)))

        except:
            Refeshpage()

    if SelectorType =="XPATH":
        try:
            WebDriverWait(driver1, 10).until(EC.presence_of_element_located((By.XPATH, Selector)))
        except:
            if driver1.current_url.__contains__("#modal_news"):

                driver1.find_element(By.XPATH,"//span[@class='fake-dialog-close']").click()
                print("worked in closing the dialog #DowJonespopup")
                time.sleep(5)

            Refeshpage()
            time.sleep(2)

    if SelectorType =="ID":
        try:
            WebDriverWait(driver1, 10).until(EC.presence_of_element_located((By.ID, Selector)))
        except:
            Refeshpage()
    time.sleep(0.5)

def login():
    Wait("CSS", "#login-field")
    # Email field
    driver1.find_element(By.CSS_SELECTOR, "#login-field").send_keys("EMAIL")  # works,keep
    # PasswordField
    driver1.find_element(By.CSS_SELECTOR, "#password-field").send_keys('Password')  # woks,keep
    # Press Log in submit button
    Wait(".buttons > .a-btn-blue", ".buttons > .a-btn-blue")
    driver1.find_element(By.CSS_SELECTOR, ".buttons > .a-btn-blue").click()
    print("Login complete")

def TransfertoDemoACC():
    Wait("XPATH", "//span[@class='ui-selectmenu-text selected real-account-select']")
    driver1.find_element(By.XPATH, "//span[@class='ui-selectmenu-text selected real-account-select']").click()
    driver1.find_element(By.CSS_SELECTOR, "#choose-account-select-menu").click()
    Wait("XPATH","/html[1]/body[1]/div[1]/div[3]/div[1]/div[2]/div[1]/div[2]/div[1]/span[1]")
    driver1.find_element(By.XPATH, "/html[1]/body[1]/div[1]/div[3]/div[1]/div[2]/div[1]/div[2]/div[1]/span[1]").click()
    print("DemoACC complete")

def GetInvestReportURL():
    URL = driver1.current_url
    return URL

def Gettradedirection():
    Wait("XPATH","//dt[contains(text(),'Operation:')]")
    Direction = driver1.find_element(By.XPATH, "//dt[contains(text(),'Operation:')]").text
    Direction = str(Direction).lstrip("Operation: to ")
    print("The direction of this trade is "+Direction)
    return Direction

def GetInvestAmount():
    InvestAmount =  driver1.find_element(By.XPATH,("//body/div[1]/div[3]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/dl[1]/dd[3]")).text
    InvestAmount = str(InvestAmount).replace(" ","").lstrip("£")
    print("The Invest Amount of this trade is "+ str(InvestAmount))
    return InvestAmount

def GetMultiplierAmount():
    MultiplierValue = driver1.find_element(By.XPATH,("/html[1]/body[1]/div[1]/div[3]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/dl[1]/dd[4]/span[1]")).text
    print("The Multiplier Value  Amount of this trade is "+ str(MultiplierValue))
    return MultiplierValue

def GetboughtPrice():
    Boughtprice =driver1.find_element(By.XPATH,("//dd[@class='col-startRate']")).text
    BoughtPrice = str(Boughtprice).replace(" ", "")
    print("The Bought price  of this trade is "+ str(BoughtPrice))
    return BoughtPrice

def GettingcurrentProfitLoss():
    Wait("XPATH","//span[@class='usd']")
    Profitlossv1 = driver1.find_element(By.XPATH,("//span[@class='usd']")).text
    ProfitlossV1 = (str(Profitlossv1).replace("£","").replace(" ",""))
    Profitloss = ProfitlossV1
    return Profitloss

def Getcomission():
    Wait("XPATH","//label[contains(text(),'Commissions and reports')]")
    driver1.find_element(By.XPATH,"//label[contains(text(),'Commissions and reports')]").click()
    TotalCommsion = driver1.find_element(By.XPATH, "//dd[@class='col-commissionTotal']").text
    driver1.find_element(By.XPATH, "//label[contains(text(),'General information')]").click()#returning to the other slide
    TotalCommsion =(str(TotalCommsion).lstrip("-"))
    print(TotalCommsion)

    return TotalCommsion

def Checkiftradinghours():

    driver1.find_element(By.XPATH, "//span[@class='a-btn a-btn-neg invest-close']").click()

    try:
        try:
            print(driver1.find_element(By.XPATH, "//h4[contains(text(),'Trade position closing')]").text)
            print("Cannot do trading yet market is closed")
            time.sleep(1)
            driver1.find_element(By.XPATH, "//span[@class='a-event back-to-report']").click()
            return False
        except Exception as e:


            time.sleep(1)
            print("Can do trading on this instrument as market is open")
            driver1.find_element(By.XPATH, "//span[@class='a-btn a-btn-trans ty-cancel']").click()
            return True
    except:
        print("Low inactivity error")
        return False

def GetMSL():

    A = (driver1.find_element(By.XPATH, "//div[@class='limit-spoiler']").get_attribute("style"))
    if A == "display: none;":
        driver1.find_element(By.XPATH, ("//div[@class='limit-link']")).click()
    try:
        Wait("XPATH", "//div[@class='modal-wrap modal-to-left']//label[3]")
        time.sleep(1)
        driver1.find_element(By.XPATH, "//div[@class='modal-wrap modal-to-left']//label[3]").click()
    except:
        print()
    time.sleep(1)
    A = driver1.find_element(By.XPATH, ("//span[@id='stopLossPriceProfit']")).text


    if str(A).__contains__("£"):
        # SL has been set
        B = str(A).replace("≈", "")
        B = str(B).replace("£", "")
        B = str(B).replace(" ", "")
        old = B

        print(old)
        return str(old)
    else:
        return str(-1)

def SetandeditRealSL(WantedSL,LP):
    print("FJ")
    print(LP)
    print(WantedSL)
    WantedSL = str(WantedSL)
    if LP.__contains__("."):
        print()
        WantedSL = WantedSL
    else:
        split = str(WantedSL).split(".")
        WantedSL = str(split[0])
        print("RJNGJE")
    print(WantedSL)
    print("Fudge")




    Wait("XPATH", "//div[@class='limit-spoiler']")
    A = (driver1.find_element(By.XPATH, "//div[@class='limit-spoiler']").get_attribute("style"))
    if A == "display: none;":
        try:
            driver1.find_element(By.XPATH, ("//div[@class='limit-link']")).click()
        except:
            print("QDFGHHRdee")

    A = driver1.find_element(By.XPATH, ("//span[@id='stopLossPriceProfit']")).text
    C = None
    if str(A).__contains__("£"):
        C = True
    else:
        C = False

    print(str(C))
    if C == False:
        try:
            driver1.find_element(By.XPATH,"//body/div[1]/div[3]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]").click()
        except:
            print("tfsjnymssu")
        try:
            driver1.find_element(By.XPATH,
                                 "//body/div[1]/div[3]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/form[1]/div[2]/dl[3]/dt[2]/label[1]").click()

        except:
            print("problem")
    print("fdf")
    print(str(C))

    Wait("XPATH", "//input[@id='stopLossPrice']")
    driver1.find_element(By.XPATH, ("//input[@id='stopLossPrice']")).click()
    driver1.find_element(By.XPATH, ("//input[@id='stopLossPrice']")).clear()
    driver1.find_element(By.XPATH, ("//input[@id='stopLossPrice']")).send_keys(WantedSL)

    A = driver1.find_element(By.XPATH, ("//span[@id='stopLossPriceProfit']")).text
    B = str(A).replace("≈", "")
    B = str(B).replace("£", "")
    B = str(B).replace(" ", "")
    Wait("XPATH", "//div[@class='limit-spoiler']")
    driver1.find_element(By.XPATH, "//div[@class='limit-spoiler']").click()
    print("hgdtgs")
    try:
        driver1.find_element(By.XPATH, "//span[@class='a-btn a-btn-trans limits-save']").click()
    except:
        print("tydjs")
        try:
            driver1.find_element(By.XPATH, "//span[@class='a-btn a-btn-trans limits-save']").click()
        except:
            Refeshpage()
            print()


    print("Completed SL edit")


def CloseLPtab():
    Wait("XPATH","//div[@class='limit-spoiler']")
    A = (driver1.find_element(By.XPATH, "//div[@class='limit-spoiler']").get_attribute("style"))
    if A != "display: none;":
        try:
            driver1.find_element(By.XPATH, ("//div[@class='limit-link']")).click()
        except:
            print()

def Refeshpage():
    driver1.refresh()

def Aforfirst():
    driver1.switch_to.window(driver1.window_handles[0])
    print("Attempting to setup host tab/first tab")
    if driver1.current_url != "https://app.libertex.com/":
        try:
            driver1.get("https://app.libertex.com/")
        except:
            print()
    try:
        Wait("XPATH","//span[@class='a-event']")
        driver1.find_element(By.XPATH, "//span[@class='a-event']").click()
    except:
        print()
    try:
        driver1.find_element(By.XPATH,
                             "//button[@class='ui-button ui-corner-all ui-widget ui-button-icon-only ui-dialog-titlebar-close']").click()
        print("Setting up or indexing  first tab succeded")
    except:
        print("error here Aforfirst")

def Getthespecialnumber(Direction):

    Extremebuy = "2000000"
    Extremesell = "0.1"

    if Direction =="buy":
        WantedSL = Extremebuy
    if Direction == "sell":
        WantedSL = Extremesell
    Wait("XPATH","//div[@class='limit-spoiler']")
    A = (driver1.find_element(By.XPATH,"//div[@class='limit-spoiler']").get_attribute("style"))
    if A== "display: none;":
        try:
            driver1.find_element(By.XPATH, ("//div[@class='limit-link']")).click()
        except:
            print("Can access Trade MSL data")
    try:
        Wait("XPATH", "//div[@class='modal-wrap modal-to-left']//label[3]")
        time.sleep(1)
        driver1.find_element(By.XPATH, "//div[@class='modal-wrap modal-to-left']//label[3]").click()
    except:
        print()
    try:
        Wait("XPATH", "//div[@class='modal-wrap modal-to-left']//label[3]")
        time.sleep(1)
        driver1.find_element(By.XPATH, "//div[@class='modal-wrap modal-to-left']//label[3]").click()
    except:
        print()
    try:
        driver1.find_element(By.XPATH, "//div[@class='limit-spoiler']").click()
        Wait("ID", "stopLossPrice")
        driver1.find_element(By.ID, ("stopLossPrice")).click()
        driver1.find_element(By.ID, ("stopLossPrice")).clear()
        driver1.find_element(By.ID, ("stopLossPrice")).send_keys(WantedSL)


        driver1.find_element(By.XPATH, "//dl[@class='limit-unit-box limit-unit-rate']").click()
        print(Direction)
        Wait("XPATH",
             "/html[1]/body[1]/div[1]/div[3]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/form[1]/div[2]/dl[3]/dd[2]/div[2]/span[1]")
        themagicnum = driver1.find_element(By.XPATH,
                                           "/html[1]/body[1]/div[1]/div[3]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/form[1]/div[2]/dl[3]/dd[2]/div[2]/span[1]").text

    except:
        driver1.find_element(By.XPATH, ("//body/div[1]/div[3]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/form[1]/div[2]/dl[3]/dt[2]/label[1]")).click()

        Wait("ID", "stopLossPrice")

        driver1.find_element(By.ID, ("stopLossPrice")).click()
        driver1.find_element(By.ID, ("stopLossPrice")).clear()
        driver1.find_element(By.ID, ("stopLossPrice")).send_keys(WantedSL)


        driver1.find_element(By.XPATH, "//dl[@class='limit-unit-box limit-unit-rate']").click()
        print(Direction)

        Wait("XPATH",
             "/html[1]/body[1]/div[1]/div[3]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/form[1]/div[2]/dl[3]/dd[2]/div[2]/span[1]")
        themagicnum = driver1.find_element(By.XPATH,
                                           "/html[1]/body[1]/div[1]/div[3]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/form[1]/div[2]/dl[3]/dd[2]/div[2]/span[1]").text

    print(themagicnum)
    print("wtf")



    try:
        driver1.find_element(By.XPATH, ("//dl[@class='limit-unit-box limit-unit-rate']//dt[2]//label[1]")).click()
    except:
        print()
    #Refeshpage()

    return float(themagicnum)

def Checkiftradestillpresent(Data):
    C = None
    try:
        time.sleep(1)
        C= driver1.find_element(By.XPATH,
                              "//span[@class='a-btn a-btn-blue new-invest']").is_displayed()
        C= True
        print("Trade is closed")
    except:
        print("This trade not closed")

    print(C)
    if C ==True:



        URL = driver1.current_url
        for i in Globallist:
            print()
            if str(i).__contains__(driver1.current_url):
                Globallist.remove(i)


        try:
            Alreadyappendedtrades.remove(URL)
        except:
            print()

        print("Deleted closed trades tab")
        deletetradefromdb(Data)
        Setupnewtrade(Data)
        return True



    else:
        print("Trade not closed yet do not need to close tab")
        return False



def Nums():
    global MSLnum,VSLnum

    MSLnum = 800
    VSLnum = 850
    #MSLnum = 300
    #VSLnum = 400










def TradingLogic(traddetails):
    splitteddata = traddetails.split("|")
    URL = str(splitteddata[0])
    print(traddetails)
    print("Poort")

    try:
        global Alreadyappendedtrades
        if Alreadyappendedtrades.__contains__(URL):
            # Aforfirst()
            Indextocorrecttab(URL)
            print(URL)
            time.sleep(1)

            Direction = splitteddata[1]
            # I = splitteddata[2]
            I = GetInvestAmount()
            MV = splitteddata[3]

            BP = splitteddata[5]
            oldVarSL = splitteddata[8]
            CP = float(GettingcurrentProfitLoss())
            Commision = 0
            if I > splitteddata[2]:
                Commision = Getcomission()
            else:
                Commision = splitteddata[12]
            Commision = float(Commision)
            oldMaxSL = splitteddata[7]
            Name = splitteddata[9]
            Specialnumber = splitteddata[10]
            partialnewtradeurl = splitteddata[11]
            tobecut = splitteddata[13]

            NewMaxSL = 0
            NewVarSL = 0

            if Direction == "buy":
                NewMaxSL = -2000000000
                NewVarSL = -2000000000
            if Direction == "sell":
                NewMaxSL = 2000000000
                NewVarSL = 2000000000

            AllowtomoveMSL = False

            BP = float(BP)
            MV = float(MV)
            I = float(I)

            oldVSL = float(oldVarSL)
            # LPstr = GetLP(URL)
            # LP = float(LPstr)
            LP = 0
            if Direction == "buy":
                LP = ((CP + Commision) * BP) / (MV * I) + BP
            if Direction == "sell":
                LP = BP * (1 - (CP + Commision) / (I * MV))

            print(LP)

            print("TL succeeded claculating LP")

            if tobecut == "T":
                split = str(LP).split(".")
                LP = str(split[0])
                print("RJNGJE")
            else:
                print("Do not need to be cut")
            LPstr = str(LP)
            LP = float(LP)

            Nums()
            # global MSLnum, VSLnum
            # MSLnum = int(input())
            # VSLnum = int(input())

            print(MSLnum)
            print(VSLnum)

            # SetandUpdateVSL
            if Direction == "buy":
                ToBe = (CP - ((I * MV) / VSLnum))
                print(ToBe)
                print("VSLrdfhdxnf")

                # CurrentProfit = (CurrentProfit - ((abs(CurrentProfit) / 100)) * VSLnum) - (Commision)
                VSL = (((ToBe + Commision) * BP) / (MV * I)) + BP

                print(VSL)
                if VSL < LP and VSL > oldVSL:
                    AllowtomoveMSL = True
                    NewVarSL = VSL
                    print("Set VSL using calcualted moving VSL buy ")

                else:
                    AllowtomoveMSL = False
                    NewVarSL = oldVSL
                    NewMaxSL = oldMaxSL
                    print("NOT updated VSL access to move MSL denied buy")

            if Direction == "sell":
                ToBe = (CP - ((I * MV) / VSLnum))
                print(ToBe)
                print("VSLrdfhdxnf")

                # CurrentProfit = (CurrentProfit - ((abs(CurrentProfit) / 100)) * VSLnum) - (Commision)
                VSL = BP * (1 - ToBe + Commision / (I * MV))

                if VSL > LP and VSL < oldVSL:
                    AllowtomoveMSL = True
                    NewVarSL = VSL
                    print("Set VSL using calcualted moving VSL  sell")



                else:
                    AllowtomoveMSL = False
                    NewVarSL = oldVSL
                    NewMaxSL = oldMaxSL
                    print("NOT updated VSL access to move MSL denied sell")

            if AllowtomoveMSL == True:
                print("Allowed to move MSL position QWERTY")
                specialnumber = float(Specialnumber)
                print(specialnumber)

                if Direction == "buy":

                    ToBe = (CP - ((I * MV) / MSLnum))
                    print(ToBe)
                    print("MSLrdfhdxnf")

                    # CurrentProfit = (CurrentProfit - ((abs(CurrentProfit) / 100)) * MSLnum) - (Commision)
                    MSL = (((ToBe + Commision) * BP) / (MV * I)) + BP

                    print(MSL)
                    print(specialnumber)
                    print(LP)

                    if not MSL + specialnumber >= LP:

                        if MSL != str(oldMaxSL):
                            NewMaxSL = MSL
                            SetandeditRealSL(NewMaxSL, LPstr)
                            print("Works buy " + str(NewMaxSL))
                            print("Set MSL using calcualted")
                            print("From " + str(oldVarSL) + "to " + str(NewVarSL))
                            print("From " + str(oldMaxSL) + "to " + str(NewMaxSL))
                            print(str(LP))
                        else:
                            print("MaxSL too close to Price ")
                            print(MSL)
                            NewMSL = LP - float(specialnumber)
                            SetandeditRealSL(NewMSL, LPstr)
                            print("Set MSL using safety net")

                    else:
                        print()
                        SetandeditRealSL((MSL - float(specialnumber)), LPstr)
                        NewMaxSL = MSL

                if Direction == "sell":
                    ToBe = (CP - ((I * MV) / MSLnum))
                    print(ToBe)

                    print("MSLrdfhdxnf")

                    # CurrentProfit = (CurrentProfit - ((abs(CurrentProfit) / 100)) * MSLnum) - (Commision)
                    MSL = BP * (1 - (ToBe + Commision) / (I * MV))
                    print(MSL)

                    if not MSL + specialnumber >= LP:
                        NewMaxSL = MSL
                        print(MSL)
                        if MSL != str(oldMaxSL):
                            SetandeditRealSL(NewMaxSL, LPstr)
                            print("Works buy" + str(NewMaxSL))
                            print("Set MSL using calcualted")
                            print("From " + str(oldVarSL) + "to " + str(NewVarSL))
                            print("From " + str(oldMaxSL) + "to " + str(NewMaxSL))
                            print(str(LP))
                        else:
                            print("MaxSL too close to Price ")
                            print(MSL)
                            NewMSL = LP - float(specialnumber)
                            SetandeditRealSL(NewMSL, LPstr)
                            print("Set MSL using safety net")
                    else:
                        SetandeditRealSL((MSL + float(specialnumber)), LPstr)
                        NewMaxSL = MSL
                        print("brokewn sheweeh")

            else:
                print("Not allowed to move MSL yet proceeding to next trade")
                print(oldVSL)
                print(NewVarSL)
                print(LPstr)

            Newtradedata = str(URL) + "|" + str(Direction) + "|" + str(I) + "|" + \
                           str(MV) + "|" + str(LP) + "|" + str(BP) + "|" + str(CP) \
                           + "|" + str(NewMaxSL) + "|" + str(NewVarSL) + "|" + Name + "|" + str(Specialnumber) \
                           + "|" + str(partialnewtradeurl) + "|" + str(Commision) + "|" + str(tobecut)

            print("------------------")

            print(Newtradedata)
            print(LP)
            print(oldVSL)
            print(NewVarSL)
            print(NewMaxSL)
            print(BP)

            print("----------------------------------------")
            # input()

            [item.replace(traddetails, Newtradedata) for item in Globallist]

            Checkiftradestillpresent(traddetails)
            Updatetrade(Newtradedata, traddetails)




        else:
            print("An error occurred else caught")
            Checkiftradestillpresent(traddetails)


    except:
        print("An error occurred except caught")
        A  = Checkiftradestillpresent(traddetails)
        # if A == False:
        #     try:
        #         Getthespecialnumber(Direction)






def Deleteclosedtradetab():
    driver1.close()

def Indextocorrecttab(URL):
    count=0
    for tab in itertools.cycle(reversed(driver1.window_handles)):
        driver1.switch_to.window(tab)
        print(URL)
        print("Indexing..")

        count+=1
        print(count)
        if count ==100 or driver1.current_url.__contains__("#modal_news")==True:
            Wait("XPATH","ThestupidDowJoneserror")
            #index between each page and press refresh on each
            for tab in itertools.cycle(reversed(driver1.window_handles)):
                driver1.switch_to.window(tab)
                driver1.quit()
                Start()
            time.sleep(5)

        if str(driver1.current_url) == str(URL):
            print(str(driver1.current_url))
            print("Indexed to correct tab")
            break




def GetLP(URL):
    Price = 0

    currenturl = URL
    comebackurl  =  driver1.current_url
    while True:
        try:
            driver1.find_element(By.XPATH, "//span[@class='fake-dialog-close']").click()
            driver1.get(currenturl)
        except:
            print("Dont need to press X yet for the Fake Dialog thing ")
        try:
            #A = driver1.find_element(By.PARTIAL_LINK_TEXT, str(Name)).get_attribute("href")
            A = driver1.find_element(By.XPATH, "//body/div[1]/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]/div[3]/a[1]").get_attribute("href")
            print(A)
            driver1.find_element(By.XPATH,"//body/div[1]/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]/div[3]/a[1]").click()
            break
        except:
            print("error")
            break


    while True:

        Wait("XPATH", "//p[@class='col-rate']")
        print("tfbszgaeesdgfhsddhua")
        Price = driver1.find_element(By.XPATH, "//p[@class='col-rate']").text
        Price = str(Price).replace(" ", "")
        print(Price)
        global partialnewtradeurl

        partialnewtradeurl  = str(driver1.current_url)
        #codenamepart = str(driver1.find_element(By.XPATH,"/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/h1[1]/span[1 or 2 depending on if forex or not]").text)
        qwe = partialnewtradeurl.split("/")
        codenamepart = qwe[-2]
        print("zdfgjn")
        print(codenamepart)
        print(codenamepart)
        codenamepart = codenamepart.replace("(","")
        codenamepart = codenamepart.replace(")", "")
        try:
            codenamepart = codenamepart.replace("/", "")
        except:
            print()
        partialnewtradeurl = partialnewtradeurl + "#modal_newInvest_" + codenamepart
        print(partialnewtradeurl)



        driver1.get(currenturl)
        time.sleep(3)
        print(Price)

        break

    return str(Price)




def Newtradesetup():
    Notradeinfanant = False
    global partialnewtradeurl, Werty
    try:
        A = []
        Aforfirst()
        # Currenttradelist
        while Notradeinfanant != True:

            try:
                driver1.find_element(By.XPATH,
                                     "//body/div[1]/aside[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]").click()
            except:
                print()

            try:  # Do this after visible list
                driver1.find_element(By.CSS_SELECTOR, ".show-more:nth-child(2) > .more").click()
            except Exception as e:
                print("Less than a few trades open")
            driver1.find_element(By.XPATH, "//body/div[1]").click()

            for i in range(1, 6):
                try:
                    Clickonindexedtradevisible(i)
                    url = driver1.current_url
                    if driver1.current_url.__contains__("invest"):
                        if not A.__contains__(url):
                            A.append(url)


                except:
                    print("An error occurred while trying to access the visible trades list")

            try:
                driver1.find_element(By.XPATH, "//body/div[1]/div[3]/div[1]/div[1]/button[1]").click()
                driver1.find_element(By.XPATH, "//body/div[1]").click()
            except:
                print()

            time.sleep(0.2)
            try:
                ScrollingOverflowlist(1)
            except:
                print()
            count = 1
            breaker = False
            while breaker != True:

                print(count)
                try:
                    ClickonindexedtradeOverflow(count)
                    url = driver1.current_url
                    if driver1.current_url.__contains__("invest"):
                        if not A.__contains__(url):
                            A.append(url)

                except:
                    print("FGNTY")
                    breaker = True
                try:
                    driver1.find_element(By.XPATH, "//body/div[1]/div[3]/div[1]/div[1]/button[1]").click()

                    print()
                except:
                    print("tgnbsrf")
                try:
                    ScrollingOverflowlist(count + 1)
                except:

                    print("reached limit")
                count += 1
            try:
                A.remove("https://app.libertex.com/")
            except:
                print("gdxnbyr")
            if len(A) > 0:
                for i in A:
                    print(i)
                print(len(A))
                Notradeinfanant = True

            else:
                print("No trades currently")
                time.sleep(20)

        tradecodes = []
        for r in A:
            derk = ""
            for q in r:
                if ord(q) > 47 and ord(q) < 58:
                    derk += q

            tradecodes.append(derk)
        print(tradecodes)
        # DBcode1 = ""
        # DBcode2 = ""
        DBread()
        for i in A:
            print(i)

        for i in Werty:
            print(i)
            print("dfsbsd")
            if not str(i).__contains__("^"):
                delta = str(i).split("|")
                if A.__contains__(str(delta[0])):
                    A.remove(str(delta[0]))
                    print(str(delta[0]))
                    print("thbhtfnhrsjh")
                    A.append(i)

        for o in Werty:
            print(o)
            print("Iodine")
            print(tradecodes)

            for r in tradecodes:
                if str(o).__contains__(r) and str(o).__contains__("^"):
                    print("Got it")

                    print(o)
                    print("trade present in this bind")
                    print("deleting these pending orders from the list")
                    deletetradefromdb(str(o))
                    split = str(o).split("^")
                    Pos1 = split[0]
                    Pos2 = split[1]
                    Pos1 = Pos1.replace("^", "")
                    Pos2 = Pos2.replace("^", "")
                    try:
                        if Pos1 != "Rebootoryeah":
                            driver1.get(Pos1)

                            time.sleep(0.5)
                            driver1.find_element(By.XPATH, "//span[contains(text(),'Cancel order')]").click()
                            driver1.find_element(By.XPATH, "//span[contains(text(),'Yes, delete')]").click()
                            driver1.find_element(By.XPATH, "//span[contains(text(),'OK')]").click()

                            print("gfhnfntffg")
                        else:
                            print(" Partial Pending order already opened")
                    except:
                        print("is the other one")
                    try:
                        if Pos2 != "Rebootoryeah":
                            driver1.get(Pos2)

                            time.sleep(0.5)
                            driver1.find_element(By.XPATH, "//span[contains(text(),'Cancel order')]").click()
                            driver1.find_element(By.XPATH, "//span[contains(text(),'Yes, delete')]").click()
                            driver1.find_element(By.XPATH, "//span[contains(text(),'OK')]").click()
                            print("gfhnfg")
                        else:
                            print(" Partial Pending order already opened")

                    except:
                        print("is pos 1 one")
                    Aforfirst()
                    try:
                        Werty.remove(o)
                    except:
                        print()
                    try:
                        driver1.find_element(By.XPATH, "//body/div[1]/div[3]/div[1]/div[1]/button[1]").click()
                    except:
                        print()
                else:
                    print("Woops")

        print("Fudgedfhf")
        for i in A:
            print(i)
        print("sdvdbdd")

        for i in Alreadyappendedtrades:
            print("blsowgff")
            print(i)

        for i in A:
            try:
                f = str(i).split("|")
                i = str(f[0])
            except:
                print("First time")

            if not Alreadyappendedtrades.__contains__(i):

                fulldata = i
                print("Start")
                # dumass = None
                print(i)
                if fulldata.__contains__("buy") or fulldata.__contains__("sell"):
                    print("Method2")
                    alreadycollecteddatasplit = str(fulldata).split("|")
                    OpenURL(alreadycollecteddatasplit[0])
                    Indextocorrecttab(alreadycollecteddatasplit[0])
                    Name = alreadycollecteddatasplit[9]
                    Direction = alreadycollecteddatasplit[1]
                    I = float(alreadycollecteddatasplit[2])
                    MV = float(alreadycollecteddatasplit[3])
                    Commision = float(alreadycollecteddatasplit[12])
                    BP = float(alreadycollecteddatasplit[5])
                    CP = float(alreadycollecteddatasplit[6])
                    Q = float(alreadycollecteddatasplit[7])  # MSL
                    W = float(alreadycollecteddatasplit[10])  # Special number
                    LivePrice = str(GetLP(alreadycollecteddatasplit[0]))
                    LPstr = LivePrice
                    print(LivePrice)
                    print(LP)
                    LP = float(LivePrice)
                    Nums()
                    URL = alreadycollecteddatasplit[0]
                    tobecut = alreadycollecteddatasplit[13]

                else:
                    print("Method1")
                    OpenURL(i)

                    Indextocorrecttab(i)

                    Wait("XPATH", "//body/div[1]/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]/div[3]/a[1]")
                    E = driver1.find_element(By.XPATH,
                                             "//body/div[1]/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]/div[3]/a[1]").text
                    print(E)  # Name

                    URL = str(i)
                    Name = str(E)
                    Direction = str(Gettradedirection())
                    I = float(GetInvestAmount())
                    MV = float(GetMultiplierAmount())
                    Commision = float(Getcomission())
                    BP = float(GetboughtPrice())
                    CP = float(GettingcurrentProfitLoss())
                    Nums()
                    print("Proceeded to this point in Setting up new trades")
                    Q = str(GetMSL())
                    W = float(Getthespecialnumber(Direction))
                    LivePrice = str(GetLP(URL))
                    LPstr = LivePrice
                    tobecut = ""
                    if str(LPstr).__contains__("."):
                        tobecut = "F"
                    else:
                        tobecut = "T"
                    LP = 0

                    # if Direction =="buy":
                    #    LP = ((CP + Commision) * BP) / (MV * I) + BP
                    # if Direction =="sell":
                    #    LP = BP * (1 - (CP + Commision) / (I * MV))
                    print(LivePrice)
                    print(LP)
                    LP = float(LivePrice)
                    URL = i

                time.sleep(1)
                MaxSL = 0
                VarSL = 0

                if Q == "-1":
                    if Direction == "buy":
                        ToBe = (CP - ((I * MV) / MSLnum))
                        MSL = ((ToBe + Commision) * BP) / (MV * I) + BP
                        print(MSL)
                        print(ToBe)
                        print(Commision)
                        print("------")
                        print(LP)
                        print(W)
                        print(Q)
                        print(Direction)
                        if (MSL + float(W)) < LP:
                            MaxSL = MSL
                            print(MaxSL)
                            SetandeditRealSL(str(MSL), LPstr)
                        else:
                            print()
                            NewMSL = float(LP) - float(W * 1.5)
                            MaxSL = NewMSL
                            SetandeditRealSL(NewMSL, LPstr)
                    if Direction == "sell":
                        ToBe = (CP - ((I * MV) / MSLnum))
                        # CurrentProfit = (CurrentProfit - ((abs(CurrentProfit) / 100)) * MSLnum) - (Commision )
                        MSL = BP * (1 - (ToBe + Commision) / (I * MV))
                        print(MSL)
                        print(Commision)
                        print(ToBe)
                        print("------")
                        print(LP)
                        print(W)
                        print(Q)
                        print(Direction)
                        if (MSL - float(W)) > LP:
                            print()
                            MaxSL = MSL
                            print(MaxSL)
                            SetandeditRealSL(str(MaxSL), LPstr)
                        else:
                            print()
                            NewMSL = float(LP) + float(W * 1.5)
                            MaxSL = NewMSL
                            SetandeditRealSL(NewMSL, LPstr)
                else:
                    if Direction == "buy":
                        ToBe = (CP - ((I * MV) / MSLnum))
                        # CurrentProfit = (CurrentProfit - ((abs(CurrentProfit) / 100)) * MSLnum) - (Commision )
                        MSL = ((ToBe + Commision) * BP) / (MV * I) + BP
                        print(MSL)
                        print("------")
                        print(LP)
                        print(W)
                        print(Q)
                        print(Direction)
                        if (MSL + float(W)) < LP:
                            print(MaxSL)
                            MaxSL = MSL
                            SetandeditRealSL(str(MaxSL), LPstr)
                        else:
                            print()
                            NewMSL = float(LP) - float(W)
                            MaxSL = NewMSL
                            SetandeditRealSL(NewMSL, LPstr)
                    if Direction == "sell":
                        ToBe = (CP - ((I * MV) / MSLnum))
                        # CurrentProfit = (CurrentProfit - ((abs(CurrentProfit) / 100)) * MSLnum) - ( Commision )
                        MSL = BP * (1 - (ToBe + Commision) / (I * MV))
                        print(MSL)
                        print("------")
                        print(LP)
                        print(W)
                        print(Q)
                        print(Direction)
                        if (MSL - float(W)) > LP:
                            print()
                            MaxSL = MSL
                            SetandeditRealSL(str(MaxSL), LivePrice)
                        else:
                            print()
                            NewMSL = float(LP) + float(W)
                            MaxSL = NewMSL
                            SetandeditRealSL(NewMSL, str(LP))
                if Direction == "buy":
                    ToBe = (CP - ((I * MV) / VSLnum))
                    # CurrentProfit = (CurrentProfit - ((abs(CurrentProfit) / 100)) * VSLnum) - (Commision )
                    VSL = ((ToBe + Commision) * BP) / (MV * I) + BP
                    VarSL = VSL
                    print(VarSL)
                if Direction == "sell":
                    ToBe = (CP - ((I * MV) / VSLnum))
                    # CurrentProfit = (CurrentProfit - ((abs(CurrentProfit) / 100)) * VSLnum) - (Commision )
                    VSL = BP * (1 - ToBe + Commision / (I * MV))
                    VarSL = VSL
                    print(VarSL)
                Newtradedata = URL + "|" + Direction + "|" + str(I) + "|" + \
                               str(MV) + "|" + str(LP) + "|" + str(BP) + "|" + str(CP) + "|" + str(MaxSL) \
                               + "|" + str(VarSL) + "|" + str(Name) + "|" + str(W) + "|" + str(
                    partialnewtradeurl) \
                               + "|" + str(Commision) + "|" + str(tobecut)
                print(Newtradedata)

                if not Alreadyappendedtrades.__contains__(URL):
                    print("Appeneded this url")
                    print(URL)
                    Globallist.append(Newtradedata)
                    Alreadyappendedtrades.append(URL)
                Allowed = True
                for er in Werty:
                    if URL in str(er):
                        Allowed = False
                if Allowed == True:
                    Creatependingorderlink(Newtradedata)


    except:
        print("An error occourred in Newtradesetup")
        Newtradesetup()
    Aforfirst()


def triggershort(NowMulti,NowInvest):
    Wait("ID", "mult")
    driver1.find_element(By.XPATH, "//input[@id='sumInv']").clear()
    driver1.find_element(By.XPATH, "//input[@id='sumInv']").send_keys(NowInvest)
    driver1.find_element(By.XPATH, "//input[@id='mult']").clear()
    driver1.find_element(By.XPATH, "//input[@id='mult']").send_keys(NowMulti)
    driver1.find_element(By.XPATH, "//div[@class='box-row investment-buttons']//span[@class='a-reduction a-submit']//span").click()


def triggerlong(NowMulti,NowInvest):
    Wait("ID","mult")
    driver1.find_element(By.XPATH, "//input[@id='sumInv']").clear()
    driver1.find_element(By.XPATH, "//input[@id='sumInv']").send_keys(NowInvest)
    driver1.find_element(By.XPATH, "//input[@id='mult']").clear()
    driver1.find_element(By.XPATH, "//input[@id='mult']").send_keys(NowMulti)
    driver1.find_element(By.XPATH, "//div[@class='box-row investment-buttons']//span[@class='a-growth a-submit']//span").click()

def triggershortpending(NowMulti,NowInvest,PriceSell):
    Wait("XPATH","//body/div[1]/div[3]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/label[2]")
    driver1.find_element(By.XPATH,"//body/div[1]/div[3]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/label[2]").click()
    driver1.find_element(By.XPATH, "//input[@id='sumInv']").clear()
    driver1.find_element(By.XPATH, "//input[@id='sumInv']").send_keys(NowInvest)
    driver1.find_element(By.XPATH, "//input[@id='mult']").clear()
    driver1.find_element(By.XPATH, "//input[@id='mult']").send_keys(NowMulti)
    driver1.find_element(By.XPATH, "//input[@id='openRate']").clear()
    driver1.find_element(By.XPATH, "//input[@id='openRate']").send_keys(str(PriceSell))
    driver1.find_element(By.XPATH, "//div[@class='box-row investment-buttons']//span[@class='a-reduction a-submit']//span").click()


def triggerlongpending(NowMulti,NowInvest,PriceBuy):
    Wait("XPATH", "//body/div[1]/div[3]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/label[2]")
    driver1.find_element(By.XPATH,"//body/div[1]/div[3]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/label[2]").click()
    driver1.find_element(By.XPATH, "//input[@id='sumInv']").clear()
    driver1.find_element(By.XPATH, "//input[@id='sumInv']").send_keys(NowInvest)
    driver1.find_element(By.XPATH, "//input[@id='mult']").clear()
    driver1.find_element(By.XPATH, "//input[@id='mult']").send_keys(NowMulti)
    driver1.find_element(By.XPATH, "//input[@id='openRate']").clear()
    driver1.find_element(By.XPATH, "//input[@id='openRate']").send_keys(str(PriceBuy))
    driver1.find_element(By.XPATH, "//div[@class='box-row investment-buttons']//span[@class='a-growth a-submit']//span").click()

def Setupnewtrade(previousdata):

    split = str(previousdata).split("|")
    newInvestURL = split[11]
    driver1.get(newInvestURL)
    Direction = split[1]
    InvestAmount = split[2].split(".")
    InvestAmount = int(InvestAmount[0])
    MV = split[3].split(".")
    MV = int(MV[0])
    LP = split[4]

    BP = float(split[5])
    #ToBe = float(split[6])#Current CP
    Commision = float(split[12])
    print(previousdata)
    ##########################
    ToBe = (2 - ((int(InvestAmount) * int(MV)) / VSLnum)) / 2

    print(ToBe)

    # iNITITING
    if Direction == "buy":
        print("pending order")
        #PriceBuy = ((ToBe + Commision) * BP) / (MV * InvestAmount) + BP
        #PriceSell = BP * (1 - (ToBe + Commision) / (InvestAmount * MV))
        #print(PriceSell)
        #print(PriceBuy)
        LP = float(GetLP(newInvestURL))
        PriceBuy = LP - ToBe
        if str(LP).__contains__("."):
            split = str(PriceBuy).split(".")
            PriceBuy = split[0]
        else:
            print()
        triggershortpending(MV, InvestAmount, PriceBuy)

        print("pending orders")
        driver1.get(newInvestURL)
        LP = float(GetLP(newInvestURL))
        PriceSell = LP + ToBe
        if str(LP).__contains__("."):
            split = str(PriceSell).split(".")
            PriceSell = split[0]

        else:
            print()
        print(PriceSell)
        triggerlongpending(MV, InvestAmount, PriceSell)




    if Direction == "sell":
        print("pending order")
        #PriceSell = BP * (1 - (ToBe + Commision) / (InvestAmount * MV))
       # PriceBuy = ((ToBe + Commision) * BP) / (MV * InvestAmount) + BP
        LP = float(GetLP(newInvestURL))
        PriceSell = LP + ToBe
        if str(LP).__contains__("."):
            split = str(PriceSell).split(".")
            PriceSell = split[0]

        else:
            print()
        print(PriceSell)
        triggerlongpending(MV, InvestAmount, PriceSell)

        print(" pending orders")
        driver1.get(newInvestURL)
        LP = float(GetLP(newInvestURL))
        PriceBuy = LP - ToBe
        if str(LP).__contains__("."):
            split = str(PriceBuy).split(".")
            PriceBuy = split[0]
        else:
            print()
        triggershortpending(MV, InvestAmount, PriceBuy)

    Deleteclosedtradetab()
    Aforfirst()
    try:
        driver1.execute_script("arguments[0].scrollIntoView()", driver1.find_element(By.XPATH,  # scroll visible
                                                                                     "//body/div[1]/aside[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[" + str(
                                                                                         5) + "]/div[1]"))
    except:
        print("Error")
    try:
        driver1.find_element(By.XPATH,  # show more pending order
                             "//body/div[1]/aside[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/span[1]/span[1]").click()
    except:
        print("gfhzbfn")
    Binded = ""
    for i in range(1, 6):
        try:
            time.sleep(0.5)
            driver1.execute_script("arguments[0].scrollIntoView()", driver1.find_element(By.XPATH,  # scroll visible
                                                                                         "//body/div[1]/aside[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[" + str(
                                                                                             i) + "]/div[1]"))
        except:
            print("Error")
        driver1.find_element(By.XPATH, "//body/div[1]").click()

        try:
            time.sleep(0.5)
            driver1.find_element(By.XPATH,  # Click vsible
                                 "//body/div[1]/aside[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[" + str(
                                     i) + "]/div[1]/div[1]/div[1]/span[1]").click()

            if not Pendingorderlist.__contains__(driver1.current_url):
                Pendingorderlist.append(driver1.current_url)
                print(driver1.current_url)
                Binded += str(driver1.current_url) + "^"
                print("Newurl")
                if Binded.count("^") == 2:
                    break


        except:
            print("Erorr pending order list or indexed to end of visible list")
        try:
            driver1.find_element(By.XPATH, "//body/div[1]/div[3]/div[1]/div[1]/button[1]").click()
        except:
            print()

        try:
            driver1.find_element(By.XPATH, "//body/div[1]").click()
        except:
            print()

    c = 0
    while True:
        c += 1
        driver1.find_element(By.XPATH, "//body/div[1]").click()

        try:
            time.sleep(0.3)
            driver1.execute_script("arguments[0].scrollIntoView()",
                                   driver1.find_element(By.XPATH,  # scroll overflow
                                                        "//body/div[1]/aside[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]"
                                                        "/div[2]/div[2]/div[" + str(c) + "]/div[1]"))
        except:
            print("Error")
            break
        driver1.find_element(By.XPATH, "//body/div[1]").click()

        try:
            time.sleep(0.3)
            driver1.find_element(By.XPATH,  # Click overflow
                                 "//body/div[1]/aside[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/div[2]/div[" + str(
                                     c) + "]"
                                          "/div[1]/div[1]/div[1]/span[1]").click()
            if not Pendingorderlist.__contains__(driver1.current_url):
                Pendingorderlist.append(driver1.current_url)
                print(driver1.current_url)
                Binded += str(driver1.current_url) + "^"
                print("Newurl")
                if Binded.count("^") == 2:
                    break


        except:
            print("Erorr pending order list or indexed to end of visible list")

        try:
            driver1.find_element(By.XPATH, "//body/div[1]/div[3]/div[1]/div[1]/button[1]").click()
        except:
            print("fbfdb")

        try:
            driver1.find_element(By.XPATH, "//body/div[1]").click()
        except:
            print("hbkmygmnxf")  # This part is kind of broken wtf

    Binded = Binded

    if not Binded.count("^") == 2:
        Binded += "Rebootoryeah"

    print(Binded)
    Creatependingorderlink(Binded)
    FirstTab()
    #indexing issue










def OpenURL(NowURL):

    if not Openedtrades.__contains__(NowURL):
        driver1.execute_script("window.open('" + NowURL + "');")
        Openedtrades.append(NowURL)


def Newloopinglistforrun():
    global driver1,t_end,Alreadyappendedtrades,Globallist
    Listed = []
    tradecountreset = 0
    while 1 != 2:


        Ace = random.choice(Globallist)
        print(Ace)
        uyu = str(Ace).split()


        print("Dumrfdbd")
        for i in Globallist:
            print(i)
        print("bdfn")

        if time.time() <= t_end:
            print("TFDHT")
            if not Listed.__contains__(Ace):
                tradecountreset +=1
                TradingLogic(Ace)
                if Alreadyappendedtrades.__contains__(str(uyu[0])):
                    Listed.append(Ace)
                    print("DRJHARG")


        else:


            driver1.quit()
            driver1 = uc.Chrome()

            for i in Globallist:
                print(i)

            for i in Alreadyappendedtrades:
                print(i)

            Alreadyappendedtrades.clear()
            Globallist.clear()
            Openedtrades.clear()

            t_end = time.time() + timetillreboot
            bootup1()

        if len(Listed) == len(Globallist):
            Listed.clear()#
            print("Lolredthr")#This is never reached
        print(tradecountreset)
        print(len(Listed))
        print(len(Globallist))
        print("Dumbeldore")
        if tradecountreset >= len(Globallist):
            tradecountreset = 0
            Newtradesetup()




def Pendingorderlistsetup():
    # Pendingorderlist
    try:
        driver1.execute_script("arguments[0].scrollIntoView()", driver1.find_element(By.XPATH,  # scroll visible
                                                                                     "//body/div[1]/aside[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[" + str(
                                                                                         5) + "]/div[1]"))
    except:
        print("Error")
    try:
        driver1.find_element(By.XPATH,  # show more pending order
                             "//body/div[1]/aside[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/span[1]/span[1]").click()
    except:
        print("gfhzbfn")

    for i in range(1, 6):
        try:
            time.sleep(0.2)
            driver1.execute_script("arguments[0].scrollIntoView()", driver1.find_element(By.XPATH,  # scroll visible
                                                                                         "//body/div[1]/aside[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[" + str(
                                                                                             i) + "]/div[1]"))
        except:
            print("Error drfh")
        try:
            driver1.find_element(By.XPATH, "//body/div[1]").click()
        except:
            print()

        try:
            time.sleep(0.2)
            driver1.find_element(By.XPATH,  # Click vsible
                                 "//body/div[1]/aside[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[" + str(
                                     i) + "]/div[1]/div[1]/div[1]/span[1]").click()
            if not  Pendingorderlist.__contains__(driver1.current_url):
                Pendingorderlist.append(driver1.current_url)
                print(driver1.current_url)



        except:
            print("Erorr pending order list or indexed to end of visible list")
        try:
            driver1.find_element(By.XPATH, "//body/div[1]/div[3]/div[1]/div[1]/button[1]").click()
        except:
            print()

        try:
            driver1.find_element(By.XPATH, "//body/div[1]").click()
        except:
            print()

    i = 0
    while True:
        i += 1
        driver1.find_element(By.XPATH, "//body/div[1]").click()

        try:
            time.sleep(0.2)
            driver1.execute_script("arguments[0].scrollIntoView()",
                                   driver1.find_element(By.XPATH,  # scroll overflow
                                                        "//body/div[1]/aside[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]"
                                                        "/div[2]/div[2]/div[" + str(i) + "]/div[1]"))
        except:
            print("Error")
            break
        driver1.find_element(By.XPATH, "//body/div[1]").click()

        try:
            time.sleep(0.2)
            driver1.find_element(By.XPATH,  # Click overflow
                                 "//body/div[1]/aside[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/div[2]/div[" + str(
                                     i) + "]"
                                          "/div[1]/div[1]/div[1]/span[1]").click()
            if not Pendingorderlist.__contains__(driver1.current_url):
                Pendingorderlist.append(driver1.current_url)
                print(driver1.current_url)



        except:
            print("Erorr pending order list or indexed to end of overflow list")

        try:
            driver1.find_element(By.XPATH, "//body/div[1]/div[3]/div[1]/div[1]/button[1]").click()
        except:
            print("fbfdb")

        try:
            driver1.find_element(By.XPATH, "//body/div[1]").click()
        except:
            print("hbkmygmnxf")


def bootup1():

    global Pendingorderlist


    for i in Globallist:
        print(i)

    for i in Alreadyappendedtrades:
        print(i)

    FirstTab() #160-155
    login()#170
    TransfertoDemoACC()#179
    time.sleep(2)
    Pendingorderlistsetup()
    Newtradesetup()
    Newloopinglistforrun()

def Createtable():
    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        sqlite_create_table_query = '''CREATE TABLE SqliteDb_developers (
                                    Entiretrade text
                                    );'''
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")
        cursor.execute(sqlite_create_table_query)
        sqliteConnection.commit()
        print("SQLite table created")

        cursor.close()
    except:
        print("Error")
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")


def Creatependingorderlink(data):
    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")



        cursor.execute("insert into SqliteDb_developers (Entiretrade) values (?)",
                       (data,))


        sqliteConnection.commit()
        print("Python Variables inserted successfully into SqliteDb_developers table")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")


def DBread():
    global Werty
    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_select_query = """SELECT * from SqliteDb_developers"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        for row in records:
            print(row[0])
            if not Werty.__contains__(str(row[0])):
                Werty.append(str(row[0]))
            sqliteConnection.commit()

        cursor.close()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")

def deletetradefromdb(datatodelete):


    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        print(datatodelete)
        sql_update_query = """DELETE from SqliteDb_developers where Entiretrade = ?"""
        cursor.execute(sql_update_query, (datatodelete,))
        sqliteConnection.commit()
        print("Record deleted successfully")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to delete record from a sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.commit()
            sqliteConnection.close()
            print("sqlite connection is closed")

def deletealltradesdb():
    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_select_query = """SELECT * from SqliteDb_developers"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        print("Total rows are:  ", len(records))
        print("Printing each row")
        for row in records:
            try:
                Data = str(row[0])
                deletetradefromdb(Data)
            except Exception as e:
                print("Removing trade ..an error occurred")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")



def Updatetrade(Newdata, Olddata):
    try:

        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sql_update_query = """Update SqliteDb_developers set Entiretrade = ? where Entiretrade = ?"""
        data = (Newdata, Olddata)
        cursor.execute(sql_update_query, data)
        sqliteConnection.commit()
        print("Record Updated successfully")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to update sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The sqlite connection is closed")

Alreadyappendedtrades = []
Openedtrades = []
Globallist = []
Pendingorderlist = []
Werty = []
# driver1 = uc.Chrome()
skip = None
driver1 = webdriver.Chrome()
# driver1 = webdriver.Edge()
MSLnum = 00
VSLnum = 00
partialnewtradeurl = ""
timetillreboot = (60 * (60 * 2))
t_end = time.time() + timetillreboot

def Start():
    try:








        deletealltradesdb()

        bootup1()  # //h4[contains(text(),'Non-trading hours')]
        DBread()
    except:
        print("Rebooting")
        Start()

#Start()
bootup1()



    #buy equation
    #CPL = ((LP/BP)-1)*(I*MV)- Commision

    #sell equation
    #CPL = (1-(LP/BP))*(I*MV)-Commision


# split = str(o).split()
# Pos1 = split[0]
# Pos2 = split[1]
# for q in Pos1:
#     if ord(q) > 47 and ord(q) < 58:
#         DBcode1 += q
# for q in Pos2 :
#     if ord(q) > 47 and ord(q) < 58:
#         DBcode2+=q







