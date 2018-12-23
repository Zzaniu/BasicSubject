import os
import traceback

import pandas as pd
import xlwings as xw


# 显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows', None)
#设置value的显示长度为100，默认为50
pd.set_option('max_colwidth',100)


def my_print(value1, value2):
    print('-'*10, value1, '-'*10)
    print(value2)
    print('')


def read_ecxel(file_path, sheet_no):
    # my_print('pd.read_excel(file_path, sheet_no, sheet_name=None)', pd.read_excel(file_path, sheet_name=0))
    all_data = pd.read_excel(file_path, sheet_name=sheet_no, skiprows=3)
    try:
        app = xw.App(visible=False, add_book=False)
        wb = app.books.open(file_path)
        for k in all_data:
            _count = len(all_data[k])  # 行数
            data = all_data[k]
            all_receivable = data.Amount.sum()  # 总回款
            sales = 0
            data1 = data.groupby(['Payment Type', 'Transaction type']).sum().reset_index()
            for i in range(len(data1)):
                if data1.iloc[i]['Payment Type'] == 'Product charges' and data1.iloc[i]['Transaction type'] == 'Order Payment':
                    sales += data1.iloc[i]['Amount']  # 总销售量
            data2 = data.groupby(['Payment Type', 'Transaction type', 'Product Title']).sum().reset_index()
            mini = 0  # 音箱
            feisty = 0  # 淘气小宠
            auricolare = 0  # 耳机
            # feisty = 0  # 挂钩
            for i in range(len(data2)):
                if data2.iloc[i]['Payment Type'] == 'Product charges' and data2.iloc[i]['Transaction type'] == 'Order Payment':
                    if data2.iloc[i]['Product Title'].lower().find('mini') > -1:
                        mini += data2.iloc[i]['Quantity']  # 音箱
                    if data2.iloc[i]['Product Title'].lower().startswith('feisty'):
                        feisty += data2.iloc[i]['Quantity']  # 淘气小宠
                    if data2.iloc[i]['Product Title'].lower().startswith(('auricolare', 'auriculares')):
                        auricolare += data2.iloc[i]['Quantity']  # 耳机

            sheet = wb.sheets[k]
            sheet.range('M{}'.format(_count+14)).value = ['回款合计', all_receivable]
            sheet.range('M{}'.format(_count+15)).value = ['总销售额', sales]
            sheet.range('I{}'.format(_count+16)).value = ['产品名称', '采购价RMB', 'FBA头程费', '销量', '总采购成本RMB', '总FBA头程成本RMB']
            sheet.range('I{}'.format(_count+17)).value = ['音箱', '46', '4', mini, mini*46, mini*4]
            sheet.range('I{}'.format(_count+18)).value = ['小宠', '87.5', '3.5', feisty, round(feisty*87.5, 2), round(feisty*3.5, 2)]
            sheet.range('I{}'.format(_count+19)).value = ['耳机', '8.1', '1.2', auricolare, round(auricolare*8.1, 2), round(auricolare*1.2, 2)]
            sheet.range('I{}'.format(_count+20)).value = ['挂钩', '40', '32', '0', 0, 0]
            print('sheet{}插入完毕'.format(k))
    except:
        print('出错了，错误信息:{}'.format(traceback.format_exc()))
    finally:
        wb.save()
        wb.close()
        app.quit()
        print('excel{}写入完毕'.format(file_path))


if __name__ == "__main__":
    base_dir = r'C:\Users\Zzaniu\Documents\WeChat Files\Ly-holy\Files'
    file_name = ['ES Transaction Summary.xlsx', 'IT Transaction Summary.xlsx']
    for filename in file_name:
        read_ecxel(os.path.join(base_dir, filename), None)
    print('程序运行完毕')

