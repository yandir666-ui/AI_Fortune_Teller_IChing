# -*- coding: utf-8 -*-
"""
卦象解析模块
Hexagram Interpreter

负责根据二进制卦象查找对应的64卦信息，并提取相关文本
"""

import json
from pathlib import Path


class HexagramInterpreter:
    """卦象解释器"""
    
    # 64卦二进制到卦序的映射表（下卦在前，上卦在后）
    BINARY_TO_NUMBER = {
        "111111": 1,  # 乾为天
        "000000": 2,  # 坤为地
        "010001": 3,  # 水雷屯
        "100010": 4,  # 山水蒙
        "010111": 5,  # 水天需
        "111010": 6,  # 天水讼
        "000010": 7,  # 地水师
        "010000": 8,  # 水地比
        "110111": 9,  # 风天小畜
        "111011": 10, # 天泽履
        "000111": 11, # 地天泰
        "111000": 12, # 天地否
        "111101": 13, # 天火同人
        "101111": 14, # 火天大有
        "000100": 15, # 地山谦
        "001000": 16, # 雷地豫
        "011001": 17, # 泽雷随
        "100110": 18, # 山风蛊
        "000011": 19, # 地泽临
        "110000": 20, # 风地观
        "101001": 21, # 火雷噬嗑
        "100101": 22, # 山火贲
        "100000": 23, # 山地剥
        "000001": 24, # 地雷复
        "111001": 25, # 天雷无妄
        "100111": 26, # 山天大畜
        "100001": 27, # 山雷颐
        "011110": 28, # 泽风大过
        "010010": 29, # 坎为水
        "101101": 30, # 离为火
        "011100": 31, # 泽山咸
        "001110": 32, # 雷风恒
        "111100": 33, # 天山遁
        "001111": 34, # 雷天大壮
        "101000": 35, # 火地晋
        "000101": 36, # 地火明夷
        "110101": 37, # 风火家人
        "101011": 38, # 火泽睽
        "010100": 39, # 水山蹇
        "001010": 40, # 雷水解
        "100011": 41, # 山泽损
        "110001": 42, # 风雷益
        "011111": 43, # 泽天夬
        "111110": 44, # 天风姤
        "011000": 45, # 泽地萃
        "000110": 46, # 地风升
        "011010": 47, # 泽水困
        "010110": 48, # 水风井
        "011101": 49, # 泽火革
        "101110": 50, # 火风鼎
        "001001": 51, # 震为雷
        "100100": 52, # 艮为山
        "110100": 53, # 风山渐
        "001011": 54, # 雷泽归妹
        "001101": 55, # 雷火丰
        "101100": 56, # 火山旅
        "110110": 57, # 巽为风
        "011011": 58, # 兑为泽
        "110010": 59, # 风水涣
        "010011": 60, # 水泽节
        "110011": 61, # 风泽中孚
        "001100": 62, # 雷山小过
        "010101": 63, # 水火既济
        "101010": 64, # 火水未济
    }
    
    def __init__(self, data_path="hexagrams_data.json"):
        """
        初始化卦象解释器
        
        Args:
            data_path: 卦象数据JSON文件路径
        """
        # 如果是相对路径，则相对于当前脚本所在目录
        if not Path(data_path).is_absolute():
            script_dir = Path(__file__).parent
            self.data_path = script_dir / data_path
        else:
            self.data_path = Path(data_path)
        self.hexagrams_data = self._load_data()
    
    def _load_data(self):
        """加载卦象数据"""
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data.get('hexagrams', {})
        except FileNotFoundError:
            print(f"警告: 未找到数据文件 {self.data_path}")
            print(f"当前查找路径: {self.data_path.absolute()}")
            return {}
        except json.JSONDecodeError as e:
            print(f"警告: JSON解析错误 - {e}")
            return {}
    
    def binary_to_number(self, binary_str):
        """
        将二进制卦象转换为卦序号
        
        Args:
            binary_str: 六位二进制字符串，如 "111111"
            
        Returns:
            int: 卦序号 (1-64)，未找到返回None
        """
        return self.BINARY_TO_NUMBER.get(binary_str)
    
    def get_hexagram_by_number(self, number):
        """
        根据卦序号获取卦象信息
        
        Args:
            number: 卦序号 (1-64)
            
        Returns:
            dict: 卦象信息，未找到返回None
        """
        return self.hexagrams_data.get(str(number))
    
    def get_hexagram_by_binary(self, binary_str):
        """
        根据二进制获取卦象信息
        
        Args:
            binary_str: 六位二进制字符串
            
        Returns:
            dict: 卦象信息，未找到返回None
        """
        number = self.binary_to_number(binary_str)
        if number is None:
            return None
        return self.get_hexagram_by_number(number)
    
    def format_hexagram_text(self, hexagram_data, include_lines=None):
        """
        格式化卦象文本用于prompt
        
        Args:
            hexagram_data: 卦象数据字典
            include_lines: 需要包含的爻辞列表，如[1,3,5]，None表示不包含爻辞
            
        Returns:
            str: 格式化后的文本
        """
        if not hexagram_data:
            return "未找到卦象数据"
        
        text_parts = []
        
        # 基本信息
        text_parts.append(f"【{hexagram_data.get('name_cn', '未知')}卦】")
        text_parts.append(f"卦序: 第{hexagram_data.get('number', '?')}卦")
        
        # 卦辞
        judgement = hexagram_data.get('judgement', '')
        if judgement:
            text_parts.append(f"\n卦辞: {judgement}")
        
        # 彖传
        judgement_detail = hexagram_data.get('judgement_detail', '')
        if judgement_detail:
            text_parts.append(f"{judgement_detail}")
        
        # 象传
        image = hexagram_data.get('image', '')
        if image:
            text_parts.append(f"\n{image}")
        
        if include_lines and 'lines' in hexagram_data:
            text_parts.append("\n相关爻辞:")
            # 确保按从下往上的顺序排列（1-6）
            for line_num in sorted(include_lines):
                line_data = hexagram_data['lines'].get(str(line_num))
                if line_data:
                    text_parts.append(f"  {line_data.get('text', '')}")
                    text_parts.append(f"  {line_data.get('image', '')}")
        
        return "\n".join(text_parts)
    
    def interpret_divination_result(self, divination_result):
        """
        解释大衍筮法的结果
        
        Args:
            divination_result: DayanDivination.run() 返回的结果字典
            
        Returns:
            dict: {
                'original_hexagram': 本卦信息,
                'changed_hexagram': 之卦信息,
                'original_text': 本卦文本,
                'changed_text': 之卦文本,
                'changing_lines': 变爻列表,
                'interpretation_guide': 解卦指南
            }
        """
        original_binary = divination_result['original_binary']
        changed_binary = divination_result['changed_binary']
        changing_lines = divination_result['changing_lines']
        
        # 获取卦象数据
        original_hex = self.get_hexagram_by_binary(original_binary)
        changed_hex = self.get_hexagram_by_binary(changed_binary) if divination_result['has_change'] else None
        
        # 根据变爻数量决定文本内容
        original_text = ""
        changed_text = ""
        guide = ""
        
        if len(changing_lines) == 0:
            # 无变爻：看本卦卦辞
            original_text = self.format_hexagram_text(original_hex, include_lines=None)
            guide = "六爻安静，无变卦。以本卦卦辞断之。"
            
        elif len(changing_lines) == 1:
            # 一爻动：看本卦变爻爻辞
            original_text = self.format_hexagram_text(original_hex, include_lines=changing_lines)
            guide = f"一爻动（第{changing_lines[0]}爻）。以本卦变爻爻辞断之。"
            
        elif len(changing_lines) == 2:
            # 二爻动：看本卦两个变爻爻辞，以上爻为主
            original_text = self.format_hexagram_text(original_hex, include_lines=changing_lines)
            guide = f"二爻动（第{'、'.join(map(str, sorted(changing_lines)))}爻）。以本卦二变爻之辞占，上爻为主。"
            
        elif len(changing_lines) == 3:
            # 三爻动：本卦和之卦卦辞合占
            original_text = self.format_hexagram_text(original_hex, include_lines=None)
            changed_text = self.format_hexagram_text(changed_hex, include_lines=None)
            guide = "三爻动。以本卦与之卦卦辞合占。"
            
        else:
            # 多爻动：以之卦卦辞为主
            changed_text = self.format_hexagram_text(changed_hex, include_lines=None)
            guide = f"变爻多达{len(changing_lines)}个。以之卦卦辞为主。"
        
        return {
            'original_hexagram': original_hex,
            'changed_hexagram': changed_hex,
            'original_text': original_text,
            'changed_text': changed_text,
            'changing_lines': changing_lines,
            'interpretation_guide': guide
        }


if __name__ == "__main__":
    # 测试代码
    interpreter = HexagramInterpreter()
    
    # 测试：乾卦
    test_result = {
        'original_binary': '111111',
        'changed_binary': '111111',
        'changing_lines': [],
        'has_change': False
    }
    
    interpretation = interpreter.interpret_divination_result(test_result)
    print(interpretation['original_text'])
    print("\n" + interpretation['interpretation_guide'])
