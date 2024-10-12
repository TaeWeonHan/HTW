from config_SimPy import *
from log_SimPy import *
import environment as env
import pandas as pd
import Visualization

scenario = {"DEMAND": DEMAND_SCENARIO, "LEADTIME": LEADTIME_SCENARIO}
# sq_pair = [[1, 1], [1, 2], [1, 3], [1, 4], [2, 1], [2, 2], [2, 3], [3, 1], [3, 2]]
sq_pair = [[3, 5]]
# 환경 생성
simpy_env, inventoryList, procurementList, productionList, sales, customer, supplierList, daily_events = env.create_env(
    I, P, LOG_DAILY_EVENTS)  # DAILY_EVENTS를 LOG_DAILY_EVENTS로 변경
env.simpy_event_processes(simpy_env, inventoryList, procurementList,
                          productionList, sales, customer, supplierList, LOG_DAILY_EVENTS, I, scenario)

outter_state = {
    'Total': [],
    'Holding': [],
    'Process': [],
    'Delivery': [],
    'Order': [],
    'Shortage': []
}

if PRINT_SIM_EVENTS:
    print(f"============= 초기 재고 상태 =============")
    for inventory in inventoryList:
        print(
            f"Day 1 - {I[inventory.item_id]['NAME']} 재고: {inventory.on_hand_inventory} units")
    print(f"============= SimPy 시뮬레이션 시작 =============")

columns = []
for pair in sq_pair:
    SQPAIR['Reorder'] = pair[0]
    SQPAIR['Order'] = pair[1]
    state = [0, 0, 0, 0, 0, 0]
    for x in range(SIM_TIME):
        LOG_DAILY_EVENTS.append(f"\\nDay {(simpy_env.now) // 24+1} Report:")  # DAILY_EVENTS를 LOG_DAILY_EVENTS로 변경
        simpy_env.run(until=simpy_env.now+24)
        
        if PRINT_SIM_EVENTS:
            for log in LOG_DAILY_EVENTS:  # DAILY_EVENTS를 LOG_DAILY_EVENTS로 변경
                print(log)
        
        LOG_DAILY_EVENTS.clear()  # DAILY_EVENTS를 LOG_DAILY_EVENTS로 변경
        env.update_daily_report(inventoryList)
        env.Cost.update_cost_log(inventoryList)
        
        for index in range(len(DAILY_COST.keys())):  # DAILY_COST_REPORT를 DAILY_COST로 변경
            state[index + 1] += DAILY_COST[list(DAILY_COST.keys())[index]]
        
        print(state)
        print(DAILY_COST)  # DAILY_COST_REPORT를 DAILY_COST로 변경
        env.Cost.clear_cost()
        print(f"총 비용: {sum(LOG_COST)}")

    state[0] = sum(LOG_COST)
    outter_state['Total'].append(state[0])
    outter_state['Holding'].append(state[1])
    outter_state['Process'].append(state[2])
    outter_state['Delivery'].append(state[3])
    outter_state['Order'].append(state[4])
    outter_state['Shortage'].append(state[5])

export_Daily_Report = LOG_DAILY_REPORTS  # DAILY_REPORTS를 LOG_DAILY_REPORTS로 변경
daily_reports = pd.DataFrame(outter_state)
daily_reports.to_csv("./experiment_ss.csv")

# print(total_reward)

