# -*- coding: utf-8 -*-
"""
Prompt模板模块
Prompt Templates

包含用于周易占卜的prompt模板
"""


class PromptTemplates:
    """Prompt模板集合"""
    
    # 精简模式系统提示词 (与微调模型一致)
    SYSTEM_PROMPT_CONCISE = """你是一位精通周易的算命先生，擅长给人占卜吉凶。
要求：
1. 基于卦象给出明确的结论
2. 用老百姓听得懂的话说，不要文绉绉的
3. 必须引用周易原文来支撑你的判断"""
    
    # 精简模式占卜模板
    DIVINATION_TEMPLATE_CONCISE = """【占卜问题】
{question}

【起卦结果】
{hexagram_info}

【周易原文】
{hexagram_texts}

---

请严格按照以下格式回答，不要使用markdown格式：

一、结论
一句话直击重点，给出最终的结论（能成/不能成/具体情况）。

二、原因
请写成一段完整、连贯的话，不要分段，不要使用数字序号。内容必须包含：导致上述结论的具体原因分析，并直接引用周易原文中的关键句子作为佐证。请将原文引用自然地融入到你的分析中（例如：“依据卦辞中‘xxx’的描述，说明了……”），让原因和依据浑然一体。
"""
    
    @staticmethod
    def build_divination_prompt(question, hexagram_info, interpretation_guide, 
                               original_text, changed_text="", concise=False):
        """
        构建占卜prompt
        
        Args:
            question: 问卜问题
            hexagram_info: 卦象基本信息
            interpretation_guide: 解卦指引 (不再使用)
            original_text: 本卦文本
            changed_text: 之卦文本（可选）
            concise: 是否使用精简模式 (保留参数以兼容，但实际只支持精简模式)
            
        Returns:
            tuple: (user_prompt, system_prompt)
        """
        # 组合卦象文本
        hexagram_texts = original_text
        if changed_text:
            hexagram_texts += f"\n\n{'='*50}\n【之卦】\n{changed_text}"
        
        # 强制使用精简模板和系统提示词
        template = PromptTemplates.DIVINATION_TEMPLATE_CONCISE
        system_prompt = PromptTemplates.SYSTEM_PROMPT_CONCISE
        
        prompt = template.format(
            question=question if question else "无具体问题，请通占",
            hexagram_info=hexagram_info,
            hexagram_texts=hexagram_texts
        )
        
        return prompt, system_prompt


if __name__ == "__main__":
    # 测试模板
    prompt, system = PromptTemplates.build_divination_prompt(
        question="我的事业发展如何？",
        hexagram_info="乾卦，六爻安静",
        interpretation_guide="以卦辞断之",
        original_text="乾:元,亨,利,贞。",
        concise=True
    )
    
    print("系统提示词:")
    print(system)
    print("\n" + "="*60)
    print("\n用户提示词:")
    print(prompt)