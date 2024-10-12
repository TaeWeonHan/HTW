import matplotlib.pyplot as plt
from config_SimPy import *

def visualization(export_Daily_Report, export_Cost_Report):
    Visual_Dict = {
        'Material': [],
        'Material Total': [],
        'Product': [],
        'Total Cost': [],  # Total Cost 항목 추가
        'Keys': {'Material': [], 'Material Total': [], 'Product': [], 'Total Cost': []}
    }
    Key = ['Material', 'Product', 'Total Cost']  # Total Cost를 Key에 추가

    for id in I.keys():
        temp = []
        for x in range(SIM_TIME): 
            temp.append(export_Daily_Report[x][id*8+7])  # 매일 말 재고량 기록
        Visual_Dict[export_Daily_Report[0][id*8+2]].append(temp)  # 업데이트
        Visual_Dict['Keys'][export_Daily_Report[0][2+id*8]].append(export_Daily_Report[0][id *8+1])  # Keys 업데이트
    
        if I[id]['NAME'] == 'MATERIAL 1':
            temp_transit = []
            temp_total = []
            for x in range(SIM_TIME):
                in_transition = export_Daily_Report[x][id*8+6]  # IN_TRANSITION 위치
                temp_transit.append(export_Daily_Report[x][id*8+6])  # IN_TRANSITION 위치 (id*8+6)
                temp_total.append(export_Daily_Report[x][id*8+7] + in_transition)
            Visual_Dict['Material Total'].append(temp_total)
            Visual_Dict['Keys']['Material Total'].append('Material Total')

    # Total Cost 데이터 추가
    total_cost_data = list(export_Cost_Report)  # 단순히 리스트로 변환
    Visual_Dict['Total Cost'].append(total_cost_data)
    Visual_Dict['Keys']['Total Cost'].append('Total Cost')

    # 시각화 생성
    visual = VISUALIAZTION.count(1)
    count_type = 0
    cont_len = 1
    for x in VISUALIAZTION:
        if x == 1:
            plt.subplot(int(f"{visual}1{cont_len}"))
            cont_len += 1
            if count_type < len(Key):  # Key 리스트의 길이를 초과하지 않도록 검사
                days = range(1, SIM_TIME + 1)  # Day 1, Day 2, ..., Day N 설정
                for lst in Visual_Dict[Key[count_type]]:
                    plt.plot(days, lst, label=Visual_Dict['Keys'][Key[count_type]][0])
                    if Key[count_type] == 'Material':
                        plt.plot(days, Visual_Dict['Material Total'][0], label='Material Total', linestyle='--')
                        reorder_point = REORDER_LEVEL
                        plt.axhline(y=reorder_point, color='r', linestyle='--', label='Reorder Point')
                    plt.legend()

            # x축 레이블을 Day로 설정
            plt.xticks(ticks=days, labels=[f"{day}" for day in days], rotation=45)
            plt.xlabel("Day")
            count_type += 1

    plt.savefig("Graph")
    plt.clf()
