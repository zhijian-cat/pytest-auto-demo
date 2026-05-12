import yaml
from pathlib import Path
from typing import List, Dict

class DataLoader:
    PROJECT_ROOT = Path(__file__).parent.parent


    @staticmethod
    def load_yaml(file_path):
        #获取项目根目录
        project_root = Path(__file__).parent.parent
        full_path = project_root / file_path

        with open(full_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        return data
    
    @staticmethod
    def get_test_cases(file_path, case_key):
        """获取测试用例列表"""
        data = DataLoader.load_yaml(file_path)
        return data[case_key]
    
    @classmethod
    def load_yaml(cls, file_path:str) -> Dict:
        full_path = cls.PROJECT_ROOT / file_path
        with open(full_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    @classmethod
    def get_test_cases(cls, file_path:str, case_key:str) ->List[Dict]:
        data = cls.load_yaml(file_path)
        return data.get(case_key, [])