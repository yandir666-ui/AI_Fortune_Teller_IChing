# -*- coding: utf-8 -*-
"""
大衍筮法模拟器
Dayan Divination Simulator

模拟传统的大衍筮法起卦过程，通过三变成一爻，六爻成卦的方式
生成本卦和之卦，用于周易占卜。
"""

import random
import time
import sys


class DayanDivination:
    """大衍筮法模拟器"""
    
    def __init__(self, verbose=True):
        """
        初始化大衍筮法模拟器
        
        Args:
            verbose: 是否显示详细过程，默认True
        """
        self.lines = []  # 存储六爻结果
        self.total_stalks = 50
        self.verbose = verbose

    def type_print(self, text, speed=0.01):
        """打字机效果，模拟叙述感"""
        if not self.verbose:
            return
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(speed)
        print()

    def wait(self, seconds):
        """模拟动作的自然停顿"""
        if self.verbose:
            time.sleep(seconds)

    def human_split(self, total):
        """
        【分二】模拟：人手分草，符合高斯分布（正态分布）
        """
        half = total / 2
        # 模拟人手误差，大部分时候在中间，偶尔偏多偏少
        left = int(random.gauss(half, 2.0))
        
        # 边界修正：任何一堆至少要有1根
        if left < 1: left = 1
        if left >= total: left = total - 1
        
        right = total - left
        return left, right

    def _calculate_physical_count(self, count):
        """内部计算揲四结果"""
        remainder = count % 4
        if remainder == 0:
            remainder = 4
        return remainder

    def _display_physical_count(self, pile_name, count):
        """显示揲四过程"""
        if not self.verbose:
            return 4 if count % 4 == 0 else count % 4

        sys.stdout.write(f"      [{pile_name}手] 揲四计数: ")
        sys.stdout.flush()
        
        current = count
        # 视觉特效：每减一次显示一个点
        while current > 4:
            current -= 4
            sys.stdout.write(".")  # 每一个点代表数走了4根
            sys.stdout.flush()
            time.sleep(0.02)  # 数数的速度
            
        remainder = 4 if current == 0 else current
        print(f" 剩 {remainder} 策")
        return remainder

    def _calculate_change(self, current_total):
        """
        计算【一变】的数据
        """
        # 1. 分二
        left, right = self.human_split(current_total)
        
        # 2. 挂一
        right_hang = right - 1
        hang_one = 1
        
        # 3. 揲四
        left_rem = self._calculate_physical_count(left)
        right_rem = self._calculate_physical_count(right_hang)
        
        # 5. 归奇
        removed = hang_one + left_rem + right_rem
        new_total = current_total - removed
        
        return {
            "left": left,
            "right": right,
            "left_rem": left_rem,
            "right_rem": right_rem,
            "removed": removed,
            "new_total": new_total
        }

    def _calculate_line(self):
        """计算【一爻】的三变数据"""
        current_stalks = 49
        changes = []
        
        for _ in range(3):
            change_data = self._calculate_change(current_stalks)
            changes.append(change_data)
            current_stalks = change_data['new_total']
            
        # 三变之后，定爻
        final_num = current_stalks // 4
        return final_num, changes

    def simulate(self):
        """
        立即执行完整演算，不显示过程
        
        Returns:
            dict: 包含所有步骤数据的字典，用于后续回放
        """
        line_data = []
        final_lines = []
        
        for i in range(1, 7):
            val, changes = self._calculate_line()
            final_lines.append(val)
            line_data.append({
                "line_idx": i,
                "value": val,
                "changes": changes
            })
            
        self.lines = final_lines
        hex_result = self.get_hexagram_result()
        
        return {
            "hex_result": hex_result,
            "process_log": line_data
        }

    def play_process(self, simulation_data):
        """
        根据模拟数据回放这一过程
        """
        if not self.verbose:
            return

        print("\n" + "="*60)
        print("          大 衍 筮 法 · 全 过 程 模 拟")
        print("="*60)
        self.type_print("大衍之数五十，其用四十有九。")
        self.type_print("分而为二以象两，挂一以象三，")
        self.type_print("揲之以四以象四时，归奇于扐以象润。")
        print("="*60)
        self.wait(1)

        pos_names = ["初", "二", "三", "四", "五", "上"]
        process_log = simulation_data["process_log"]

        for line_step in process_log:
            line_idx = line_step["line_idx"]
            val = line_step["value"]
            changes = line_step["changes"]
            
            print("\n" + "#" * 60)
            print(f"###  正在演算：{pos_names[line_idx-1]}爻  ###")
            print("#" * 60)
            
            current_total = 49 # 每次都从49开始描述吗？不对，是每一爻开始都是49
            
            for change_idx, change in enumerate(changes, 1):
                print(f"    < 第 {line_idx} 爻 - 第 {change_idx} 变 >")
                
                # 回放：分二
                print(f"      [分二]  左手: {change['left']}  |  右手: {change['right']}  (总: {current_total})")
                self.wait(0.3)
                
                # 回放：挂一
                print(f"      [挂一]  取右一策，挂于左手小指")
                
                # 回放：揲四 (这里需要模拟视觉效果)
                self._display_physical_count("左", change['left'])
                
                # 右手实际上是减了1之后再去揲四的
                self._display_physical_count("右", change['right'] - 1)
                
                # 回放：归奇
                print(f"      [归奇]  挂1 + 左余{change['left_rem']} + 右余{change['right_rem']} = 去掉 {change['removed']} 策")
                print(f"      [结余]  当前剩余: {change['new_total']} 策")
                print("-" * 60)
                self.wait(0.5)
                
                current_total = change['new_total']

            # 显示该爻结果
            result_text = ""
            if val == 6: result_text = "老阴 (六) -> 变"
            elif val == 7: result_text = "少阳 (七) -> 不变"
            elif val == 8: result_text = "少阴 (八) -> 不变"
            elif val == 9: result_text = "老阳 (九) -> 变"
            
            print(f"  >>> {pos_names[line_idx-1]}爻 结果判定: 剩 {current_total} 策 ÷ 4 = {val}")
            print(f"  >>> 获得: {result_text}")
            self.wait(1.5)

        # 显示最终卦象
        self.display_hexagram()

    def run(self):
        """
        主程序 - 向后兼容
        """
        # 1. 模拟 calculations
        data = self.simulate()
        # 2. 播放 visualization
        self.play_process(data)
        # 3. 返回结果
        return data["hex_result"]

    def get_hexagram_result(self):
        """
        获取卦象结果
        
        Returns:
            dict: {
                'original_lines': [6,7,8,9,...],  # 原始爻值
                'original_binary': '101010',       # 本卦二进制
                'changed_binary': '101011',        # 之卦二进制
                'changing_lines': [1, 3],          # 变爻位置
                'has_change': True                 # 是否有变爻
            }
        """
        # 计算本卦和之卦的二进制表示
        original_binary = ""
        changed_binary = ""
        changing_lines = []
        
        for idx, val in enumerate(self.lines):
            # 本卦：7,9为阳(1)，6,8为阴(0)
            if val in [7, 9]:
                original_binary += "1"
            else:
                original_binary += "0"
            
            # 之卦：老阴(6)变阳，老阳(9)变阴
            if val == 6:  # 老阴变阳
                changed_binary += "1"
                changing_lines.append(idx + 1)
            elif val == 9:  # 老阳变阴
                changed_binary += "0"
                changing_lines.append(idx + 1)
            elif val == 7:  # 少阳不变
                changed_binary += "1"
            else:  # val == 8, 少阴不变
                changed_binary += "0"
        
        return {
            'original_lines': self.lines.copy(),
            'original_binary': original_binary,
            'changed_binary': changed_binary,
            'changing_lines': changing_lines,
            'has_change': len(changing_lines) > 0
        }

    def display_hexagram(self):
        """
        显示最终的本卦与之卦
        """
        print("\n\n")
        print("="*60)
        print(f"{'【 本 卦 】':^28}")
        print("="*60)
        
        pos_names = ["初", "二", "三", "四", "五", "上"]
        
        # 倒序遍历，因为画卦是从上往下画
        for i in range(5, -1, -1):
            num = self.lines[i]
            p_name = pos_names[i]
            
            # 定义符号（短横，便于紧凑显示）
            yin = "— —"
            yang = "———"
            
            # 构建本卦的图形（仅显示本卦，去掉之卦）
            if num == 6:  # 老阴 -> 变阳（显示为老阴的本卦形态）
                left = f"{yin} x"
                name = "老阴"
            elif num == 7:  # 少阳 -> 不变
                left = f"{yang}  "
                name = "少阳"
            elif num == 8:  # 少阴 -> 不变
                left = f"{yin}  "
                name = "少阴"
            elif num == 9:  # 老阳 -> 变阴
                left = f"{yang} o"
                name = "老阳"
                
            # 格式化输出（仅本卦），对齐本卦图像并缩短横杠
            label = f"{p_name}{'九' if num%2!=0 else '六'}:"
            print(f"{label:<4} {left:<9} ({name})")
            
        print("="*60)
        self.analyze_summary()
        
    def analyze_summary(self):
        """分析变爻情况并给出断语参考"""
        return


# --- 执行 ---
if __name__ == "__main__":
    sim = DayanDivination(verbose=True)
    result = sim.run()
    print("\n结果数据:")
    print(f"本卦: {result['original_binary']}")
    print(f"变爻: {result['changing_lines']}")
