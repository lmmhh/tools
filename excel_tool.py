# -*- coding: UTF-8 -*-
import pandas as pd


class ExcelTool:

    def __init__(self, file_path):
        self.file_path = file_path

    def read_excel(self, sheet_name='Sheet1', header=0):
        try:
            if self.file_path.endswith('.xlsx'):
                df = pd.read_excel(self.file_path, sheet_name=sheet_name)
                return df
            elif self.file_path.endswith('.csv'):
                df = pd.read_csv(self.file_path, header=header, encoding='gbk')
                return df
            else:
                print(f"Not supported file type: {self.file_path}")
                return None
        except Exception as e:
            print(f"Error reading Excel file: {e}")
            return None

    def write_excel(self, data, sheet_name='Sheet1', index=False):
        try:
            writer = pd.ExcelWriter(self.file_path, engine='xlsxwriter')
            data.to_excel(writer, sheet_name=sheet_name, index=index)
            writer.save()
            print("Excel file written successfully.")
        except Exception as e:
            print(f"Error writing Excel file: {e}")

    def column_label(self):
        try:
            df = self.read_excel()
            print(df.columns)
        except Exception as e:
            print(f"Error filtering data: {e}")
            return None

    def transform_data(self, column, func):
        try:
            df = self.read_excel()
            df[column] = df[column].apply(func)
            return df
        except Exception as e:
            print(f"Error transforming data: {e}")
            return None


# 使用示例
if __name__ == '__main__':

    file_name = '230713mn'
    excel_file_path = 'D:/data/wave_data/' + file_name + '.csv'
    excel_tool = ExcelTool(excel_file_path)
    # 数据转换
    transformed_data = excel_tool.transform_data(column='Column1', func=lambda x: x * 2)
    print("Transformed Data:")
    print(transformed_data)


###############################################################################################################
## 测试代码
# import pytest
# from s.tools.excel_tool import ExcelTool
#
# # 测试构造函数和 read_excel 方法（.xlsx 文件）
# def test_excel_tool_xlsx():
#     tool = ExcelTool('test.xlsx')
#     df = tool.read_excel()
#     assert df is not None
#
# # 测试构造函数和 read_excel 方法（.csv 文件）
# def test_excel_tool_csv():
#     tool = ExcelTool('test.csv')
#     df = tool.read_excel()
#     assert df is not None
#
# # 测试 write_excel 方法
# def test_write_excel():
#     tool = ExcelTool('test_output.xlsx')
#     data = {'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']}
#     df = pd.DataFrame(data)
#     tool.write_excel(df)
#
# # 测试 column_label 方法
# def test_column_label():
#     tool = ExcelTool('test.xlsx')
#     tool.column_label()
#
# # 测试 transform_data 方法
# def test_transform_data():
#     tool = ExcelTool('test.xlsx')
#     df = tool.transform_data('col1', lambda x: x * 2)
#     assert df is not None
###############################################################################################################


###############################################################################################################
## 中文注释
# class ExcelTool:
#     """
#     ExcelTool 类，用于处理 Excel 文件的读取和写入操作。
#
#     参数：
#         file_path (str)：要处理的 Excel 文件的路径。
#
#     方法：
#         read_excel(sheet_name='Sheet1')：
#             读取 Excel 文件，如果是.xlsx 或.csv 格式，则分别使用 pandas 的 read_excel 和 read_csv 方法读取，
#             并返回一个 DataFrame。如果文件格式不支持，则打印错误信息并返回 None。
#
#         write_excel(data, sheet_name='Sheet1', index=False)：
#             将数据写入 Excel 文件。使用 pandas 的 ExcelWriter 创建一个 writer 对象，然后将数据写入指定的 sheet 中，最后保存文件。
#
#         column_label()：
#             读取 Excel 文件，并打印出所有列的标签。
#
#         transform_data(column, func)：
#             读取 Excel 文件，并对指定列应用一个函数进行转换，然后返回转换后的数据。
#     """
#
#     def __init__(self, file_path):
#         """
#         初始化 ExcelTool 类的实例，并传入文件路径。
#
#         参数：
#             file_path (str)：要处理的 Excel 文件的路径。
#         """
#         self.file_path = file_path
#
#     def read_excel(self, sheet_name='Sheet1'):
#         """
#         尝试读取 Excel 文件
#
#         参数：
#             sheet_name (str), 默认为 Sheet1: 指定要读取的工作表名称。
#
#         返回：
#             pandas.DataFrame 或 None: 成功时返回读取的数据；如果文件格式不支持或读取失败，则返回 None。
#         """
#         try:
#             if self.file_path.endswith('.xlsx'):
#                 df = pd.read_excel(self.file_path, sheet_name=sheet_name)
#                 return df
#             elif self.file_path.endswith('.csv'):
#                 df = pd.read_csv(self.file_path, header=20, encoding='gbk')
#                 return df
#             else:
#                 print(f"Not supported file type: {self.file_path}")
#                 return None
#         except Exception as e:
#             print(f"Error reading Excel file: {e}")
#             return None
#
#     def write_excel(self, data, sheet_name='Sheet1', index=False):
#         """
#         将数据写入 Excel 文件。
#
#         参数：
#             data (pandas.DataFrame): 要写入 Excel 文件的数据。
#             sheet_name (str), 默认为 Sheet1: 指定要写入的工作表名称。
#             index (bool), 默认为 False: 是否写入行索引。
#         """
#         try:
#             writer = pd.ExcelWriter(self.file_path, engine='xlsxwriter')
#             data.to_excel(writer, sheet_name=sheet_name, index=index)
#             writer.save()
#             print("Excel file written successfully.")
#         except Exception as e:
#             print(f"Error writing Excel file: {e}")
#
#     def column_label(self):
#         """
#         读取 Excel 文件，并打印出所有列的标签。
#         """
#         try:
#             df = self.read_excel()
#             print(df.columns)
#         except Exception as e:
#             print(f"Error filtering data: {e}")
#             return None
#
#     def transform_data(self, column, func):
#         """
#         读取 Excel 文件，并对指定列应用一个函数进行转换，然后返回转换后的数据。
#
#         参数：
#             column (str): 要转换的列名。
#             func (function): 要应用的转换函数。
#
#         返回：
#             pandas.DataFrame 或 None: 成功时返回转换后的数据；如果转换失败，则返回 None。
#         """
#         try:
#             df = self.read_excel()
#             df[column] = df[column].apply(func)
#             return df
#         except Exception as e:
#             print(f"Error transforming data: {e}")
#             return None
###############################################################################################################