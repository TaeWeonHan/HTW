import matplotlib.pyplot as plt
from config_SimPy import *
from environment import *
import numpy as np

def visualization(export_Daily_Report):
    Visual_Dict = {
        'Material': [],
        'WIP': [],
        'Product': [],
        'Keys': {'Material': [], 'WIP': [], 'Product': []}
    }
    Key = ['Material', 'WIP', 'Product']

    # 예를 들어, 주문 시점과 LEAD_TIME 정의
    order_days = [3, 8, 13]  # 주문이 이루어진 날짜 인덱스
    LEAD_TIME = 2  # 리드 타임은 2일

    for id in I.keys():
        temp = []
        for x in range(SIM_TIME):
            temp.append(export_Daily_Report[x][id*7+6])  # Record Onhand inventory at day end
        Visual_Dict[export_Daily_Report[0][id*7+2]].append(temp)  # Update 
        Visual_Dict['Keys'][export_Daily_Report[0][2+id*7]].append(export_Daily_Report[0][id*7+1])  # Update Keys
    
    visual = VISUALIZATION.count(1)
    count_type = 0
    cont_len = 1
    for x in VISUALIZATION:
        cont = 0
        if x == 1:
            plt.subplot(int(f"{visual}1{cont_len}"))
            cont_len += 1
            for lst in Visual_Dict[Key[count_type]]:
                plt.plot(lst, label=Visual_Dict['Keys'][Key[count_type]][cont])
                
                if Key[count_type] != 'Product':
                    plt.axhline(y=S_REORDER_POINT, color='r', linestyle='--', label='S_REORDER_POINT' if cont == 0 else "")
                plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
                cont += 1
            plt.xticks(ticks=np.arange(0, 14, 1), labels=np.arange(1, 15, 1))

        count_type += 1
    plt.subplots_adjust(right=0.85)  # Adjust the right margin
    plt.savefig("Graph", bbox_inches='tight')  # Adjust for any overflow due to legend
    plt.clf()
