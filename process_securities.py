import csv
import glob
import os.path
import io
import heapq
import re
import sys


def calculate_risk(trades_sell, trades_buy):
    '''
    SEARCH for BUY SIDE and SELL SIDE Trades for each Security and 
    CALCULATE LONG SHORT Positions
    '''
    #TO DO: Finish Loss Calculation
    #loss_positions = []
    risk = ''
    risk_positions = []
    for ts in trades_sell:
        for tb in trades_buy:
            if ts[1] == tb[1]:
                # CALCULATE if we sold securities for less than we bought them
                loss = (float(ts[4])*float(ts[5])) - (float(tb[4])*float(tb[5]))
                # CALCULATE if we have sold less securites than we bought
                if loss < 0:
                    #loss_positions.append(ts[1])
                    #loss_positions.append(ts[2])
                    risk = (int(tb[4]) - int(ts[4]))
                    if risk < tb[4] and risk > 0:
                        tbs = []
                        tbs.append(risk)
                        tbs.append(tb[2])
                        tbs.append(tb[1])
                        risk_positions.append(tbs)
    risk_positions = sorted(risk_positions)
    return risk_positions 

def get_counter_party(f):
    '''
    Extracts Counter Party name from file name
    and returns them for processing
    '''
    cpn = ''
    for i in range(0,3): 
        cpn += f[i] 
    return cpn

def get_marks():
    '''
    Reads all Securities "Marks" into a list for inclusion as part
    of Risk Position record
    '''
    smark = ''
    smarks = []
    with open('marks', 'rb') as m:
        reader = csv.reader(m)
        for m in reader:
            smark = m
            smarks.append(smark)
    return smarks 

def get_top_twenty_counter_parties():
    '''
    GET TOP 20 - Biggest Dollar Trading Counterparties
    '''
  

def get_top_twenty_risk(risk_positions):
    '''
    CALCULATE RISK for Holdings in Securities
    '''
    srisks = []
    risk_positions = sorted(risk_positions)
    smarks = get_marks()
    for rp in risk_positions:
        for smark in smarks:
            if rp[2] == smark[1]:
                srisk = []
                srisk.append(rp[0])
                srisk.append(rp[1])
                srisk.append(rp[2])
                srisk.append(smark[2])
                srisks.append(srisk)
    # GET TOP 20 = Asset RISK Long Positions
    t20 = heapq.nlargest(20, srisks)
    return t20

def process_trade_information():
    '''
    READ IN trade data from all files that are marked .csv
    in corresponding directory
    '''
    cparties= []
    cp_volume = []
    final_trades = {}
    risk_positions = []
    trade_in = ''
    trades_buy = []
    trades_sell = []
    top_twenty_risks = []

    for f in glob.glob("*.csv"):
        cp_name = ''
        cparties.append(f)
        # Get Counter Party name from file name
        cp_name = get_counter_party(f)
        with open(f, 'rb') as f:
            reader = csv.reader(f)
            for r in reader:
                trade_in = r
                # Pass in all BUY trades for the 
                # counter party
                if trade_in[3].strip() == "BUY":
                    trades_buy.append(trade_in)
                # Pass in all SELL trades for the 
                # counter party
                elif trade_in[3].strip() == "SELL":
                    trades_sell.append(trade_in)   
                cp_volume.append(trade_in)
        # Pass in SELL and BUY sides of all TRADES
        # for ALL counter parties for final volume processing
        final_trades[cp_name] = cp_volume
        #TO DO: Calculate top 20 Counter Parties
        #top_twenty_counter_parties = get_top_twenty_counter_parties(final_trades)
    #print final_trades
    risk_positions = calculate_risk(trades_sell, trades_buy)
    top_twenty_risks = get_top_twenty_risk(risk_positions)
    return top_twenty_risks 

def main():
    '''
    WRITE all data in CSV files into one file
    '''
    with open('top_20_risk.txt', 'wb') as top:
        writer = csv.writer(top, delimiter=',')
        top_twenty_risks = process_trade_information()
        for r in top_twenty_risks:
            writer.writerow(r)

if __name__ == '__main__':
    main()

