from config_SimPy import *
from log_SimPy import *
import environment as env
import pandas as pd
import Visualization

# Define the scenario
scenario = {"DEMAND": DEMAND_SCENARIO, "LEADTIME": LEADTIME_SCENARIO}

# Create environment
simpy_env, inventoryList, procurementList, productionList, sales, customer, supplierList, daily_events = env.create_env(
    I, P, LOG_DAILY_EVENTS)
env.simpy_event_processes(simpy_env, inventoryList, procurementList,
                          productionList, sales, customer, supplierList, daily_events, I, scenario)


if PRINT_SIM_EVENTS:
    print(f"============= Initial Inventory Status =============")
    for inventory in inventoryList:
        print(
            f"{I[inventory.item_id]['NAME']} Inventory: {inventory.on_hand_inventory} units")

    print(f"============= SimPy Simulation Begins =============")

for x in range(SIM_TIME):
    print(f"\nDay {(simpy_env.now) // 24+1} Report:")
    simpy_env.run(until=simpy_env.now+24)  # Run the simulation for 24 hours

    # Print the simulation log every 24 hours (1 day)
    if PRINT_SIM_EVENTS:
        for log in daily_events:
            print(log)
    daily_events.clear()

    env.update_daily_report(inventoryList)
    # Print the daily report
    if PRINT_SIM_REPORT:
        for id in range(len(inventoryList)):
            print(LOG_DAILY_REPORTS[x][id])

    env.Cost.update_cost_log(inventoryList)
    # Print the daily cost
    
    if PRINT_DAILY_COST:
        for key in DAILY_COST.keys():
            print(f"{key}: {DAILY_COST[key]}")
        print(f"Daily Total Cost: {LOG_COST[-1]}")
    print(f"Cumulative Total Cost: {sum(LOG_COST)}")

    env.Cost.clear_cost()
    
# CSV 파일로 리포트 내보내기
export_Daily_Report = LOG_DAILY_REPORTS  # log_SimPy.py에서 데이터를 불러옴
daily_reports = pd.DataFrame(export_Daily_Report)

# 컬럼 리스트 수정
columns_list = []
for keys in I.keys():
    columns_list.append("DAY")  # DAY가 추가됨
    columns_list.append(f"{I[keys]['NAME']}'s NAME")
    columns_list.append(f"{I[keys]['NAME']}'s TYPE")
    columns_list.append(f"{I[keys]['NAME']}'s START")
    columns_list.append(f"{I[keys]['NAME']}'s INCOME")
    columns_list.append(f"{I[keys]['NAME']}'s OUTCOME")
    columns_list.append(f"{I[keys]['NAME']}'s IN_TRANSITION")
    columns_list.append(f"{I[keys]['NAME']}'s END")


# 오류를 해결하기 위해 두 개의 리스트가 일치하도록 조정
daily_reports.columns = columns_list
daily_reports.to_csv("./Daily_Report.csv")  # CSV 파일 저장

export_Cost_Report = LOG_CUMULATIVE_COST
daily_cost_reports = pd.DataFrame(export_Cost_Report)
daily_cost_reports.to_csv("./Daily_Cost_Report.csv")

if VISUALIAZTION != False:
    Visualization.visualization(export_Daily_Report, export_Cost_Report)